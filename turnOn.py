import asyncio
import sys
import requests
import json
import os
import time
from settings import env

from pywizlight import wizlight, PilotBuilder, PilotParser

async def main():

    # This code expects 4 parameters: r, g and b values, as well as brightness.
    # If none are given, it will just turn on last color you had on
    codes = sys.argv

    #This is taking in ip addresses from an env file, but you can put in your ip addresses directly for each bulb
    ip = os.getenv('IP')
    ip2 = os.getenv('IP_2')
    ip3 = os.getenv('IP_3')
    ip4 = os.getenv('IP_4')
    ip5 = os.getenv('IP_5')
    ip6 = os.getenv('IP_6')
    ip7 = os.getenv('IP_7')
    ip8 = os.getenv('IP_8')
    user_id = os.getenv('USER_ID')

    # Set up a Wiz light. Set up as many you have/want
    bulb1 = wizlight(ip)
    bulb2 = wizlight(ip2)
    bulb3 = wizlight(ip3)
    bulb4 = wizlight(ip4)
    bulb5 = wizlight(ip5)
    bulb6 = wizlight(ip6)
    bulb7 = wizlight(ip7)
    bulb8 = wizlight(ip8)


    #Sets up color schemes. I based them off of movies that seemed fitting for the mood
    if len(codes) >= 1 and codes[1] == "midnightinparis":
        r = 200
        g = 50
        b = 0
        br = 150
    elif len(codes) >= 1 and codes[1] == "moonrisekingdom":
        r = 200
        g = 50
        b = 0
        br = 254
    elif len(codes) >= 1 and codes[1] == "cyberpunk":
        hueRooms = [1,2,3]
        r = 250
        g = 0
        b = 80
        r2 = 0
        g2 = 220
        b2 = 252
        br = 254
    elif len(codes) >= 1 and codes[1] == "bladerunner":
        hueRooms = [1,2,3]
        r = 255
        g = 60
        b = 0
        r2 = 0
        g2 = 200
        b2 = 250
        br = 254
    elif len(codes) >= 1 and codes[1] == "alien":
        hueRooms = [1,2,3]
        r = 0
        g = 128
        b = 0
        r2 = 255
        g2 = 255
        b2 = 1
        br = 254
    elif len(codes) >= 1 and codes[1] == "godfather":
        hueRooms = [1,2,3]
        r = 250
        g = 0
        b = 0
        r2 = 255
        g2 = 55
        b2 = 1
        br = 120
    elif len(codes) >= 1 and codes[1] == "brucealmighty":
        hueRooms = [1,2,3]
        r = 250
        g = 250
        b = 250
        r2 = 250
        g2 = 250
        b2 = 250
        br = 254
    elif len(codes) >= 1 and codes[1] == "titanic":
        hueRooms = [1,2,3]
        r = 0
        g = 0
        b = 250
        r2 = 0
        g2 = 50
        b2 = 250
        br = 120

    if(hueRooms):

        # Roughly converts rgb values to Hue values.(This can be optimized to be more precise)
        X = (r * 0.649926 + g * 0.103455 + b * 0.197109)
        Y = (r * 0.234327 + g * 0.743075 + b * 0.022598)
        Z = (r * 0.0000000 + g * 0.053077 + b * 1.035763)

        x = round(X / (X + Y + Z), 4)
        y = round(Y / (X + Y + Z), 4)

        xy = []
        xy.append(x)
        xy.append(y)
        pyPay = {"on": True, "bri": br, "xy": [
            xy[0],
            xy[1]
        ]}

        X2 = (r2 * 0.649926 + g2 * 0.103455 + b2 * 0.197109)
        Y2 = (r2 * 0.234327 + g2 * 0.743075 + b2 * 0.022598)
        Z2 = (r2 * 0.0000000 + g2 * 0.053077 + b2 * 1.035763)

        x2 = round(X2 / (X2 + Y2 + Z2), 4)
        y2 = round(Y2 / (X2 + Y2 + Z2), 4)

        xy2 = []
        xy2.append(x2)
        xy2.append(y2)
        pyPay2 = {"on": True, "bri": br, "xy": [
            xy2[0],
            xy2[1]
        ]}

        for room in hueRooms:
            if room == 1:
                converted = json.dumps(pyPay2)
            else:
                converted = json.dumps(pyPay)

            payload = converted
            
            url = f'http://{ip}/api/{user_id}/groups/{room}/action'

            requests.put(url, payload)

            time.sleep(.25)

        if br <= 255:
            br = 50
        elif br <= 120:
            br = 20

        await asyncio.gather(bulb1.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)),
        bulb2.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)), bulb7.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)), 
        bulb8.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)))

        await asyncio.gather(bulb3.turn_on(PilotBuilder(rgb = (r2, g2, b2), brightness = br)),
        bulb4.turn_on(PilotBuilder(rgb = (r2, g2, b2), brightness = br)), bulb5.turn_on(PilotBuilder(rgb = (r2, g2, b2), brightness = br)), 
        bulb6.turn_on(PilotBuilder(rgb = (r2, g2, b2), brightness = br)))

    else:

        # Retrieves all Hue lights
        urlG = f'http://{ip}/api/{user_id}/lights/'
        responseG = requests.get(urlG)

        lights = json.loads(responseG.text)

        X = (r * 0.649926 + g * 0.103455 + b * 0.197109)
        Y = (r * 0.234327 + g * 0.743075 + b * 0.022598)
        Z = (r * 0.0000000 + g * 0.053077 + b * 1.035763)

        x = round(X / (X + Y + Z), 4)
        y = round(Y / (X + Y + Z), 4)

        xy = []
        xy.append(x)
        xy.append(y)
        pyPay = {"on": True, "bri": br, "xy": [
            xy[0],
            xy[1]
        ]}

        # Turns on all Hue lights
        for light in lights:
            url = f'http://{ip}/api/{user_id}/lights/{light}/state'

            converted = json.dumps(pyPay)

            payload = converted

            requests.put(url, payload)

        # Turns on all Wiz lights in sync
        await asyncio.gather(bulb1.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)),
        bulb2.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)), bulb3.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)), bulb4.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)), bulb5.turn_on(PilotBuilder(rgb = (r, g, b), brightness = br)), loop = loop)
    

loop = asyncio.get_event_loop()
loop.run_until_complete(main())