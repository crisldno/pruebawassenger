from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from .models import USUARIO, USUARIO_MOVIL
from django.http import HttpResponse
import json
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from urllib.parse import urljoin



@csrf_exempt 
def webhook_handler(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        #response_message = procesar_mensaje(data)
        sesion = sesion_estado(data)
        response = procesar(data, sesion)
        #print("Respuesta generada:", response_message)
        return JsonResponse(response)
    
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def sesion_estado(data):
    mensaje = data.get("data", {})
    usuario = USUARIO.objects.get(id_usuario=1)
    device,creado = USUARIO_MOVIL.objects.get_or_create(id_device=mensaje.get("from", "").lower(), estado = True, defaults={
        'id_usuario':usuario,
        'celular':mensaje.get("fromNumber", "").lower(),
        'estado':True,
        'id_device':mensaje.get("from", "").lower(),
        'estado_solicitud':1
        })     
    
    data = device      
        #print("El registro ya existía.")
    return data
    return serialize('json', [data])


def procesar(request,sesion):
    opcion = sesion.estado_solicitud
    match opcion:
        case 1:
            #bienvenida
            sesion.estado_solicitud = 2
            sesion.save()
            status = enviar_mensaje(sesion.celular, "Hola Bienvenido a Andes Servicio De Certificación digital. Este canal es para la solicitud de certificados de facturación electrónica digital. En el momento no cuentas con solicitudes pendientes, ¿deseas realizar una? 1. Si 2. No")

        case 2:
            #respuesta bienvenida
            status = procesar_respuesta_bienvenida(request.get("data", {}).get("body", "").lower(), sesion)
        case 3:
            #respuesta documento
            status = procesar_numero_documento(request.get("data", {}).get("body", "").lower(), sesion)
        case 4:
            #respuesta .pdf
            status = procesar_documentos(request,sesion)


        case _:

            #no valida    
            print("Opción no válida")

    return status

def procesar_respuesta_bienvenida(respuesta_usuario, sesion):
    if respuesta_usuario == '1':
        sesion.estado_solicitud = 3
        sesion.save()
        #mensaje = 'Seleccione su tipo de documento: 1. Cédula De Ciudadanía. 2. Pasaporte. 3. Cédula De Extranjería.'
        mensaje =  "Perfecto. Ahora, por favor, ingresa tu número de identificacion."
    else:
        mensaje = 'opcion incorrecta, recuerde digitar una opcion valida: 1.SI 2.NO'
    return enviar_mensaje(sesion.celular, mensaje)

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
        if request.get("data", {}).get("type") == "document":
            documento = request.get("data", {}).get("media", {})
            if documento:
                url_descarga = documento.get("links", {}).get("download")
                nombre_archivo = documento.get("filename", "documento_descargado.pdf")
                #return enviar_mensaje(sesion.celular, url_descarga) 
                if url_descarga: 
                    token = '596768a4322d983c72d53a1c1596e19952422069bfc74dfcbaa54e2e125318f3184866cd62163911'
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
        "Token": "596768a4322d983c72d53a1c1596e19952422069bfc74dfcbaa54e2e125318f3184866cd62163911"
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