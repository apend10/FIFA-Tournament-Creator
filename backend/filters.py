import requests
import json

API_LINK = "https://drop-api.ea.com/rating/fc-24/filters"

response = requests.get(f"{API_LINK}")
jsonresponse = json.loads(response.text)

#print(jsonresponse["teamGroups"])

length = len(jsonresponse["teamGroups"]) #57 total leagues
print(length)

print("-------------------------")
leagues = []
for i in range(length):
    #if jsonresponse["teamGroups"][i]['teams'][0]['isPopular'] == "True":
        print("LEAGUE:")
        league_name = jsonresponse["teamGroups"][i]['label']
        print(jsonresponse["teamGroups"][i]['label'])
        leagues.append(jsonresponse["teamGroups"][i]['label'])
        #print(jsonresponse["teamGroups"][i]['teams'])
        print("_________________________________")

print(leagues)

