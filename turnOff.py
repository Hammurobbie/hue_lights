import asyncio
import sys
import requests
import json
import os
from settings import env

from pywizlight import wizlight, PilotBuilder, PilotParser

async def main():

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
    urlG = f'http://{ip}/api/{user_id}/lights'

    responseG = requests.get(urlG)

    lights = json.loads(responseG.text)

    # Turns off all hue lights
    for light in lights:
        url = f'http://{ip}/api/{user_id}/lights/{light}/state'

        pyPay = {"on": False}

        converted = json.dumps(pyPay)

        payload = converted

        response = requests.put(url, payload)

    # Turns off all Wiz lights at the same in sync 
    await asyncio.gather(bulb1.turn_off(), bulb2.turn_off(), bulb3.turn_off(), bulb4.turn_off(), bulb5.turn_off(), loop = loop)
    

loop = asyncio.get_event_loop()
loop.run_until_complete(main())