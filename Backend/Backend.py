from flask import Flask, render_template
import twitter
from functions import *
from statistics import mean
import feedparser

app = Flask(__name__)

api = twitter.Api(
)

TWEET_COUNT = 3


@app.route('/')
def hello_world():
    # return 'Hi'
    trends = api.GetTrendsCurrent()
    tweets = []
    temp = {}
    hl_keys = set()
    rss = feedparser.parse('http://rss.cnn.com/rss/edition_world.rss')
    headlines = [item['title'] for item in rss['items']]
    for headline in headlines[:3]:
        for concept in concept_extract(headline):
            hl_keys.add(concept)
    for trend in trends[:2]:
        trend = trend.name.encode('utf=8').decode('utf-8', 'ignore').replace('#', '')
        trend = trend.strip()
        print(trend)
        tweets = api.GetSearch(term=trend, lang='en', count=TWEET_COUNT)
        for tweet in tweets:
            text = tweet.text.encode('utf=8').decode('ascii', 'ignore')
            sentiment = sentiment_detect(tweet.text.encode('utf-8').decode('ascii', 'ignore'))
            location = tweet.user.location
            if not location or location == 'Global':
                location = {
                    'code': 'IN',
                    'label': 'India'
                }
            else:
                location = country_extract(location)
            loc_code = location['code']
            if loc_code not in list(temp.keys()):
                temp[loc_code] = {}
            if 'trends' not in list(temp[loc_code].keys()):
                temp[loc_code]['trends'] = {}
            temp[loc_code]['name'] = location['label']
            if trend not in list(temp[loc_code]['trends'].keys()):
                temp[loc_code]['trends'][trend] = []
            temp[loc_code]['trends'][trend].append(sentiment)

    i = 0
    for hl_key in hl_keys:
        i += 1
        if i == 3:
            break
        tweets = api.GetSearch(term=hl_key, lang='en', count=TWEET_COUNT)
        for tweet in tweets:
            text = tweet.text.encode('utf=8').decode('ascii', 'ignore')
            # print(text)
            # print('HAHAHAHAHAHAHA')
            sentiment = sentiment_detect(tweet.text.encode('utf-8').decode('ascii', 'ignore'))
            location = tweet.user.location
            if not location or location == 'Global':
                location = {
                    'code': 'IN',
                    'label': 'India'
                }
            else:
                location = country_extract(location)
            loc_code = location['code']
            if loc_code not in list(temp.keys()):
                temp[loc_code] = {}
            if 'trends' not in list(temp[loc_code].keys()):
                temp[loc_code]['trends'] = {}
            temp[loc_code]['name'] = location['label']
            if trend not in list(temp[loc_code]['trends'].keys()):
                temp[loc_code]['trends'][trend] = []
            temp[loc_code]['trends'][trend].append(sentiment)


    map_output = []
    for k1 in temp:
        sentiments = []
        for k2 in temp[k1]['trends']:
            i += 1
            temp[k1]['trends'][k2] = mean(temp[k1]['trends'][k2])
            sentiments.append(temp[k1]['trends'][k2])

        map_output.append({
            'value': mean(sentiments),
            'code': k1,
            'name': temp[k1]['name']
        })

    return render_template('search.html', output={
        'map': map_output,
        'loc': temp
    })


@app.route('/search/<query>')
def search_query(query):
    # return query
    query_params = query.split('_')
    # print(query_params)
    # return 'Hi'
    term = None
    since = None
    until = None

    for param in query_params:
        # Search with this keyword
        try:
            param = param.split('=')
            value = param[1]
            param = param[0]
        except:
            continue
        if param == 'keyword':
            term = value
        # Time period start
        elif param == 'start':
            since = value
        # Time period end
        elif param == 'until':
            until = value

    map_output = []
    loc_sentiments = {}
    tweet_sentiment = []
    tweets = api.GetSearch(term=term, since=since, until=until, count=200, lang='en')
    for tweet in tweets:
        sentiment = sentiment_detect(tweet.text.encode('utf-8').decode('ascii', 'ignore'))
        location = tweet.user.location
        if not location or location == 'Global':
            location = {
                'code': 'IN',
                'label': 'India'
            }
        else:
            location = country_extract(location)
        if location['code'] in loc_sentiments:
            loc_sentiments[location['code']].append(sentiment)
        else:
            loc_sentiments[location['code']] = [sentiment]
        tweet_sentiment.append((tweet.text.encode('utf-8').decode('ascii', 'ignore'), sentiment))
    tweet_list = []
    for key in loc_sentiments:
        loc_sentiments[key] = mean(loc_sentiments[key])
        map_output.append({
            'code': key,
            'value': loc_sentiments[key],
            'name': term
        })

    mu = mean([loc_sentiments[key] for key in loc_sentiments])
    for i in range(len(tweet_sentiment)):
        tweet_sentiment[i] = (tweet_sentiment[i][0], (tweet_sentiment[i][1]-mu)**2)
    tweet_sentiment = sorted(tweet_sentiment, key=get_key)
    if len(tweet_sentiment) > 5:
        tweet_sentiment = tweet_sentiment[:5]

    tweet_sentiment = [tweet for (tweet, s) in tweet_sentiment]

    output = {
        'tweets': tweet_sentiment,
        'map_data': map_output
    }

    return render_template('search.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)

