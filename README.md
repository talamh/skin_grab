# skin_grab.py

Simple utility to download a Minecraft skin and convert it for use with Minetest.
Also generates preview image.

## requirements
Depending on your installation you may need to install:

PILLOW

`$ pip install PILLOW`

requests

`$ pip install requests`

## requirements

To only use the top half of 64x64 Minecraft skins:

`$ python skin_grab.py -n playername`

To also use the overlay section of 64x64 skins:

`$ python skin_grab.py -n playername -overlays`
