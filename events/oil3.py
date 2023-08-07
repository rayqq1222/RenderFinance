def oil_price():
    url = 'https://www2.moeaboe.gov.tw/oil111/'
    from bs4 import BeautifulSoup
    import requests

    re = requests.get(url)
    soup = BeautifulSoup(re.text, 'lxml')
    #'html.parser'

    list1 = soup.find_all('ul', class_="cont_18")[6]
    #print(list1.prettify())

    items = list1.find_all('li')
    #print(len(items))

    #content=[]
    for item in items:
        title = item.find('div', class_='col-4')
        price = item.find('strong')
        unit = item.find('small')
        content = ('%s%s %s' %(title.text.replace(" ",'').replace('\n\n\n', ''), price.text.replace(" ",'').replace('\n\n', ''), unit.text))
        
    return content