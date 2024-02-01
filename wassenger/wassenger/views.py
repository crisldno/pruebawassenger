from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from .models import USUARIOS, USUARIOS_MOVIL
from django.http import HttpResponse
import json
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from urllib.parse import urljoin
from datetime import datetime, timedelta
from django.utils import timezone
import random


@csrf_exempt 
def webhook_handler(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        sesion = sesion_estado(data)
        sesion_expirada = tiempo_sesion(sesion)
        if sesion_expirada:
            sesion = sesion_estado(data)
        print(sesion)
        response = procesar(data, sesion)
        
        return JsonResponse(response)
    
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    

def sesion_estado(data):
    mensaje = data.get("data", {})
    try:
        usuario = USUARIOS.objects.get(celular = mensaje.get("fromNumber", "").lower(),estado = True)
    except USUARIOS.DoesNotExist:

        usuario = USUARIOS.objects.get(id_usuario=1)
    
    device,creado = USUARIOS_MOVIL.objects.get_or_create(id_device=mensaje.get("from", "").lower(), estado = True, defaults={
        'id_usuario':usuario,
        'celular':mensaje.get("fromNumber", "").lower(),
        'estado':True,
        'id_device':mensaje.get("from", "").lower(),
        'estado_solicitud':1
        })     
    
    data = device      
        #print("El registro ya existía.")
    print(data.id_usuario_movil)
    return data
    return serialize('json', [data])


def procesar(request,sesion):
    opcion = sesion.estado_solicitud
    match opcion:
        case 1:
            #bienvenida
            sesion.estado_solicitud = 2
            sesion.save()
            status = enviar_mensaje(sesion.celular, "Hola Bienvenido a Andes Servicio De Certificación digital. En el momento no cuentas con solicitudes pendientes, ¿deseas realizar una? 1. Si 2. No")

        case 2:
            #respuesta bienvenida
            status = procesar_respuesta_bienvenida(request.get("data", {}).get("body", "").lower(), sesion)
        case 3:
            #respuesta nombre
            #status = procesar_tipo_proceso(request.get("data", {}).get("body", "").lower(), sesion)
            status = procesar_nombres(request.get("data", {}).get("body", "").lower(), sesion)
        case 4:
             #respuesta foto
            status = procesar_doc_front(request,sesion)
        case 5:
             #respuesta foto
            status = procesar_doc_front(request,sesion)
        case 6:
             #respuesta pago
            status = procesar_pago(request.get("data", {}).get("body", "").lower(), sesion)
        case 7:
             #respuesta 
            status = reintentar(request.get("data", {}).get("body", "").lower(), sesion)
        
        


        #case _:

            #no valida    
            print("Opción no válida")

    return status

def procesar_respuesta_bienvenida(respuesta_usuario, sesion):
    if respuesta_usuario == '1':
        sesion.estado_solicitud = 3
        sesion.save()
        mensaje = "Perfecto. Ahora, por favor, digita tu nombre completo."
        
    elif respuesta_usuario == '2':
        mensaje = "perfecto. estaremos pendientes por si cambias de opinion."
        sesion.estado = False
        sesion.save()
        
    else:
        mensaje = 'Opción incorrecta. Recuerda digitar una opción válida: 1.SI 2.NO'
    return enviar_mensaje(sesion.celular, mensaje)

def procesar_nombres(respuesta_usuario, sesion):
    nombre_apellido = respuesta_usuario.split()
    ahora = timezone.now()
    if len(nombre_apellido) >= 2:  # Verificar si se proporcionaron al menos un nombre y un apellido
        device,creado = USUARIOS.objects.get_or_create(nombres= nombre_apellido[0], apellidos= nombre_apellido[1:], estado = True, defaults={
            'id_rol':1,
            'nombres':nombre_apellido[0], 
            'apellidos':format(nombre_apellido[1:]), 
            'id_tipo_documento':1,
            'documento':"11111",
            'fecha_expide_doc':ahora, 
            'celular':sesion.celular, 
            'email': "text@text.com",
            'email_confirmed': True,
            'email_verified_at': ahora,
            'email_confirmation_code':"lkjhg",
            'password':"hgghgj",
            'estado': True,
            'created_at': ahora,
            'updated_at':ahora,
        })
    
        sesion.id_usuario_id = int(device.id_usuario)   
        sesion.estado_solicitud = 4
        sesion.save()
        mensaje = "Gracias {}. ¿En qué más puedo ayudarte?".format(device.nombres)
        mensaje += "\n por favor cargue una fotografia de su documento de identidad por la parte frontal (foto)"
    else:
        mensaje = "Por favor, ingresa tanto tu nombre como tu apellido."
    return enviar_mensaje(sesion.celular, mensaje)

def procesar_doc_front(request, sesion):
    
    try:
         if request.get("data", {}).get("type") == "image":
            imagen = request.get("data", {}).get("media", {})
            if imagen:
                url_descarga = imagen.get("links", {}).get("download")
                nombre_archivo = imagen.get("filename", "imagen_descargado.pdf")
                extension_archivo = imagen.get("extension", "jpg")
                #return enviar_mensaje(sesion.celular, url_descarga) 
                if url_descarga: 
                    token = 'b07b2841be941d39a85eff31c8c41b4edb2463edceae6e2ffa241557fab5d0175f178b696ab729f9'
                    headers={'Authorization':'Token '+ token}
                    url = "https://api.wassenger.com" + url_descarga
                    response = requests.get(url,headers=headers)
                    directorio = r'C:\Users\devcristian\Downloads\chatbox\wassenger\wassenger\media\pdfs\\'+sesion.id_device + '.' +extension_archivo 
                     #print(settings.MEDIA_URL +str('pdfs/prueba.pdf'))
                    if response.status_code == 200:
                        with open(directorio, 'wb') as file:
                            file.write(response.content)
                            file_url ='http://127.0.0.1:8000'+ settings.MEDIA_URL +str('pdfs/'+ sesion.id_device)
                             #print(file_url)
                            if sesion.estado_solicitud == 4:
                                sesion.estado_solicitud = 5
                                sesion.save()
                                mensaje = "imagen guardada con Exito, para consultar ingrese a: " + file_url + '.' + extension_archivo
                                mensaje += "\n por favor cargue una fotografia de su documento de identidad por la parte posterior (huella)" 
                            else:
                                sesion.estado_solicitud = 6
                                sesion.save()
                                mensaje = "imagen guardada con Exito, para consultar ingrese a: " + file_url + '.' + extension_archivo
                                mensaje += "\n puede realizarel pago a través del siguiente link: \n https://secure.epayco.co/payment/methods?transaction=iET5axQpRPSdRZQAR " 

                            

                    else: 
                        mensaje = "Error al descargar el documento. Código de estado: {response.status_code}"      
                       
                else:
                     mensaje = "URL de descarga no encontrada en el JSON."
            else:
                 mensaje = "Atributos del documento no encontrados en el JSON."
         else:
             mensaje = "El mensaje no es de tipo documento."
         return enviar_mensaje(sesion.celular, mensaje)
    except Exception as e:
         return enviar_mensaje(sesion.celular, "Error general: "+ str(e))
    

def procesar_pago(respuesta_usuario, sesion):
    if respuesta_usuario == "pago":
        radicado = random.randint (10000,100000)
        mensaje= "¡Pago exitoso! Tu solicitud ha sido recibida. Número de radicado:" + str(radicado)
        mensaje += "\n" + "Puede consultar el estado de su sollicitud a través del siguiente link: https://ecommerce.andesscd.com.co/shop"
        mensaje += "\n" + "Desea realizar otra solicitud? 1.SI 2.NO"
        sesion.estado_solicitud = 7
        sesion.save()
    else:
        mensaje = "¡pago en validación! una vez tu pago se confirme te enviaremos un mensaje de manera automatica"
    return enviar_mensaje(sesion.celular, mensaje)

def reintentar(respuesta_usuario, sesion):
    if respuesta_usuario == '1':
        sesion.estado_solicitud = 3
        sesion.save()
        mensaje = "¡Perfecto, para continuar escriba nuevamente el nombre completo!"
    elif respuesta_usuario =='2':
        mensaje = "¡gracias por utilizar nuestros servicios!"
    else:
        mensaje = "Opción incorrecta. Recuerda digitar una opción válida: 1.SI 2.NO"
    return enviar_mensaje(sesion.celular, mensaje)


   




def procesar_tipo_proceso(respuesta_usuario, sesion):
    mensaje = ''
    if respuesta_usuario == '1':
        # Mensaje de aviso de privacidad
        mensaje += "Aviso de privacidad:\n\nEl certificado de persona natural le permite acreditar su identidad y firmar digitalmente sus documentos con la misma validez legal que la firma manuscrita.\n\nPara adquirir un certificado de persona natural NO te solicitaremos documentos siempre y cuando ANDES SCD pueda validar la integridad y confiabilidad de la información, de lo contrario te estaremos informando a través de nuestra plataforma que documentos son necesarios para acreditar dicha información.\n\n"
        # Mensaje con enlace para obtener más información
        mensaje += "Haga clic en el siguiente enlace para obtener más información respecto a la aplicación de los certificados de persona natural a una comunidad, los usos que se le pueden dar a este tipo de certificado y los requerimientos técnicos, legales y de seguridad exigidos para la gestión del ciclo de vida del certificado:\nhttps://www.andesscd.com.co/docs/pc_personanatural.pdf\n\n"
        # Mensaje de términos y condiciones
        mensaje += "Términos y condiciones:\n\nAntes de continuar debes tener en cuenta:\n\n- Debe leer atentamente los términos y condiciones y aceptar nuestras políticas acorde a nuestro aviso de privacidad.\n- Debe tener a la mano los documentos de titular y empresa si es el caso.\n\nAhora puedes consultar nuestros Términos y Condiciones y nuestra Política de Tratamiento de Datos Personales:\nhttps://www.andesscd.com.co/docs/Terminos-y-condiciones-servicios-certificados-digitales.pdf\n\n"
        mensaje += "¿Aceptas los términos y condiciones?\n1. Sí\n2. No"
        status = enviar_mensaje(sesion.celular, mensaje)
        return status
    elif respuesta_usuario == '2':
        # Aquí puedes definir el flujo para la opción 2 (Consultar estado de solicitud)
        pass
    elif respuesta_usuario == '3':
        # Aquí puedes definir el flujo para la opción 3 (Revocar certificado)
        pass
    else:
        mensaje = 'Opción incorrecta. Por favor, elige una opción válida: 1, 2 o 3.'

    # Continuar el flujo después de la respuesta del usuario
    if sesion.estado_solicitud == 5:  # Si se solicitó la foto frontal, enviar mensaje para la foto trasera
        mensaje += " Después de enviar la foto frontal, por favor envía una de la parte trasera."
    else:
        mensaje += " ¿Hay algo más en lo que pueda ayudarte?"

    return enviar_mensaje(sesion.celular, mensaje)


def procesar_mensaje_pago(respuesta_usuario, sesion):
    if sesion.estado_solicitud == 6:  # Verificar si estamos esperando las fotos de la cédula
        # Procesar las fotos de la cédula (aquí debes tener tu lógica para manejar las fotos)
        # Una vez que se procesen las fotos, proceder con el mensaje para el pago
        mensaje_pago = "Para proceder con el pago, por favor haz clic en el siguiente enlace:\nhttps://epayco.com/"
        status_pago = enviar_mensaje(sesion.celular, mensaje_pago)
        # Cambiar el estado de la sesión para esperar confirmación de pago
        sesion.estado_solicitud = 7
        sesion.save()
        return status_pago
    elif sesion.estado_solicitud == 7:  # Verificar si estamos esperando la confirmación de pago
        # Si el usuario ha vuelto del enlace y confirmó el pago, enviar mensaje de confirmación con número de radicado
        numero_radicado = "123456789"  # Número de radicado generado (puedes ajustar esto según tu lógica)
        mensaje_confirmacion = "¡Pago exitoso! Tu solicitud ha sido recibida. Número de radicado: {}".format(numero_radicado)
        status_confirmacion = enviar_mensaje(sesion.celular, mensaje_confirmacion)
        # Cambiar el estado de la sesión para finalizar el proceso
        sesion.estado_solicitud = 8
        sesion.save()
        return status_confirmacion
    else:
        # En caso de que no estemos esperando las fotos de la cédula ni la confirmación de pago, manejar la situación según corresponda
        pass






def procesar_numero_documento(respuesta_usuario, sesion):
     if respuesta_usuario.isdigit() and len(respuesta_usuario) == 10:
         sesion.estado_solicitud = 4
         sesion.save()
         mensaje = 'Gracias por proporcionar tu número. Ahora, por favor, adjunta un documento PDF.'
     else:
         mensaje =  "Respuesta no válida. Por favor, ingresa un número válido de 10 dígitos."
     return enviar_mensaje(sesion.celular, mensaje)

def procesar_documentos(request, sesion):
     try:
         if request.get("data", {}).get("type") == "image":
             documento = request.get("data", {}).get("media", {})
             if documento:
                 url_descarga = documento.get("links", {}).get("download")
                 nombre_archivo = documento.get("filename", "documento_descargado.pdf")
                 #return enviar_mensaje(sesion.celular, url_descarga) 
                 if url_descarga: 
                     token = 'b07b2841be941d39a85eff31c8c41b4edb2463edceae6e2ffa241557fab5d0175f178b696ab729f9'
                     headers={'Authorization':'Token '+ token}
                     url = "https://api.wassenger.com" + url_descarga
                     response = requests.get(url,headers=headers)
                     directorio = r'C:\Users\devcristian\Downloads\chatbox\wassenger\wassenger\media\pdfs\\'+sesion.id_device+'.pdf' 
                     #print(settings.MEDIA_URL +str('pdfs/prueba.pdf'))
                     if response.status_code == 200:
                         with open(directorio, 'wb') as file:
                             file.write(response.content)
                             file_url ='http://127.0.0.1:8000'+ settings.MEDIA_URL +str('pdfs/'+ sesion.id_device)
                             #print(file_url)
                             mensaje = "documento descargado y guardado con Exito, para consultar ingrese a: " + file_url+'.pdf'
                     else: 
                         mensaje = "Error al descargar el documento. Código de estado: {response.status_code}"      
                       
                 else:
                     mensaje = "URL de descarga no encontrada en el JSON."
             else:
                 mensaje = "Atributos del documento no encontrados en el JSON."
         else:
             mensaje = "El mensaje no es de tipo documento."
         return enviar_mensaje(sesion.celular, mensaje)
     except Exception as e:
         return enviar_mensaje(sesion.celular, "Error general: "+ str(e))
   

def tiempo_sesion(sesion):
     if sesion:
         ahora = timezone.now()
         tiempo_transcurrido = ahora - sesion.fecha_actualiza
         if tiempo_transcurrido > timedelta(minutes=55):
             sesion.estado_solicitud = 1
             sesion.save()
             return True
         else:
             return False
     else:
         return False




@csrf_exempt  
def procesar_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            #procesar_mensaje(data)
            sesion_estado(data)
            #return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Error decoding JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)





def es_saludo(data):
    mensaje = data.get("data", {}).get("body", "").lower()
    saludos = ["hola", "buenos días", "buenas tardes", "buenas noches"]
    return any(saludo in mensaje for saludo in saludos)

def es_numero_documento(data):
    numero_documento = data.get("data", {}).get("body", "")
    return numero_documento.isdigit()

def es_respuesta_valida(data):
    respuesta_usuario = data.get("data", {}).get("body", "").lower()
    opciones_validas = ['1', '2', '3']
    return respuesta_usuario in opciones_validas

def es_tipo_documento(data):
    mensaje = data.get("data", {}).get("body", "").lower()
    opciones = ["1", "2", "3"]
    return any(opcion in mensaje for opcion in opciones)






def procesar_tipo_documento(respuesta_usuario, numero_telefono):
    if respuesta_usuario in ['1', '2', '3']:
        if respuesta_usuario == '1':
            enviar_mensaje(numero_telefono, "Perfecto. Ahora, por favor, ingresa tu número.")
        elif respuesta_usuario == '2':
            pass
        elif respuesta_usuario == '3':
            
            pass
    else:
        enviar_mensaje(numero_telefono, "Respuesta no válida. Por favor, selecciona una opción válida ('1', '2' o '3').")

def procesar_mensaje(data):
    numero_telefono = obtener_numero_telefono(data)
    respuesta_usuario = data.get("data", {}).get("body", "").lower()

    if es_saludo(data):
        procesar_saludo_inicial(numero_telefono)
    elif es_respuesta_valida(data):
        if respuesta_usuario == '1':
            procesar_tipo_documento(respuesta_usuario, numero_telefono)
        else:
            
            pass
    elif es_numero_documento(data):
        procesar_numero_documento(respuesta_usuario, numero_telefono)
    else:
        procesar_saludo_inicial(numero_telefono)

def procesar_saludo_inicial(numero_telefono):

    enviar_mensaje(numero_telefono, "Hola Bienvenido a Andes Servicio De Certificación digital. Este canal es para la solicitud de certificados de facturación electrónica digital. En el momento no cuentas con solicitudes pendientes, ¿deseas realizar una? 1. Si 2. No")

def obtener_numero_telefono(data):
    return data.get("device", {}).get("phone", "")

def enviar_mensaje(phone, message):
    print(f"Enviando respuesta a {phone}: {message}")
    
    url = "https://api.wassenger.com/v1/messages"
    payload = {
        "phone": phone,
        "message": message
    }
    headers = {
        "Content-Type": "application/json",
        "Token": "b07b2841be941d39a85eff31c8c41b4edb2463edceae6e2ffa241557fab5d0175f178b696ab729f9"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        return ({'status':'success','status_code': response.status_code, 'response': response.json()})
    except Exception as e:
        return ({'status':'error','status_code': 500, 'error':str(e)})
    

def descargar_documentos(data):
    try:
        if data.get("data", {}).get("type") == "document":
            documento = data.get("media", {})
            if documento:
                url_descarga = documento.get("links", {}).get("download")
                nombre_archivo = documento.get("filename", "documento_descargado.pdf")

                if url_descarga:
                    response = requests.get(url_descarga)
                    if response.status_code == 200:
                        
                        with open(nombre_archivo, 'wb') as file:
                            file.write(response.content)
                        print(f"Documento descargado y guardado como {nombre_archivo}")
                        return JsonResponse({'status': 200, 'message': 'Documento descargado exitosamente'})
                    else:
                        print(f"Error al descargar el documento. Código de estado: {response.status_code}")
                        return JsonResponse({'status': response.status_code, 'message': 'Error al descargar el documento'})
                else:
                    print("URL de descarga no encontrada en el JSON.")
                    return JsonResponse({'status': 400, 'message': 'URL de descarga no encontrada en el JSON'})
            else:
                print("Atributos del documento no encontrados en el JSON.")
                return JsonResponse({'status': 400, 'message': 'Atributos del documento no encontrados en el JSON'})
        else:
            print("El mensaje no es de tipo documento.")
            return JsonResponse({'status': 400, 'message': 'El mensaje no es de tipo documento'})
    except Exception as e:
        print(f"Error general: {str(e)}")
        return JsonResponse({'status': 500, 'message': f'Error general: {str(e)}'})


"""
url = "https://api.wassenger.com/v1/messages"

payload = json.dumps({
  "phone": "+573007623287",
  "message": "Hola Bienvenido a Andes Servcio De Certificación digital. Este canal es para la solicitud de certificados de facturacion electronica digital. En el momento no cuentas con solicitudes pendientes, ¿deseas realizar una ? 1.Si            2.No"
})
headers = {
  'Content-Type': 'application/json',
  'Token': 'a29b02c04809ca1f495c2ca3a9f5429492720ed8313e60921a34c751067ddd3cc268b2b314317a6e'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
"""