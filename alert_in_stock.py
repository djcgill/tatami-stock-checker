from bs4 import BeautifulSoup
import requests
import smtplib

def send_email():
    email_address = ""
    password = ""
    message = """
                BLACK NOVA GI ON TATAMI FIGHTWEAR IS IN STOCK
                https://www.tatamifightwear.com/collections/bjj-gi/products/nova-mk4-black
              """
    server = smtplib.SMTP('smtp.gmail.com')
    server.set_debuglevel(1)
    server.sendmail(email_address, email_address, message)
    server.quit()

def get_stock(store_response):
    soup = BeautifulSoup(store_response.content, "html.parser")
    # Element div class="swatch-element a3 soldout" data-value="A3"
    item_stock = soup.find('div',attrs={"class":"swatch-element a3 available"})
    return item_stock

url = "https://www.tatamifightwear.com/collections/bjj-gi/products/nova-mk4-black"
response = requests.get(url, timeout=5)
in_stock = get_stock(response)

if in_stock:
    print ("ITEM IN STOCK")
    try:
        send_email()
    except Exception:
        # Send out SMS via twilo
        raise NotImplementedError
else:
    print ('NOT IN STOCK')
