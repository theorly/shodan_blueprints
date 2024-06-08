#qui uso la libreria pyTelegramBotAPI
import telebot
from flask import request, Blueprint, current_app
import logging
import ipaddress
import shodan
import os


shodan_bot = Blueprint('shodan_bot', __name__)
#TODO variabile d'ambiente
bot = telebot.TeleBot("7458903004:AAF6-178ocwCgh4GQvroclS_z-Uznvm5AqQ", parse_mode='HTML')
#SHODAN_API_KEY = 'hJ4hcLWj7YK3PiIYKqhIaNf0Mw6uGNpQ'
SHODAN_API_KEY = os.environ["SHODAN_API_KEY"]
api = shodan.Shodan(SHODAN_API_KEY)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

#################################################################  FUNCTION ##########################################################################
def info() ->str:
    msg="\n\n<b>Usage:</b>\n\n"
    msg+="<b>SHODAN: </b>Shodan is a search engine that allows the user to find the same or different specific types of equipment (routers, servers, etc.) connected to the Internet through a variety of filters.\n"
    msg+="\n<b>Usage examples:</b>\n\n<code>shodan 'ip_address' 'range_km'</code>\n\n<code>shodan 133.242.147.74</code>\n<code>shodan 133.242.147.74 5</code>\n"

    return msg

#TODO da accorpare con il metodo results in search.py
def results(ip_address,range_km) -> str:
    #api = current_app.config['API_SHODAN']
    try:
        # Effettua la ricerca tramite API di Shodan
        result = api.host(ip_address)
        #TODO da togliere
        range_km = "0"
        vuln = {}
        indexes = len(result['data'])

        for i in range(indexes): 
           
            lista_vuln = result['data'][i].keys()
            
            for j in (lista_vuln): 
                if j == 'vulns':
                    for vul in result['data'][i][j]:
                        reference = []
                        for ref in range(len(result['data'][i][j][vul]['references'])):
                            reference.append(result['data'][i][j][vul]['references'][ref])
                        vuln[vul] = [result['data'][i][j][vul]['summary'],result['data'][i][j][vul]['cvss'],reference]
                        
        relevant_info = {
            'ip': result['ip_str'],
            'organization': result.get('org', 'N/A'),
            'os': result.get('os', 'N/A'),
            'country_name' : result['country_name'],
            'city' : result['city'],
            'domains' : result['domains'],
            'ports': result.get('ports', 'N/A'),
            'latitude' : result.get('latitude'),
            'longitude' : result.get('longitude'), 
        }
        relevant_info["vuln"] = vuln

        if range_km != "0":
            latitude = result['latitude']
            longitude = result['longitude']
            results = api.search(f'geo:{latitude},{longitude},{range_km}')
            devices = []
            for result in results['matches']:
                    city = result['location']['city']
                    country_name = result['location']['country_name']
                    _latitude = result['location']['latitude']
                    _longitude = result['location']['longitude']
                
                    device_info = {
                        'ip': result['ip_str'],
                        'ports': result['port'],
                        'organization': result.get('org', 'N/A'),
                        'os': result.get('os', 'N/A'),
                        'vulnerabilities': [],
                        'country_name' : result.get('country_name' , 'N/A'),
                        'city' : city, 
                        'country_name' : country_name,
                        'latitude' : _latitude,
                        'longitude' : _longitude
                    }
                    
                    # Recupera informazioni sulle vulnerabilità, se disponibili
                    if 'vulns' in result:
                        for vulnerability in result['vulns'].keys():
                            
                            device_info['vulnerabilities'].append(vulnerability)

                    devices.append(device_info)
                    
            message = ('Success!')
            relevant_info['near_devices'] = devices
            #writing on cache 
            return (message, relevant_info)
        
        else: 
            message = ('Success!')
            return (message,relevant_info)
    
    except shodan.APIError as e:
        logging.error(e)
        message = str(e)
        return message
###################################################################################################################################################


@bot.message_handler(commands=['start'])
def send_welcome(message):
    with open(f"chat/{message.chat.id}.log", "a") as file:
        file.write(f"{message.from_user.id} - {message.from_user.first_name} {message.from_user.last_name} - {message.text}\n")

    msg = f"Benvenuto {message.from_user.first_name}"
    bot.reply_to(message, msg)


@bot.message_handler(commands=['shodan'])
def send_welcome(message):
    with open(f"chat/{message.chat.id}.log", "a") as file:
        file.write(f"{message.from_user.id} - {message.from_user.first_name} {message.from_user.last_name} - {message.text}\n")

    bot.send_message(message.chat.id, info())


@bot.message_handler(func=lambda m: "shodan" in m.text.lower())
def echo_all(message):
    with open(f"chat/{message.chat.id}.log", "a") as file:
        file.write(f"{message.from_user.id} - {message.from_user.first_name} {message.from_user.last_name} - {message.text}\n")
    arr_msg = message.json['text'].split()
    res = ""

    try:
        #controllo se la stringa ha almeno due parametri, se il primo è shodan e il secondo è un ip
        if len(arr_msg) >= 2 and arr_msg[0].lower() == "shodan" and ipaddress.ip_address(arr_msg[1]):
            #se ha due paramentri sottointendo che il range_km sia = a 0
            if len(arr_msg) == 2:
                res = results(arr_msg[1],"0")
            #se ha 3 paramentri il terzo è il range_km
            elif len(arr_msg) == 3 and arr_msg[2].isdigit():
                res = results(arr_msg[1],arr_msg[2])
            else:
                bot.send_message(message.chat.id, info())
        else:
            bot.send_message(message.chat.id, info())
        
        if res != "":
            msg = f"<b>{res[0]}</b> \nResults of your scan: \nIP = {res[1]['ip']} \nOrganization= {res[1]['organization']} \nPort = {res[1]['ports']} \nCountry name = {res[1]['country_name']} \n"
            msg+= f"City = {res[1]['city']} \nOs = {res[1]['os']} \nDomains = {res[1]['domains']} \nLatitude = {res[1]['latitude']} \nLongitude = {res[1]['longitude']}\n\n <b>ID Vulnerability</b>\n"
            msg+="{"
            for id, elemento in res[1]['vuln'].items():
                msg+= f"{id};"
            msg+="}"
            bot.send_message(message.chat.id, msg)
            bot.send_location(message.chat.id, res[1]['latitude'], res[1]['longitude'])

            bot.send_message(message.chat.id, )
    except ValueError:
        bot.send_message(message.chat.id, "IP ADDRESS DONT'T VALID")
        bot.send_message(message.chat.id, info())



@bot.message_handler(commands=['authors'])
def send_welcome(message):
    with open(f"chat/{message.chat.id}.log", "a") as file:
        file.write(f"{message.from_user.id} - {message.from_user.first_name} {message.from_user.last_name} - {message.text}\n")

    msg = "<b>Authors:</b> Sambu, Pier, Orli\n"
    msg+= "<b>Github:</b> https://github.com/theorly/shodan_blueprints"
    bot.send_message(message.chat.id, msg)



#nel momento che arriva una richiesta dal server telegram
#arriva in questa route, assegnata nel metodo setwebook()
@shodan_bot.route("/webhook", methods=['POST'])
def getMessage():
	json_string = request.get_data().decode('utf-8')
	update = telebot.types.Update.de_json(json_string)
	bot.process_new_updates([update])
	return "!", 200


def set_webhook():
    bot.remove_webhook()
    #TODO variabile d'ambiente
    bot.set_webhook("https://shodanscanning.azurewebsites.net/webhook")
	
    #bot.set_webhook("https://a1cf-137-204-150-22.ngrok-free.app/webhook")
	#https://$shodanscanning:EzXnzQWi2dStdoAvKpusCAv5QlDkemobfMTuGroF9d2gfxthfoRg9pRRoJj3@shodanscanning.scm.azurewebsites.net/api/registry/webhook
	#https://shodanscanning.azurewebsites.net/
	

set_webhook()
#bot.polling()
	