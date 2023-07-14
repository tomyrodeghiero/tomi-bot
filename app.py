from flask import Flask, request
import sett
import services

app = Flask(__name__)

@app.route('/welcome', methods=['GET'])
def welcome():
    return 'Hello World from my API on Flask!'

@app.route('/webhook', methods=['GET'])
def validate_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge != None:
            return challenge, 200
        else:
            return 'Invalid token', 403
    except Exception as e:
        return e, 403
    
@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']

        if 'messages' in value and 'contacts' in value:
            message = value['messages'][0]
            number = services.replace_start(str(message['from']))
            number = message['from']
            
            print("Número de teléfono sin modificar:", number)

            number = services.replace_start(str(message['from']))
            print("Número de teléfono modificado:", number)
            
            messageId = message['id']
            contacts = value['contacts'][0]
            name = contacts['profile']['name']
            text = services.get_message_whatsapp(message)

            services.manage_chatbot(text, number, messageId, name)
            return 'enviado'
        else:
            return 'no enviado - falta messages o contacts en value'

    except Exception as e:
        return 'no enviado - excepción: ' + str(e)



if __name__ == '__main__':
    app.run()