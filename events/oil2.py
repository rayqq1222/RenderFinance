import requests
from bs4 import BeautifulSoup

def oil_price():
    target_url = 'https://www.cpc.com.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    title1 = soup.find('h2.elementor-heading-title elementor-size-default b').text
    title2 = soup.select
    title3 = soup.select
    #gas_price = soup.select('#gas-price')[0].text.replace('\n\n\n', '').replace(' ', '')
    #cpc = soup.select('#cpc')[0].text.replace(' ', '')
    content = '{}\n{}{}'.format(title)
    return content