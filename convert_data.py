import os
import json
import csv
from datetime import date, timedelta, datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
DAYS_BACK = 365 * 2
CACHE_TEMPLATE = "{STATE}-{CITY}-{YYYYMMDD}.json"
STATE = "IL"
CITY = "Chicago"

OUTPUT = "weather_debris_data.csv"


def extract_weather_data(data):
  summary = data["history"]["dailysummary"][0]
  rain = summary["rain"]
  snow = summary["snow"]
  maxwspdm = summary["maxwspdm"]
  precipm = summary["precipm"]
  if precipm == "T": precipm = 0.00
  return dict({
    "rain": rain,
    "snow": snow,
    "maxwspd": maxwspdm,
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
  date_step = now - timedelta(days=DAYS_BACK)

  # Open up the debris JSON and read into a dict.
  with open(debris_file, "r") as df:
    debris_data = json.loads(df.read())

  debris_counts = debris_data["data"]

  # Prime the output
  with open(OUTPUT, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "snow", "rain", "maxwspd", "precip", "debris"])
    writer.writerow(["datetime", "int", "int", "float", "float", "int"])
    writer.writerow(["T", "", "", "", "", ""])

    while date_step < now:
      # Read input weather data for this day.
      date_step = date_step + timedelta(days=1)
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
        debris_date = None
        while len(debris_counts) > 1 and (debris_date is None or debris_date < date_step):
          debris_date, count = pop_date(debris_counts)

        writer.writerow([
          date_step.strftime("%Y-%m-%d"),
          weather["snow"],
          weather["rain"],
          weather["maxwspd"],
          weather["precip"],
          count
        ])



if __name__ == "__main__":
  convert_data()
