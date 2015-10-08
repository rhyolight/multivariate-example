import os
from datetime import date, timedelta
import requests

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
DEBRIS_URL = "http://data.numenta.org/chicago-311/Tree Debris/data.json?aggregate=1 day&since=0"


def fetch_url_and_save(url, filepath):
  if os.path.isfile(filepath):
    print "Skipping: %s" % filepath
    return
  print "Fetching: %s" % url
  response = requests.get(url)
  if response.status_code != 200:
    raise Exception("Got bad status code for last request: %i" 
                    % response.status_code)
  data = response.text
  print "Writing: %s" % filepath
  with open(filepath, "w") as f:
    f.write(data)
    f.close()



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
  fetch_url_and_save(DEBRIS_URL, os.path.join(DATA_DIR, "debris.json"))  



if __name__ == "__main__":
  fetch_debris_data()
  fetch_weather_data()