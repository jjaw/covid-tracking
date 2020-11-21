import requests
import json
import matplotlib.pyplot as plt

#script to test OC r not number with data from CovidActNow

apiKey = "0d0c18e9f6894a898708e30eb617ac66"

#fips for Orange County, CA
fips = "06059"

#current data for OC
res_current = requests.get("https://api.covidactnow.org/v2/county/{}.json?apiKey={}".format(fips, apiKey))

#historic data for OC
res = requests.get("https://api.covidactnow.org/v2/county/{}.timeseries.json?apiKey={}".format(fips, apiKey))

metrics = res.json()["metricsTimeseries"]

infectionRate = []
dates = []

for x in metrics:
  #infectionRate is the estimated number of infections arising from a typical case.
  rate = x["infectionRate"]
  date = x["date"]
  infectionRate.append(rate)
  dates.append(date)

y = list(zip(dates, infectionRate))

plt.plot(dates, infectionRate)
plt.show()

def jprint(obj):
  text = json.dumps(obj, sort_keys=True, indent=4)
  print(text)




