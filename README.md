# skin_grab.py

Simple utility to download a Minecraft skin and convert it for use with Minetest.
Also generates preview image.

## requirements
PILLOW

```bash
$ pip install PILLOW
```

requests

```bash
$ pip install requests
```

## usage

To only use the top half of 64x64 Minecraft skins:

```bash
$ python skin_grab.py -n playername
```

To also use the overlay section of 64x64 skins:

```bash
$ python skin_grab.py -n playername -overlays
```
