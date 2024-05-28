from flask import Blueprint, render_template, request
import shodan 
import logging
import os 


logging.basicConfig(filename='app.log', level=logging.INFO)    

#SHODAN_API_KEY = 'hJ4hcLWj7YK3PiIYKqhIaNf0Mw6uGNpQ'
SHODAN_API_KEY = os.environ("SHODAN_API_KEY")
api = shodan.Shodan(SHODAN_API_KEY)

host = Blueprint("search", __name__)

@host.route("/search", methods=['POST'])
def search():
    ip_address = request.form['ip_address']
    range_km = request.form["range"]

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
            'longitude' : result.get('longitude')
        }
        
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
                        'port': result['port'],
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
           
            return render_template('results_geo.html' , message = message, device_info = relevant_info, context = vuln, devices=devices)
        
        else: 
            message = ('Success!')
            
            return render_template('results.html' , message = message, device_info = relevant_info, context = vuln)
    
    except shodan.APIError as e:
        logging.error(e)
        message = str(e)
        return render_template('results.html' , message = message, device_info = dict(), context = dict())
    

