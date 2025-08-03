import asyncio
import os
from dotenv import load_dotenv
import random

load_dotenv()

from tapo import ApiClient
from tapo.requests import Color


async def main():
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")
    bulb_addresses = {
        "bulb1":"192.168.68.75",
        "bulb2":"192.168.68.76",
        "bulb3":"192.168.68.78",
        "bulb4":"192.168.68.79",
    }

    client = ApiClient(tapo_username, tapo_password)

    bulb_list = []

    for name, ip in bulb_addresses.items():
        bulb = await client.l530(ip)
        bulb_list.append(bulb)

    for i in range(30):

        for device in bulb_list:

            hue = random.randint(0, 360)
            saturation = random.randint(80, 100)  # High saturation for vivid colours

            await device.set_hue_saturation(hue, saturation)

            await device.on()

            await asyncio.sleep(0.1)

            await asyncio.sleep(0.1)

            await device.off()

        await asyncio.gather(*[
            asyncio.create_task(device.set_hue_saturation(hue, saturation)) for device in bulb_list
        ])

        await asyncio.gather(*[
            asyncio.create_task(device.on()) for device in bulb_list
        ])

        await asyncio.sleep(0.15)

        await asyncio.gather(*[
        asyncio.create_task(device.off()) for device in bulb_list
        ])

    await asyncio.gather(*[
        asyncio.create_task(device.off()) for device in bulb_list
    ])

if __name__ == "__main__":
    asyncio.run(main())