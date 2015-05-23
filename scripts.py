import requests
import json
import os #to access secrets.sh
GMAPS_KEY=os.environ['gmaps_key'] #'gmaps_key' from secrets.sh and passing to gmaps_key in url


def gmaps_request(search, destination):
    """requests info about a place using query parameter"""

    pre_query = search + '+' + destination
    QUERY = pre_query.replace(' ', '+') 

    url= 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s' %(QUERY, GMAPS_KEY)

    api_data = requests.get(url)
    data = api_data.json()
    return data #dictionary from json




 
