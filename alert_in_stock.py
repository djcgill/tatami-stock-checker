from bs4 import BeautifulSoup
import requests
import smtplib
import yaml

def load_config():
    with open('config.yml', 'r') as config_file:
        config = yaml.load(config_file)
    return config

def send_email():
    server = smtplib.SMTP(smtp_server)
    server.set_debuglevel(1)
    server.sendmail(from_email, to_email, message)
    server.quit()

def get_stock(store_response, size):
    soup = BeautifulSoup(store_response.content, "html.parser")
    # Element div class="swatch-element a3 soldout" data-value="A3"
    item_stock = soup.find('div',attrs={"class":f"swatch-element {size} available"})
    return item_stock

config = load_config()
from_email = config['email_address']
to_email = config['to_email_address']
smtp_server = config['smtp_server']
size = config['size']

if config['tatami_url'].endswith('/'):
    url = f'{config["tatami_url"]}{config["product"]}'
else:
    url = f'{config["tatami_url"]}/{config["product"]}'

response = requests.get(url, timeout=5)
in_stock = get_stock(response, size)

if in_stock:
    print ("ITEM IN STOCK")
    try:
        send_email()
    except Exception:
        # Send out SMS via twilo
        raise NotImplementedError
else:
    print ('NOT IN STOCK')
