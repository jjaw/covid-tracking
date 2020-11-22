import requests
import json
import matplotlib.pyplot as plt
import pandas as pd

#script to test OC r naught number with data from CovidActNow
def main():
  apiKey = "0d0c18e9f6894a898708e30eb617ac66"

  #fips for Orange County, CA
  fips = "06059"

  #current data for OC
  res_current = requests.get("https://api.covidactnow.org/v2/county/{}.json?apiKey={}".format(fips, apiKey))

  #historic data for OC
  res = requests.get("https://api.covidactnow.org/v2/county/{}.timeseries.json?apiKey={}".format(fips, apiKey))
  #https://api.covidactnow.org/v2/county/06059.timeseries.json?apiKey=0d0c18e9f6894a898708e30eb617ac66

  #This part has all the metrics collected from the API
  metrics = res.json()["metricsTimeseries"]
  metrics_keys = metrics[0].keys()

  #df_m = pd.DataFrame(data=metrics)
  
  #set up empty dictionary to store the data
  data = {}
  
  # Need to figure out how to loop through the json and get all the data
  # can probably use 
  # for x, v, in metrics.items():
  
  # put the data in the metrics into one dictionary
  for key in metrics_keys:
    data[key] = list(data[key] for data in metrics)
  
  for key in metrics_keys:
    #we'll get the chart if we have data for it from 2-weeks ago, this might need to be changed later on
    if data[key][len(metrics)-14] != None and key != 'date':
      print("Plotted... " + key)
      make_plot(data["date"], data[key], key)


def make_plot(dates, data_name, title):
  plt.figure()
  plt.title(title, fontsize=14, fontweight='bold')
  plt.plot(dates, data_name)
  plt.savefig(title + ".png")
  plt.show()


  """
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
def jprint(obj):
  text = json.dumps(obj, sort_keys=True, indent=4)
  print(text)

if __name__ == "__main__":
  main()


