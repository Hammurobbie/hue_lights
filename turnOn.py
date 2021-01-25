import asyncio
import sys
import requests
import json
import os
from settings import env

from pywizlight import wizlight, PilotBuilder, PilotParser

async def main():

    # This code expects 4 parameters: r, g and b values, as well as brightness.
    # If none are given, it will just turn on last color you had on
    codes = sys.argv

    #This is taking in ip addresses from an env file, but you can put in your ip addresses directly for each bulb
    ip = os.getenv('IP')
    ip2 = os.getenv('IP2')
    ip3 = os.getenv('IP3')
    ip4 = os.getenv('IP4')
    ip5 = os.getenv('IP5')
    user_id = os.getenv('USER_ID')

    # Set up a Wiz light. Set up as many you have/want
    bulb1 = wizlight(ip)
    bulb2 = wizlight(ip)
    bulb3 = wizlight(ip)
    bulb4 = wizlight(ip)
    bulb5 = wizlight(ip)
    state = await bulb1.updateState()

    # Retrieves all Hue lights
    urlG = f'http://{ip}/api/{user_id}/lights/'

    responseG = requests.get(urlG)

    lights = json.loads(responseG.text)


    #Sets up rgb and brightness values from arguments given
    if len(codes) > 4:
        r = int(codes[1])
        g = int(codes[2])
        b = int(codes[3])
        br = int(codes[4])
    elif len(codes) > 1:
        r = int(codes[1])
        g = int(codes[2])
        b = int(codes[3])
        br = 254
    else:
        r = 255
        g = 255
        b = 255
        br = 254

    # Roughly converts rgb values to Hue values.(This can be optimized to be more precise)
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
        xy.push(x);
        xy.push(y);
        pyPay = {"on": True, "xy": [
			xy[0],
			xy[1]
		]}
    else:
        pyPay = {"on": True}

    # Turns on all Hue lights
    for light in lights:
        url = f'http://{ip}/api/{user_id}/lights/{light}/state'

        converted = json.dumps(pyPay)

        payload = converted

        response = requests.put(url, payload)

    # Turns on all Wiz lights in sync
    await asyncio.gather(bulb1.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)),
       bulb2.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)), bulb3.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)), bulb4.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)), bulb5.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)), loop = loop)
    

loop = asyncio.get_event_loop()
loop.run_until_complete(main())