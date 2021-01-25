import asyncio
import sys
import requests
import json

from pywizlight import wizlight, PilotBuilder, PilotParser

async def main():
    room = sys.argv[1]

    # Set up all Wiz bulbs
    wizBulbs = []
    bulb1 = wizlight("ip address")
    bulb2 = wizlight("ip address")
    bulb3 = wizlight("ip address")
    bulb4 = wizlight("ip address")
    bulb5 = wizlight("ip address")
    state = await bulb1.updateState()
    hueGroup = ""

    # Sets up hue group and Wiz lights depending on "room" argument given
    if(room == "vibe"):
        print("vibe room")
        wizBulbs.append(bulb1)
        wizBulbs.append(bulb2)
        hueGroup = 5
    elif(room == "living"):
        print("living room")
        hueGroup = 3
    elif(room == "bed"):
        print("bed room")
        hueGroup = 1
    elif(room == "office"):
        print("office")
        wizBulbs.append(bulb3)
        wizBulbs.append(bulb4)
        wizBulbs.append(bulb5)
    
    # If hue bulbs are present in room, retrieves the hue group and turns it off
    if(hueGroup):
        urlG = f'http://<your bridge ip address>/api/<your hue api key>/groups/{hueGroup}'

        responseG = requests.get(urlG)

        hueLights = json.loads(responseG.text)

        pyPay = {'on': False}

        url = f'http://<your bridge ip address>/api/<your hue api key>/groups/{hueGroup}/action'

        converted = json.dumps(pyPay)

        payload = converted

        response = requests.put(url, payload)

    # Turns off Wiz lights with a bit of a delay to (somewhat) match hue api.(Could be optimsed to be more precise with async func)
    timeout = 20000
    
    for bulb in wizBulbs:
        await asyncio.wait_for(bulb.turn_off(), timeout)

    

loop = asyncio.get_event_loop()
loop.run_until_complete(main())