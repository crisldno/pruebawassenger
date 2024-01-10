import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Mensaje

@csrf_exempt
@require_POST
def recibir_mensaje(request):
    print("Recibiendo mensaje...")
    data = json.loads(request.body)

    # Obtener información del mensaje entrante
    phone = data.get('phone')
    message_content = data.get('message')

    # Guardar el mensaje en la base de datos
    nuevo_mensaje = Mensaje(phone=phone, message=message_content)
    nuevo_mensaje.save()

    # Lógica del chatbot para determinar la respuesta
    response_message = procesar_mensaje(message_content)

    # Enviar la respuesta automáticamente
    enviar_respuesta(phone, data['id'], response_message)
    

    return JsonResponse({'status':'ok'})

def procesar_mensaje(message):
    print(f"Mensaje recibido: {message}")
    # Implementa la lógica del chatbot aquí
    # Puedes utilizar condicionales, procesamiento de lenguaje natural (NLP), etc.
    # para determinar la respuesta adecuada
    
    # Ejemplo de una lógica básica
    if "hola" in message.lower():
        return "¡Hola! ¡Bienvenido a tu asistente virtual!"
    elif "información" in message.lower():
        return "Proporcióname más detalles para ayudarte mejor."
    else:
        return "Lo siento, no entendí. ¿Puedes reformular tu mensaje?"

def enviar_respuesta(phone, quote_id, message):
    print(f"Enviando respuesta a {phone}: {message}")
    # Configurar la URL de la API de WhatsApp y los datos de la solicitud
    url = "https://api.wassenger.com/v1/messages"
    payload = {
        "phone": phone,
        "quote": quote_id,
        "message": message
    }
    headers = {
        "Content-Type": "application/json",
        "Token": "1b16187d446e2c1b7b91b27482d2e05be69cb66d36ec58ea5089726808461f8236feed7a279e00ab"
    }

    try:
        # Realizar la solicitud POST a la API de WhatsApp
        response = requests.post(url, headers=headers, json=payload)

        # Devolver la respuesta de la API como JSON (esto es opcional)
        return JsonResponse({'status': response.status_code, 'response': response.json()})
    except Exception as e:
        # En caso de error, devuelve un mensaje de error
        return JsonResponse({'status': 500, 'error': str(e)})
    

