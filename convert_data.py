import os
import json
import csv
from datetime import date, timedelta, datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
START_DATE = datetime.strptime("2011/01/03", "%Y/%m/%d").date()
CACHE_TEMPLATE = "{STATE}-{CITY}-{YYYYMMDD}.json"
STATE = "IL"
CITY = "Chicago"

OUTPUT = "weather_debris_data.csv"


def extract_weather_data(data):
  summary = data["history"]["dailysummary"][0]
  hail = summary["hail"]
  mintempm = float(summary["mintempm"])
  maxtempm = float(summary["maxtempm"])
  meanwindspdm = summary["meanwindspdm"]
  precipm = summary["precipm"]
  if precipm == "T": precipm = 0.00
  return dict({
    "hail": hail,
    "tempvariation": maxtempm - mintempm,
    "meanwindspdm": meanwindspdm,
    "precip": precipm
  })


def pop_date(debris_counts):
  data_point = debris_counts.pop(0)
  count = data_point[1]
  date_string = data_point[0].split(" ")[0]
  debris_date = datetime.strptime(date_string, "%Y/%m/%d").date()
  return (debris_date, count)


def convert_data():
  debris_file = os.path.join(DATA_DIR, "debris.json")
  now = date.today()
  date_step = START_DATE

  # Open up the debris JSON and read into a dict.
  with open(debris_file, "r") as df:
    debris_data = json.loads(df.read())

  debris_counts = debris_data["data"]

  # Prime the output
  with open(OUTPUT, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "tempvariation", "hail", "meanwindspdm", "precip", "debris"])
    writer.writerow(["datetime", "float", "int", "float", "float", "int"])
    writer.writerow(["T", "", "", "", "", ""])

    while date_step < now:
      # Read input weather data for this day.
      date_string = date_step.strftime("%Y%m%d")
      filename = CACHE_TEMPLATE.replace("{YYYYMMDD}", date_string) \
                               .replace("{STATE}", STATE) \
                               .replace("{CITY}", CITY)
      filepath = os.path.join(DATA_DIR, filename)
      if os.path.isfile(filepath):
        with open(filepath, "r") as weather_file:
          weather_data = json.loads(weather_file.read())
        weather = extract_weather_data(weather_data)
        # Get input debris call count for this day by stepping through the data
        # until we get to the right day.
        if len(debris_counts) == 0: break
        debris_date, count = pop_date(debris_counts)
        while debris_date < date_step:
          debris_date, count = pop_date(debris_counts)
          
        writer.writerow([
          date_step.strftime("%Y-%m-%d"),
          weather["tempvariation"],
          weather["hail"],
          weather["meanwindspdm"],
          weather["precip"],
          count
        ])
      date_step = date_step + timedelta(days=1)



if __name__ == "__main__":
  convert_data()
