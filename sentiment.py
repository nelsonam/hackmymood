import json
import csv
import sys
import os
import requests, urllib

def read_tweets(t_file):
    with open(t_file, 'rb') as ts:
        tweets = []
        reader = csv.reader(ts)
        sents = []
        output = {}
        output['data'] = []
        index = 0
        for t in reader:
            #print t[1]
            index +=1
            print index
            sent = get_text_sentiment(t)
            #print index
            if sent is not None:
                sents.append(sent)
        output['data'] = sents
        with open('data.json', 'w') as outfile:
            json.dump(output, outfile)
            
        print "done!"

def get_weather(tweet):
    base_url = "http://api.wunderground.com/api/"
    call = "/history_"
    date = ""
    loc = "/q/CA/San_Francisco.json"
    api_key = os.environ['wunderground']
    # http://api.wunderground.com/api/d16fe73eabd707fa/history_YYYYMMDD/q/CA/San_Francisco.json
    date = tweet[1]
    date = date[0:4]+date[5:7]+date[8:10]
    weather_url = base_url+api_key+call+date+loc
    results = requests.get(url=weather_url)
    response = results.json()
    rain = response['history']['dailysummary'][0]['rain']
    temp = response['history']['dailysummary'][0]['meantempi']
    return rain, temp 

def get_text_sentiment(tweet):
    alchemy_url = "http://access.alchemyapi.com/calls/text/TextGetTextSentiment"
    
    parameters = {
        "apikey" : os.environ['alchemy']
        "text" : tweet[2],
        "outputMode" : "json",
        "showSourceText" : 1
        }

    try:
        stats = {}
        results = requests.get(url=alchemy_url, params=urllib.urlencode(parameters))
        response = results.json()
        stats['date'] = tweet[1]
        stats['text'] = tweet[2]
        rain, temp = get_weather(tweet)
        stats['weather'] = {}
        stats['weather']['rain'] = rain
        stats['weather']['temp'] = temp
        stats['sentiment'] = response['docSentiment']['type']
        stats['score'] = float(response['docSentiment']['score'])
        return stats
           

    except Exception as e:
        #print "Error while calling TextGetTextSentiment on Tweet (ID %s)" % tweet[0]
        #print "Error:", e
        return None



