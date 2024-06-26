from flask import Blueprint, render_template, request, current_app
from flask_login import current_user
import shodan 
import logging
import os 
import redis 
from prometheus_client import Counter, REGISTRY, generate_latest, CONTENT_TYPE_LATEST
from prometheus_flask_exporter import PrometheusMetrics

import json
from . import db
from app.models import HistoryIp

REQUEST_COUNT_SEARCH = Counter('http_requests_total_search', 'Total HTTP Requests', ['method', 'endpoint'])
metrics = PrometheusMetrics.for_app_factory()

redis_host = os.environ["REDIS_HOST"]  # Sostituisci con l'indirizzo host
redis_port = os.environ["REDIS_PORT"]  # Porta Redis standard
redis_psw = os.environ["REDIS_PSW"]

logging.basicConfig(level=logging.INFO)    

try:
    redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_psw, ssl=False)
    logging.info("Connected to Redis server successfully!")
except redis.exceptions.AuthenticationError as e:
    logging.error(e)


host = Blueprint("search", __name__)

@host.route("/search", methods=['POST'])
@metrics.counter('search_requests', 'Number of requests to the search endpoint')
def search():
    api = current_app.config['API_SHODAN']
    ip_address = request.form['ip_address']
    range_km = request.form["range"]

    if current_user.is_authenticated:
        emailUser = current_user.email
        new_historyIp = HistoryIp(ip=ip_address, emailUser=emailUser, range=range_km)

        # add the new historyIp to the database
        db.session.add(new_historyIp)
        db.session.commit()

    
    if redis_client.exists(ip_address):
        message = "Retrieved from RedisCache!"
        retrieved_info =  json.loads(redis_client.get(ip_address))
        logging.info(f"retrieved from cache {ip_address} successfull!!")
        return render_template('results.html' , message = message, device_info = retrieved_info)
    
    elif redis_client.exists(ranged_value:=str(ip_address + '_' +range_km)):
        message = "Retrieved from RedisCache!"
        retrieved_info =  json.loads(redis_client.get(ip_address))
        logging.info(f"retrieved from cache {ranged_value} successfull!!")
        return render_template('results_geo.html' , message = message, device_info = retrieved_info)
    
    logging.info("Resolved ip_address and range from the index.html")
    
    try:
        # Effettua la ricerca tramite API di Shodan
        result = api.host(ip_address)
        
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
            logging.info("Trying to write on cache the result. \n")
            relevant_info_json = json.dumps(relevant_info)
            redis_client.set(f"{ip_address}_{range_km}", relevant_info_json)
            logging.info("Wirting on cache successful! \n")
            return render_template('results_geo.html' , message = message, device_info = relevant_info)
        
        else: 
            message = ('Success!')
            logging.info("Trying to write on cache the result. \n")
            relevant_info_json = json.dumps(relevant_info)
            redis_client.set(f"{ip_address}", relevant_info_json)
            logging.info("Wirting on cache successful! \n")
            return render_template('results.html' , message = message, device_info = relevant_info)
    
    except shodan.APIError as e:
        logging.error(e)
        message = str(e)
        return render_template('results.html' , message = message, device_info = dict(), context = dict())
    




