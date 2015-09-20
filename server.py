from spyre import server
from sentiment import read_tweets
import json
import pandas as pd
from pandas.io.json import json_normalize

class MyMood(server.App):
    title = "Hack My Mood"
    inputs = [{"type":"text",
               "key":"username",
               "label":"Enter your Twitter username here",
               "value":"",
               "action_id":"update_data"}]

    outputs = [{"type":"html",
                "id":"home",
                "control_id":"update_data",
                "tab":"Home"},
               {"type":"table",
                "id":"table_id",
                "control_id":"update_data",
                "tab":"Table",
                "on_page_load":False},
               {"type":"plot",
                "id":"plot_id",
                "control_id":"update_data",
                "tab":"Plot",
                "on_page_load":False}]

    controls = [{ "type" : "hidden",
                  "id" : "update_data"}]

    tabs = {"Home", "Table", "Plot"}

    def getHTML(self, params):
        name = params["username"]
        return "<h3>%s,</h3><p>You've taken the first step to better mental health. Awareness of mood fluctuations is key to understanding them." % name

    def getPlot(self, params):
       with open('data.json', 'r') as jfile:
           data = json.load(jfile)
           df = pd.DataFrame.from_records(data)
           df = json_normalize(df['data'])
           df['date'] = df['date'].str[:-8]
           df['date'] = pd.to_datetime(df['date'])
           df = df.convert_objects(convert_numeric=True)
           ts = pd.Series(df['score'])
           plotthing = ts.plot(figsize=(50,10))
           fig = plotthing.get_figure()
           return fig

    def getTable(self, params):
        name = params["username"]
        # read data.json
        
        with open('data.json', 'r') as jfile:
            data = json.load(jfile)
            df = pd.DataFrame.from_records(data)
            df = json_normalize(df['data'])  
            df['date'] = df['date'].str[:-8]
            return df
        

app = MyMood()
app.launch(port=9999)
