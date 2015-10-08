import os
from datetime import date, timedelta
import requests
import json

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

# Wunderground data
API_KEY = os.environ["WUNDERGROUND_API_KEY"]
URL_TEMPLATE = "http://api.wunderground.com/api/{API_KEY}/history_{YYYYMMDD}/q/{STATE}/{CITY}.json"
CACHE_TEMPLATE = "{STATE}-{CITY}-{YYYYMMDD}.json"
STATE = "IL"
CITY = "Chicago"
# STATE = "OR"
# CITY = "Portland"

# River View data
DEBRIS_2011 = "http://data.numenta.org/chicago-311/Tree Debris/data.json?aggregate=1 day&since=1293868800&until=1325404800"
DEBRIS_2012 = "http://data.numenta.org/chicago-311/Tree Debris/data.json?aggregate=1 day&since=1325404800&until=1357027200"
DEBRIS_2013 = "http://data.numenta.org/chicago-311/Tree Debris/data.json?aggregate=1 day&since=1357027200&until=1388563200"
DEBRIS_2014 = "http://data.numenta.org/chicago-311/Tree Debris/data.json?aggregate=1 day&since=1388563200&until=1420099200"
DEBRIS_2015 = "http://data.numenta.org/chicago-311/Tree Debris/data.json?aggregate=1 day&since=1420099200"



def save_to_file(data, filepath):
  print "Writing: %s" % filepath
  with open(filepath, "w") as f:
    f.write(data)
    f.close()



def fetch_url(url):
  print "Fetching: %s" % url
  response = requests.get(url)
  if response.status_code != 200:
    raise Exception("Got bad status code for last request: %i"
                    % response.status_code)
  data = response.text
  return data


def fetch_url_and_save(url, filepath):
  if os.path.isfile(filepath):
    print "Skipping: %s" % filepath
    return
  data = fetch_url(url)
  save_to_file(data, filepath)



def fetch_weather_data():
  day = date.today()
  while True:
    # Move back one day
    day = day - timedelta(days=1)
    date_string = day.strftime("%Y%m%d")
    url = URL_TEMPLATE.replace("{API_KEY}", API_KEY) \
                      .replace("{YYYYMMDD}", date_string) \
                      .replace("{STATE}", STATE) \
                      .replace("{CITY}", CITY)
    filename = CACHE_TEMPLATE.replace("{YYYYMMDD}", date_string) \
                             .replace("{STATE}", STATE) \
                             .replace("{CITY}", CITY)
    filepath = os.path.join(DATA_DIR, filename)
    fetch_url_and_save(url, filepath)



def fetch_debris_data():
  debris_2011 = json.loads(fetch_url(DEBRIS_2011))
  debris_2012 = json.loads(fetch_url(DEBRIS_2012))
  debris_2013 = json.loads(fetch_url(DEBRIS_2013))
  debris_2014 = json.loads(fetch_url(DEBRIS_2014))
  debris_2015 = json.loads(fetch_url(DEBRIS_2015))
  
  debris_2011["data"] = debris_2011["data"] + debris_2011["data"] 
  debris_2011["data"] = debris_2011["data"] + debris_2012["data"] 
  debris_2011["data"] = debris_2011["data"] + debris_2013["data"] 
  debris_2011["data"] = debris_2011["data"] + debris_2014["data"] 
  debris_2011["data"] = debris_2011["data"] + debris_2015["data"] 
  
  save_to_file(json.dumps(debris_2011), os.path.join(DATA_DIR, "debris.json"))
    



if __name__ == "__main__":
  fetch_debris_data()
  fetch_weather_data()