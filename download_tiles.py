import os
import math
import requests

# Create folder
os.makedirs("offline_maps", exist_ok=True)

# Location (Delhi example)
lat = 28.6139
lon = 77.2090
zoom = 10

# Convert lat/lon to tile numbers
def deg2num(lat_deg, lon_deg, zoom):

    lat_rad = math.radians(lat_deg)

    n = 2.0 ** zoom

    xtile = int((lon_deg + 180.0) / 360.0 * n)

    ytile = int(
        (1.0 - math.asinh(math.tan(lat_rad)) / math.pi)
        / 2.0 * n
    )

    return (xtile, ytile)

x, y = deg2num(lat, lon, zoom)

# Download nearby tiles
for dx in range(-2, 3):

    for dy in range(-2, 3):

        tile_x = x + dx
        tile_y = y + dy

        url = f"https://tile.openstreetmap.org/{zoom}/{tile_x}/{tile_y}.png"

        response = requests.get(url)

        if response.status_code == 200:

            filename = f"offline_maps/{zoom}_{tile_x}_{tile_y}.png"

            with open(filename, "wb") as f:

                f.write(response.content)

            print("Saved:", filename)