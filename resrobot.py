import requests
import json
import xml.etree.ElementTree as ET

'''
######### ######### ######### ######### ######### ######### ######### 72
'''
''' 
A json file with api-keys is needed in the working directory:
{"apikey_resrobot_stt" : <key ResRobot - Stolptidtabeller 2>,
"apikey_resrobot_rp" : <key ResRobot - Reseplanerare>}
'''
with open("api_keys.json") as keyfile:
    api_keys = json.load(keyfile)

urls = {
    "nearbystops": "https://api.resrobot.se/v2/location.nearbystops",
    "departureboard": "https://api.resrobot.se/v2/departureBoard",
    "trip": "https://api.resrobot.se/v2/trip"
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


def print_trip_json(params):
    payload = params.copy()
    payload["format"] = "json"
    payload["key"] = api_keys["apikey_resrobot_rp"]
    rr = requests.get(urls["trip"], params=payload)
    triplist = rr.json()["Trip"]
    for trip in triplist:
        print("Alternativ {}:".format(
            int(trip["idx"]) + 1
        ))
        leglist = trip["LegList"]["Leg"]
        for leg in leglist:
            # print(leg)
            #leg = legcont["Leg"]
            print("  {}.  {} från {} {} till {} {}".format(
                int(leg["idx"]) + 1,
                leg["name"],
                leg["Origin"]["name"],
                leg["Origin"]["time"],
                # leg["direction"],
                leg["Destination"]["name"],
                leg["Destination"]["time"],
            ))

tag_TripList = '{hafas_rest_v1}TripList'
tag_Trip = '{hafas_rest_v1}Trip'
tag_Leg = '{hafas_rest_v1}Leg'
tag_Origin = '{hafas_rest_v1}Origin'
tag_Destination = '{hafas_rest_v1}Destination'

def print_trip_xml(params):
    payload = params.copy()
    payload["format"] = "xml"
    payload["key"] = api_keys["apikey_resrobot_rp"]
    rr = requests.get(urls["trip"], params=payload)
    triplist = ET.fromstring(rr.text)
    if triplist.tag != tag_TripList:
        raise TypeError(
            'XML root is not TripList but {}.'.format(triplist.tag))
    for trip in triplist:
        if trip.tag != tag_Trip:
            raise TypeError('XML root tag is not Trip but {}.'.format(trip.tag))
        print("Alternativ {}:".format(
            int(trip.attrib["idx"]) + 1
        ))
        for leglist in trip:
            for leg in leglist:
                if leg.tag != tag_Leg:
                    raise TypeError('XML tag is not Leg but {}.'.format(trip.tag))
                idx = leg.attrib["idx"]
                name = leg.attrib["name"]
                orig = leg.find(tag_Origin)
                dest = leg.find(tag_Destination)
                print("  {}.  {} från {} {} till {} {}".format(
                    int(idx) + 1,
                    name,
                    orig.attrib["name"],
                    orig.attrib["time"],
                    # leg["direction"],
                    dest.attrib["name"],
                    dest.attrib["time"],
                ))


# print_departures(740000008)
print_trip_xml({
    "originCoordLat": 58.387464,
    "originCoordLong": 13.870660,
    "destCoordLat": 58.384686,
    "destCoordLong": 13.654951
})
