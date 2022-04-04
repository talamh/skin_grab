import argparse
import base64
import urllib.request
from io import BytesIO
from typing import Union

from json import JSONDecodeError
from json import loads

import requests
from PIL import Image


def player_by_name(player_name: str) -> Union[tuple, None]:
    """ download the minecraft skin of the given player """
    with urllib.request.urlopen(f'https://api.mojang.com/users/profiles/minecraft/'
                                f'{player_name}') as url:
        try:
            data = loads(url.read().decode())
        except JSONDecodeError:
            print(f'player {player_name} not found')
            return None

        data = player_by_uuid(data.get('id'))

        if data is None:
            return player_name, None

        return data


def player_by_uuid(uuid: str) -> Union[tuple, None]:
    """ download the minecraft skin of the player with the given uuid """
    with urllib.request.urlopen(f'https://sessionserver.mojang.com/session/minecraft/profile/'
                                f'{uuid}') as url:
        try:
            data = loads(url.read().decode())
        except JSONDecodeError:
            print(f'player with uuid {uuid} not found')
            return None

        player_name = data.get('name')
        data = loads(base64.b64decode(data.get('properties')[0]
                                      .get("value"))).get('textures').get('SKIN').get('url')

        request = requests.get(data, stream=True)

        if request.status_code == 200:
            request.raw.decode_content = True
            img = Image.open(BytesIO(request.content))
            return player_name, img

        return None


def process_skin(player: tuple) -> tuple:
    """ generate minetest skin and skin preview images """
    width, height = player[1].size

    skin_preview = Image.new(mode='RGBA', size=(16, 32), color=(0, 0, 0, 0))

    # head
    layer_1 = player[1].crop((8, 8, 16, 16))
    skin_preview.paste(layer_1, (4, 0))

    # hair/glasses etc
    layer_1 = player[1].crop((40, 8, 48, 16))
    skin_preview.paste(layer_1, (4, 0), layer_1)

    # body
    layer_1 = player[1].crop((20, 20, 28, 32))
    skin_preview.paste(layer_1, (4, 8), layer_1)

    # right leg
    layer_1 = player[1].crop((4, 20, 8, 32))
    skin_preview.paste(layer_1, (4, 20), layer_1)

    # right arm
    layer_1 = player[1].crop((44, 20, 48, 32))
    skin_preview.paste(layer_1, (0, 8), layer_1)

    if height == 64:
        # left arm
        layer_1 = player[1].crop((36, 52, 40, 64))
        skin_preview.paste(layer_1, (12, 8), layer_1)

        # left leg
        layer_1 = player[1].crop((20, 52, 24, 64))
        skin_preview.paste(layer_1, (8, 20), layer_1)

        mt_skin = player[1].crop((0, 0, width, 32))

        # optionally use overlays from bottom half
        if args.overlays:
            layer_1 = player[1].crop((0, 32, width, 48))
            mt_skin.paste(layer_1, (0, 16), layer_1)
            # right leg overlay
            layer_1 = player[1].crop((4, 36, 8, 48))
            skin_preview.paste(layer_1, (4, 20), layer_1)

            # left leg overlay
            layer_1 = player[1].crop((4, 52, 8, 64))
            skin_preview.paste(layer_1, (8, 20), layer_1)
            # right arm overlay
            layer_1 = player[1].crop((40, 36, 44, 48))
            skin_preview.paste(layer_1, (0, 8), layer_1)

            # left arm overlay
            layer_1 = player[1].crop((52, 52, 56, 64))
            skin_preview.paste(layer_1, (12, 8), layer_1)

            # body overlay
            layer_1 = player[1].crop((20, 36, 28, 48))
            skin_preview.paste(layer_1, (4, 8), layer_1)

        return player[0], mt_skin, skin_preview

    # left arm
    layer_1 = player[1].crop((44, 20, 48, 32))
    skin_preview.paste(layer_1, (12, 8), layer_1)

    # left leg
    layer_1 = player[1].crop((4, 20, 8, 32))
    skin_preview.paste(layer_1, (8, 20), layer_1)

    return player[0], player[1], skin_preview


def main():
    player = player_by_name(args.n)

    if player is not None:
        player = process_skin(player)
        player[1].save(f'{player[0]}.png')
        player[2].save(f'preview_{player[0]}.png')
        print(f'{player[0]} skin downloaded successfully.')


parser = argparse.ArgumentParser(description="Minecraft skin downloader/converter.")
parser.add_argument("-n", help="Minecraft player name", required=True)
parser.add_argument('-overlays', action='store_true')
args = parser.parse_args()

if __name__ == "__main__":
    main()
