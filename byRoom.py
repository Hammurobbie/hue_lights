import asyncio
import sys
import requests
import json

from pywizlight import wizlight, PilotBuilder, PilotParser

async def main():
    # this code expects at least one argument, room. Scene and brightness are optional 
    room = sys.argv[1]
    if len(sys.argv) > 2:
        scene = sys.argv[2]
    else:
        scene = ""
    if len(sys.argv) > 3:
        bright = sys.argv[3]
    else:
        bright = ""
    
    # Set up all Wiz bulbs
    wizBulbs = []
    bulb1 = wizlight("<ip_address>")
    bulb2 = wizlight("<ip_address>")
    bulb3 = wizlight("<ip_address>")
    bulb4 = wizlight("<ip_address>")
    bulb5 = wizlight("<ip_address>")
    state = await bulb1.updateState()
    hueGroup = ""

    # Sets up hue group and Wiz lights depending on "room" argument given
    if(room == "vibe"):
        wizBulbs.append(bulb1)
        wizBulbs.append(bulb2)
        hueGroup = 5
    elif(room == "living"):
        hueGroup = 3
    elif(room == "bed"):
        hueGroup = 1
    elif(room == "office"):
        wizBulbs.append(bulb3)
        wizBulbs.append(bulb4)
        wizBulbs.append(bulb5)

    # Sets up brightness and color codes depending on arguments given
    if bright:
        br = int(bright)
    else:
        br = 255
    
    if scene == "pink":
        r = 250
        g = 1
        b = 80
    elif scene == "blue":
        r = 1
        g = 80
        b = 250
    elif scene == "club":
        r = 240
        g = 70
        b = 1
    elif scene == "cyan":
        r = 1
        g = 220
        b = 250
    elif scene == "plant":
        r = 10
        g = 1
        b = 35
    else:
        r = 0
        g = 0
        b = 0

    # If hue bulbs are present in room, retrieves the hue group
    if(hueGroup):
        urlG = f'http://<your bridge ip address>/api/<your hue api key>/groups/{hueGroup}'

        responseG = requests.get(urlG)

        hueLights = json.loads(responseG.text)

        # Converts rgb to hue color code (This is pretty close, but could definitely be optimized)
        if r and g and b and br:
            X = (r * 0.649926 + g * 0.103455 + b * 0.197109);
            Y = (r * 0.234327 + g * 0.743075 + b * 0.022598);
            Z = (r * 0.0000000 + g * 0.053077 + b * 1.035763);

            x = round(X / (X + Y + Z), 4);
            y = round(Y / (X + Y + Z), 4);

            xy = [];
            xy.append(x);
            xy.append(y);
            pyPay = {"on": True, "bri": br, "xy": [
        		xy[0],
        		xy[1]
        	]}
        elif r and g and b:
            X = (r * 0.649926 + g * 0.103455 + b * 0.197109);
            Y = (r * 0.234327 + g * 0.743075 + b * 0.022598);
            Z = (r * 0.0000000 + g * 0.053077 + b * 1.035763);

            x = X / (X + Y + Z);
            y = Y / (X + Y + Z);

            xy = [];
            xy.append(x);
            xy.append(y);
            pyPay = {"on": True, "xy": [
        		xy[0],
        		xy[1]
        	]}
        # If no arguments are given, just turns on bulbs using last color that you had on
        else:
            pyPay = {"on": True}

        # The api call to hue to change the current state of the bulbs
        url = f'http://<your bridge ip address>/api/<your hue api key>/groups/{hueGroup}/action'

        converted = json.dumps(pyPay)

        payload = converted

        response = requests.put(url, payload)

    # Turns on Wiz lights
    for bulb in wizBulbs:
        await bulb.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br))
    

loop = asyncio.get_event_loop()
loop.run_until_complete(main())