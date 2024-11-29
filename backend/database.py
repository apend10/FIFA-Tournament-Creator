import requests
import json

API_LINK = "https://drop-api.ea.com/rating/fc-24"
# **** FILTERS ****

# positions
goalkeeper = "position=0"

centreback = "position=5"
rightback = "position=3"
leftback = "position=7"

defensive_midfielder = "position=10"
attacking_midfielder = "position=18"
central_midfielder = "position=14"

midfielder = "position=10,14"

leftwing = "position=16,27"
rightwing = "position=12,23"
striker = "position=25"

#gender
male = "gender=0"
female = "gender=1"

#team groups (league)
portugal = "teamGroups=308"
spain = "teamGroups=53"
italy = "teamGroups=31"
germany = "teamGroups=19"
france = "teamGroups=16"
england = "teamGroups=13"


response = requests.get(f"{API_LINK}?{male}&{striker}&{england}")
print(f"{API_LINK}?{male}&{striker}&{england}")
jsonresponse = json.loads(response.text)


for i in range(len(jsonresponse["items"])):
    ratings = str(i) + ")  " + str(jsonresponse["items"][i]["overallRating"]) + " | " + jsonresponse["items"][i]["firstName"] + " " + jsonresponse["items"][i]["lastName"]
    print(ratings)