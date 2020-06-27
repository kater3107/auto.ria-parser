import parse

# URL = input('Enter URL: ')
URL = 'https://auto.ria.com/newauto/marka-audi/'
HEADERS = {
    'user-agent': 'Chrome/81.0.4044.138',
    'accept': '*/*'

}
HOST = 'https://auto.ria.com'

parse.parse(URL, HEADERS, HOST)
