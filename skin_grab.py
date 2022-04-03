import argparse
import base64
import json
import urllib.request
from io import BytesIO
from typing import Union

import requests
from PIL import Image


def player_by_name(player_name: str) -> Union[tuple, None]:
    with urllib.request.urlopen(f'https://api.mojang.com/users/profiles/minecraft/{player_name}') as url:
        try:
            data = json.loads(url.read().decode())
        except JSONDecodeError:
            print(f'player {player_name} not found')
            return None

        data = player_by_uuid(data.get('id'))

        if data is None:
            return player_name, None
        else:
            return data


def player_by_uuid(uuid: str) -> Union[tuple, None]:
    with urllib.request.urlopen(f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}') as url:
        try:
            data = json.loads(url.read().decode())
        except JSONDecodeError:
            print(f'player with uuid {uuid} not found')
            return None

        player_name = data.get('name')
        data = json.loads(base64.b64decode(data.get('properties')[0]
                                           .get("value"))).get('textures').get('SKIN').get('url')

        r = requests.get(data, stream=True)

        if r.status_code == 200:
            r.raw.decode_content = True
            img = Image.open(BytesIO(r.content))
            return player_name, img
        else:
            return None


def process_skin(player: tuple) -> tuple:
    width, height = player[1].size

    if height == 64:
        layer_0 = player[1].crop((0, 0, width, 32))

        # optionally use overlays from bottom half
        if args.overlays:
            layer_1 = player[1].crop((0, 32, width, 48))
            layer_0.paste(layer_1, (0, 16), layer_1)
        return player[0], layer_0
    else:
        return player


def main():
    player = player_by_name(args.n)

    if player is not None:
        player = process_skin(player)
        player[1].save(f'{player[0]}.png')


parser = argparse.ArgumentParser(description="Minecraft skin downloader/converter.")
parser.add_argument("-n", help="Minecraft player name", required=True)
parser.add_argument('-overlays', action='store_true')
args = parser.parse_args()

if __name__ == "__main__":
    main()
