import requests
import json
import pandas as pd

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

def filter(selected_positions:list):
    position_abbreviation_full_form_conversion = {
        "GK" : "0",
        "LB" : "7",
        "RB" : "3",
        "CB" : "5",
        "CDM" : "10",
        "CM" : "14",
        "CAM" : "18",
        "LM" : "16",
        "RM" : "12",
        "LW" : "27",
        "RW" : "23",
        "ST" : "25"
    }

    selected_positions_str = ""
    for i in range(len(selected_positions)):
        selected_positions_str += position_abbreviation_full_form_conversion[selected_positions[i]]
        if i != len(selected_positions) - 1:
           selected_positions_str += ","

    response = requests.get(f"{API_LINK}?position={selected_positions_str}&{male}")
    print(f"{API_LINK}?position={selected_positions_str}&{male}")
    jsonresponse = json.loads(response.text)
    
    overallRating = []
    name = []
    for i in range(len(jsonresponse["items"])):
      overallRating.append(jsonresponse["items"][i]["overallRating"])
      name.append(jsonresponse["items"][i]["firstName"] + " " + jsonresponse["items"][i]["lastName"])
      ratings = str(i) + ")  " + str(jsonresponse["items"][i]["overallRating"]) + " | " + jsonresponse["items"][i]["firstName"] + " " + jsonresponse["items"][i]["lastName"]
      print(ratings)
    
    result = pd.DataFrame({
       "Name" : name, 
       "Rating" : overallRating
    })

    return result

filter(["ST"])
# ENDPOINT TESTING CODE
# response = requests.get(f"{API_LINK}?position=23&{male}")
# jsonresponse = json.loads(response.text)


# for i in range(len(jsonresponse["items"])):
#     ratings = str(i) + ")  " + str(jsonresponse["items"][i]["overallRating"]) + " | " + jsonresponse["items"][i]["firstName"] + " " + jsonresponse["items"][i]["lastName"]
#     print(ratings)