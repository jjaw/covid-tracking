import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import os
import errno
from datetime import date
import pprint

#script to chart different metrics of OC data from CovidActNow
def main():
  apiKey = "0d0c18e9f6894a898708e30eb617ac66"

  #fips for Orange County, CA
  fips = "06059"

  #current data for OC
  #res_current = requests.get("https://api.covidactnow.org/v2/county/{}.json?apiKey={}".format(fips, apiKey))

  #historic data for OC
  res = requests.get("https://api.covidactnow.org/v2/county/{}.timeseries.json?apiKey={}".format(fips, apiKey))
  #https://api.covidactnow.org/v2/county/06059.timeseries.json?apiKey=0d0c18e9f6894a898708e30eb617ac66

  #This part has all the metrics collected from the API
  metrics = res.json()["metricsTimeseries"]
  actuals = res.json()["actualsTimeseries"]

  metrics_keys = metrics[0].keys()
  actuals_keys = actuals[0].keys()

  run_data(metrics_keys, metrics)
  run_data(actuals_keys, actuals)

def run_data(keys, data):
  #saves the data from response into a dictionary then plot it
  data = {}
  for key in keys:
    data[key] = list(data[key] for data in data)
  
  for key in keys:
    if data[key][len(data)-14] != None and key != 'date':
      if not isinstance(data[key][0], dict):
        print("Plotted..." + key)
        make_plot(data["date"], data[key], key + " " + str(date.today()))

def make_plot(dates, data_name, title):
  #make the plot title, it, then save it to the chart folder
  plt.figure()
  plt.title(title, fontsize=14, fontweight='bold')
  plt.plot(dates, data_name)
  filename = "chart/" + title + ".png"
  if not os.path.exists(os.path.dirname(filename)):
    try:
       os.makedirs(os.path.dirname(filename))
    except OSError as ex:
      if ex.errno != errno.EEXIST:
        raise
  plt.savefig("chart/" +title + ".png")
  #plt.show()

def jprint(obj):
  text = json.dumps(obj, sort_keys=True, indent=4)
  print(text)

if __name__ == "__main__":
  main()

  """
  plt EXAMPLES:

  plt.figure(1)
  plt.title("Infection Rate", fontsize=14, fontweight='bold')
  plt.plot(dates, infectionRate)
  #saves the figure to an output
  plt.savefig("1.png")
  
  #for subplots on same figure use following blocks of code
  #fig, ax = plt.subplots()
  #ax = ax.plot(dates, infectionRate)
  plt.figure(2)
  plt.title("Infection Rate2", fontsize=14, fontweight='bold')
  plt.plot(dates, infectionRate)
  plt.savefig("2.png")
  plt.show() 
  """

