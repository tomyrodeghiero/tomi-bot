import time
import requests
import sett
import json


def get_message_whatsapp(message):
    if 'type' not in message:
        text = "message not recognized"
        return text
    
    type_message = message['type']
    if type_message == 'text':
        text = message['text']['body']
    elif type_message == "button":
        text = message['button']['text']
    elif type_message == "interactive" and message["interactive"]["type"] == "list_reply":
        text = message["interactive"]["list_reply"]["title"]
    elif type_message == "interactive" and message["interactive"]["type"] == "button_reply":
        text = message["interactive"]["button_reply"]["title"]
    else:
        text = "message not recognized"
    
    return text

def send_message_whatsaap(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + whatsapp_token}
        print("se envía", data)
        response = requests.post(whatsapp_url, headers=headers, data=data)
        
        if response.status_code == 200:
            return "Message sent", 200
        else:
            return "There was an error to send message", response.status_code
    except Exception as e:
        return e, 403
         
def text_message(number, text):
    data = json.dumps({
        "messaging_product": 'whatsapp',
        "recipient_type": "individual",
        "to": number,
        "type": "text",
        "text": {
            "body": text
        }
    })

    return data

def button_reply_message(number, options, body, footer, sedd, messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append({
            "type": "reply",
            "reply": {
                "id": sedd + "_btn_" + str(i+1),
                "title": option
            }
        })
 
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def list_reply_message(number, options, body, footer, sedd, messageId):
    rows = []

    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "View Options",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_message(number, url, caption, messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "url": url,
                "caption": caption,
                "filename": "filename",
            }
        }
    )
    return data

def sticker_message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name, media_type):
    media_id = ""
    if media_type == 'sticker':
        media_id = sett.stickers.get(media_name, None)
    elif media_type == 'image':
        media_id = sett.images.get(media_name, None)
    elif media_type == 'video':
        media_id = sett.videos.get(media_name, None)
    elif media_type == 'audio':
        media_id = sett.audio.get(media_name, None)
    return media_id

def reply_reaction_message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def reply_text_message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "content": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text,
            }
        }
    )
    return data

def mark_read_message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": messageId
        })
    return data

def manage_chatbot(text, number, messageId, name):
    text = text.lower() # message that sent user
    list = []

    if "hola" in text:
        body = "¡Hola! 👋 Bienvenido a Tomi Bot. ¿Cómo podemos ayudarte hoy?"
        footer = "Team Tomi"
        options = ["✅ servicios", "📅 agendar cita"]

        replyButtonData = button_reply_message(number, options, body, footer, "sed1",messageId)
        replyReaction = reply_reaction_message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
    elif "servicios" in text:
        body = "Tenemos varias áreas de consulta para elegir. ¿Cuál de estos servicios te gustaría explorar?"
        footer = "Equipo Tomi"
        options = ["Creación de E-commerce", "Analítica Avanzada", "Inteligencia Artificial para mi Negocio"]

        listReplyData = list_reply_message(number, options, body, footer, "sed2",messageId)
        sticker = sticker_message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)
    elif "Inteligencia Artificicial para mi negocio" in text:
        body = "Buenísima elección. ¿Te gustaría que te enviara un documento PDF con una introducción a nuestros métodos de Inteligencia de Negocio?"
        footer = "Equipo Bigdateros"
        options = ["✅ Sí, envía el PDF.", "⛔ No, gracias"]

        replyButtonData = button_reply_message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)

    elif "Sí, por favor envía el PDF" in text:
        sticker = sticker_message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_message(number,"Genial, por favor espera un momento.")

        send_message_whatsaap(sticker)
        send_message_whatsaap(textMessage)
        time.sleep(3)

        document = document_message(number, sett.document_url, "Listo 👍🏻", "Inteligencia Artificial para mi de Negocio.pdf")
        send_message_whatsaap(document)
        time.sleep(3)

        body = "¿Te gustaría programar una reunión con uno de nuestros especialistas para discutir estos servicios más a fondo?"
        footer = "Equipo Tomi"
        options = ["✅ Sí, agenda reunión", "No, gracias." ]

        replyButtonData = button_reply_message(number, options, body, footer, "sed4",messageId)
        list.append(replyButtonData)
    elif "sí, agenda una reunión" in text :
        body = "Estupendo. Por favor, selecciona una fecha y hora para la reunión:"
        footer = "Equipo Tomi"
        options = ["📅 10: mañana 10:00 AM", "📅 7 de junio, 2:00 PM", "📅 8 de junio, 4:00 PM"]

        listReply = list_reply_message(number, options, body, footer, "sed5", messageId)
        list.append(listReply)
    elif "7 de junio, 2:00 pm" in text:
        body = "Excelente, has seleccionado la reunión para el 7 de junio a las 2:00 PM. Te enviaré un recordatorio un día antes. ¿Necesitas ayuda con algo más hoy?"
        footer = "Equipo Bigdateros"
        options = ["✅ Sí, por favor", "❌ No, gracias."]


        buttonReply = button_reply_message(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
    elif "no, gracias." in text:
        textMessage = text_message(number,"Perfecto! No dudes en contactarnos si tienes más preguntas. Recuerda que también ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😊")
        list.append(textMessage)
    else :
        data = text_message(number,"Lo siento, no entendí lo que dijiste. ¿Quieres que te ayude con alguna de estas opciones?")
        list.append(data)

    for item in list:
        send_message_whatsaap(item)

