import requests
import json
######### ######### ######### ######### ######### ######### ######### 72
''' 
A json file with api-keys is needed in the working directory:
{"apikey_resrobot_stt" : <key ResRobot - Stolptidtabeller 2>,
"apikey_resrobot_rp" : <key ResRobot - Reseplanerare>}
'''
with open("api_keys.json") as keyfile:
    api_keys = json.load(keyfile)

urls = {
    "nearbystops": "https://api.resrobot.se/v2/location.nearbystops",
    "departureboard": "https://api.resrobot.se/v2/departureBoard"
}


def print_departures(id, max=20):
    payload = {
        "key": api_keys["apikey_resrobot_stt"],
        "id": id,
        "maxJourneys": max,
        "format": "json"
    }
    rr = requests.get(urls["departureboard"], params=payload)
    for apa in rr.json()["Departure"]:
        # print(apa)
        print("{}: avg. {} från {} mot {}".format(
            apa["name"], apa["time"], apa["stop"], apa["direction"]))
        stop = apa["Stops"]["Stop"]
        # print(stop[1])
        for st in stop:
            try:
                arrTime = st["arrTime"]
                name = st["name"]
                print(" ank. {:<8} {:<30}".format(arrTime, name))
            except:
                pass
            try:
                depTime = st["depTime"]
                name = st["name"]
                print(" avg. {:<8} {:<30}".format(depTime, name))
            except:
                pass


print_departures(740000008)
