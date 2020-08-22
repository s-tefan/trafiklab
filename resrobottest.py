import requests

apikey_resrobot_stt = "093f4e3c-ae12-4109-9265-3e596f3161f8"
apikey_resrobot_rp = "1ce32405-db7a-4a4d-9a45-7e3a04dd916e"

urls = {
    "nearbystops" : "https://api.resrobot.se/v2/location.nearbystops",
    "departureboard" : "https://api.resrobot.se/v2/departureBoard" 
}

payload_test = {
    "key" : apikey_resrobot_rp,
    "originCoordLat" : 58.387,
    "originCoordLong" : 13.871,
    "format" : "json"
}

payload_test["originCoordLat"] =  58.389216
payload_test["originCoordLong"] = 13.851925
payload_test_db = {
    "key" : apikey_resrobot_stt,
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
print(rr.json())
for apa in rr.json()["Departure"]:
    print(apa["name"], apa["time"])