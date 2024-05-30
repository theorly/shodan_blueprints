from flask import Blueprint, render_template, request
import shodan 
import logging
import os 
from prometheus_client import Counter, REGISTRY, generate_latest, CONTENT_TYPE_LATEST
from prometheus_flask_exporter import PrometheusMetrics


REQUEST_COUNT_SEARCH = Counter('http_requests_total_alert', 'Total HTTP Requests', ['method', 'endpoint'])
metrics = PrometheusMetrics.for_app_factory()

#logging.basicConfig(filename='app.log', level=logging.INFO) 
logging.basicConfig(level=logging.INFO)    

#SHODAN_API_KEY = os.environ["SHODAN_API_KEY"]
SHODAN_API_KEY = 'hJ4hcLWj7YK3PiIYKqhIaNf0Mw6uGNpQ'

api = shodan.Shodan(SHODAN_API_KEY)

alert = Blueprint("alert", __name__)


@alert.route('/create_alert', methods=['POST']) 
@metrics.counter('create_alert_requests', 'Number of requests to the create_alert endpoint')
def create_alert(): 
      
    if request.method == 'POST': 
        name = request.form['name'] 
        net = request.form['net'] 
        expires = int(request.form['expires']) 
        trigger = request.form['trigger']
        logging.info("Resolved name-net-expires from the index page.")
        try: 
                alert = api.create_alert(name, net, expires=expires) 
                # add the alert to the trigger
                trigger = trigger.split(', ')
               
                print("TRIGGER:",trigger)
                for tri in trigger:
                    triggers = api.enable_alert_trigger(aid=alert['id'], trigger=tri)
        
                # print the alert status
                message = api.alerts(aid=alert['id'])
    
                return render_template('create_alert.html', message=message, name = name, net = net, expires=expires)
                
        except shodan.APIError as e: 
                logging.error(e)
                error = str(e)
                return render_template('create_alert.html', message=error, name = name, net = net, expires=expires)


@alert.route('/delete_alert', methods=['POST']) 
@metrics.counter('delete_alert_requests', 'Number of requests to the delete_alert endpoint')
def delete_alert(): 

    if request.method == 'POST': 
        name = request.form['name_delete'] 
        logging.info("Resolved AlertID to remove.")
        try: 
            api.delete_alert(aid=name)
            message = (f"Alert '{name}' distrutto con successo.\n")
            return render_template('delete_alert.html', message=message, name = name)
                
        except shodan.APIError as e: 
                logging.error(e)
                return render_template('delete_alert.html', message=str(e), name = name)


@alert.route('/alert_list', methods=['POST']) 
@metrics.counter('alert_list_requests', 'Number of requests to the alert_list endpoint')
def list(): 
    
    alerts = api.alerts()
    logging.info("Resolved alert lists.")
    lista = []
    for i in (alerts): 
        alert_list = {
            'name' : i['name'],
            'triggers' : i['triggers'],
            'expires' : i['expires'],
            'id' : i['id'],
            'ip' : i['filters']['ip']
        } 
        lista.append(alert_list)     
    
    return render_template('alert_list.html',  info = lista)
