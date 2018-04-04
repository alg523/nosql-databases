import requests

parameters ={'date': '2017-07-20', 'hd': 'False', 'api_key': 'fraC1KpqpUDaWg7eqQKYYvsCTqs4RRjgMz40GrZ1'}
r = requests.get('https://api.nasa.gov/planetary/apod', params=parameters)
url = r.json().get('url')
print(url)
