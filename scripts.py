import requests
import json
import pprint
import urllib
import urllib2
import os #to access secrets.sh
import oauth2
import rauth



# def gmaps_request(search, destination):
#     """requests info about a place using query parameter"""

#     GMAPS_KEY=os.environ['gmaps_key']  #'gmaps_key' from secrets.sh and passing to gmaps_key in url
#     pre_query = search + '+' + destination
#     QUERY = pre_query.replace(' ', '+') 

#     url= 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s' %(QUERY, GMAPS_KEY)

#     api_data = requests.get(url)
#     data = api_data.json()

#     #*******************test*******************
#     pprint.pprint(data, indent=2)
#     # return data #dictionary from json



API_HOST = 'api.yelp.com'
SEARCH_LIMIT = 3
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
TOKEN = os.environ['TOKEN']
TOKEN_SECRET = os.environ['TOKEN_SECRET']


def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    
    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def search(term, location, sort):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """
    
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'sort': sort,
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(term, location, sort):
    """Queries the API by the input values from the user. Uses both the search and get_business function
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    #response is a dictionary where the key is businesses and value is a list of info about the business
    response = search(term, location, sort)
    #*******************test*******************
    # print "here is the response"
    # pprint.pprint(response, indent=2)

    #for each business id, get the data for each business
    id_list = [business['id'] for business in response['businesses']]
    businesses = [get_business(business_id) for business_id in id_list]
    #*******************test*******************
    # print "here are the businesses"
    # pprint.pprint(businesses, indent=2)

    #reformatting each business id results(dictionary) with the info I need in a list comprehension
    businesses = [{'name': business['name'],
                  'address': ' '.join(business['location']['address']),
                  'city': business['location']['city'],
                  'state': business['location']['state_code'],
                  'zipcode': business['location']['postal_code'],
                  'phone': business.get('display_phone'),
                  'id': business['id'],
                  'yelp_url': business['url'], 
                  'rating': business['rating'],
                  'url_rating_stars': business['rating_img_url'],
                  'review_count': business['review_count'],
                  'categories': ', '.join([i[0] for i in business['categories']]),
                  'neighborhoods': ', '.join(business['location'].get('neighborhoods', [])) or None,
                  # getting the key if exists, joining into string
                  # if doesnt exist, set value to empty list
                  # joining an empty list is false, so set value to none (using or)
                  # separated latitude and longitude, does NOT account for non existent coordinates
                  'latitude': business['location']['coordinate']['latitude'],
                  'longitude': business['location']['coordinate']['longitude']} for business in businesses]
    
    #*******************test*******************
    # print "here are the businesses"
    # pprint.pprint(businesses, indent=2)

    return businesses










