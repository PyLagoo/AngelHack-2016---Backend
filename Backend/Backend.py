from flask import Flask
# from flask_oauthlib.client import OAuth
import twitter

app = Flask(__name__)

api = twitter.Api(
    consumer_key='7jbKM37yIz9pPNAsVwktacerc',
    consumer_secret='iEGbqG5fNHyJSsMLuJzib27lj7lI7CIiBtbC3YiT6Z17eU0XFe',
    access_token_key='47313714-VnLZ0lFKLxQbewnxskwDB6Zbj4VnF0Fq6rbrjPqPI',
    access_token_secret='HJuA4JBGOfFy7dZRVDQihw1l7dnkxVsNpOfer8YjZ0SZ9'
)

@app.route('/')
def hello_world():
    return 'Hello World!'

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
