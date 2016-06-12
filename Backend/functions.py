from havenondemand.hodclient import *

client = HODClient("921405ad-c2f6-48fb-b8b6-3e9044a5f716", version="v1")


def sentiment_detect(sentence):
    print(sentence)
    params = {'text': sentence}
    response = client.get_request(params, HODApps.ANALYZE_SENTIMENT, async=False)
    # print(response)
    try:
        sentiment_value = response['aggregate']['score']
    except:
        print("Sentiment error")
        sentiment_value = float(0.0)
    print('Sentiment: ' + str(sentiment_value))
    return sentiment_value


def country_extract(location_data):
    params = {'text': location_data, 'entity_type': 'places_eng' }
    response = client.get_request(params, HODApps.ENTITY_EXTRACTION, async=False)
    location = {
        'code': 'IN',
        'label': 'India'
    }
    # print(response)
    try:
        entity = response['entities'][-1]
        loc_code = entity['additional_information']['place_country_code'].encode('utf-8').decode('ascii', 'ignore')
        loc_label = entity['normalized_text'].encode('utf-8').decode('ascii', 'ignore')
        location['code'] = loc_code
        location['label'] = loc_label
    except:
        print('Loc error')
    print(location)
    return location


def concept_extract(headline):
    print(headline)
    params = {'text': headline}
    response = client.get_request(params, HODApps.EXTRACT_CONCEPTS, async=False)
    # print(response)
    concepts = []
    try:
        for entity in response['concepts']:
            concepts.append(entity['concept'].encode('utf-8').decode('ascii', 'ignore'))
    except:
        pass
    print(concepts)
    return concepts


def get_key(item):
    return item[1]