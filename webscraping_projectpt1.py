from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import keys
from twilio.rest import Client
client = Client(keys.accountSID,keys.authToken)
TwilioNumber = "+18336213062"

myCellPhone = "+17045792295"


webpage = 'https://www.cryptocurrencychart.com/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
req = Request(webpage, headers=headers)

webpage = urlopen(req).read()

soup = BeautifulSoup(webpage, 'html.parser')
print(soup.title.text)

crypto_row = soup.findAll('tr')
crypto_col = soup.findAll('td')


counter = 1
for x in range(5):
    ranking = crypto_col[counter -1].text
    name = crypto_col[counter].text.replace('\n', '').strip()
    price = (crypto_col[counter +1].text)
    the_price = float(price.replace('$','').replace(',','').replace('.',''))
    change = crypto_col[counter +3].text
    print(f"Rank: {ranking}\n Name: {name} \nPrice: {price}\n Percent Change: {change}\n")
    input()
    counter += 11


    if name == 'Ethereum (ETH)' and the_price > 2000:

        price_change = 'Alert!: Ethereum is over $2000!!'
        textmessage = client.messages.create(to=myCellPhone, from_=TwilioNumber, body=price_change)
        print(price_change)
        print(textmessage.status)