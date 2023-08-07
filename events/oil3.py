def oil_price():
    url = 'https://www2.moeaboe.gov.tw/oil111/'
    from bs4 import BeautifulSoup
    import requests

    re = requests.get(url)
    re.encoding = 'utf-8'
    soup = BeautifulSoup(re.text, 'lxml')
    #'html.parser'

    list1 = soup.find_all('ul', class_="cont_18")[6]
    #print(list1.prettify())

    items = list1.find_all('li')
    #print(len(items))

    content='---本週油價---'
    for item in items:
        title = item.find('div', class_='col-4')
        price = item.find('strong')
        unit = item.find('small')
        result = ('%s%s %s\n' %(title.text.replace(" ",'').replace('\n\n\n', ''), price.text.replace(" ",'').replace('\n\n', ''), unit.text))
        content += result
    return content