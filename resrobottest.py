import requests
import json

''' 
A json file with api-keys is needed in the working directory:
{"apikey_resrobot_stt" : <key ResRobot - Stolptidtabeller 2>,
"apikey_resrobot_rp" : <key ResRobot - Reseplanerare>}
'''
with open("api_keys.json") as keyfile:
    api_keys = json.load(keyfile)

urls = {
    "nearbystops" : "https://api.resrobot.se/v2/location.nearbystops",
    "departureboard" : "https://api.resrobot.se/v2/departureBoard" 
}

payload_test = {
    "key" : api_keys["apikey_resrobot_rp"],
    "originCoordLat" : 58.387,
    "originCoordLong" : 13.871,
    "format" : "json"
}

payload_test["originCoordLat"] =  58.389216
payload_test["originCoordLong"] = 13.851925
payload_test_db = {
    "key" : api_keys["apikey_resrobot_stt"],
    "id" : 0,
    "maxJourneys" : 50,
    "format" : "json"
}

r = requests.get(urls["nearbystops"], params=payload_test)
#print(type(r), type(r.json), '\n', r.json(), '\n', r.text)

rjson = r.json()
stoplocation = rjson["StopLocation"]
'''
for a in stoplocation:
    for b in a:
        print(b, a[b])
    payload_test_db["id"] = a["id"]
    rr = requests.get(urls["departureboard"], params = payload_test_db)
    print(rr.json())
    '''

payload_test_db["id"] = "740000008"

rr = requests.get(urls["departureboard"], params = payload_test_db)
#print(rr.json())
for apa in rr.json()["Departure"]:
    #print(apa)
    print("{:<30} avg. {:<8} mot {:<30}".format(apa["name"], apa["time"], apa["direction"]))
    stop = apa["Stops"]["Stop"]
    #print(stop[1])
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




