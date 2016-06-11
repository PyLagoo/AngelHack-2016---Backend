from flask import Flask
# from flask_oauthlib.client import OAuth
import twitter
from havenondemand.hodclient import *

app = Flask(__name__)

api = twitter.Api(
    consumer_key='7jbKM37yIz9pPNAsVwktacerc',
    consumer_secret='iEGbqG5fNHyJSsMLuJzib27lj7lI7CIiBtbC3YiT6Z17eU0XFe',
    access_token_key='47313714-VnLZ0lFKLxQbewnxskwDB6Zbj4VnF0Fq6rbrjPqPI',
    access_token_secret='HJuA4JBGOfFy7dZRVDQihw1l7dnkxVsNpOfer8YjZ0SZ9'
)

client = HODClient("921405ad-c2f6-48fb-b8b6-3e9044a5f716", version="v1")

@app.route('/')
def hello_world():
    return 'Hello World!'

def sentiment_detect(sentence):
    params = {'text': sentence}
    response = client.get_request(params, HODApps.ANALYZE_SENTIMENT, async=False)
    #print(response)
    sentiment_value = response['aggregate']['score']
    #print(sentiment_value)
    return sentiment_value

def country_extract(location_data="India"):
    params = {'text': location_data, 'entity_type': 'places_eng' }


    response = client.get_request(params, HODApps.ENTITY_EXTRACTION, async=False)
    #print(response)

    if len(response['entities'])>0:
        country_code = response['entities'][0]['additional_information']['place_country_code']
        country_name = response['entities'][0]['original_text']
        #print(country_code)
        #print(country_name)

    else:
        country_code = "IN"
        country_name = "India"

    return country_code, country_name


@app.route('/search/<query>')
def search_query(query):
    query_string = ''
    query_params = query.split('?')
    term = None
    since = None
    until = None

    for param in query_params:
        # Search with this keyword
        param = param.split('=')
        value = param[1]
        param = param[0]
        if param == 'keyword':
            term = value
        # Time period start
        elif param == 'start':
            since = value
        # Time period end
        elif param == 'until':
            until = value

        tweets = api.GetSearch(term=term, since=since, until=until, count=200)


if __name__ == '__main__':
    app.run()
