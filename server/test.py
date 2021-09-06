import gzip
from typing import IO
import fitparse

import pandas as pd

import time as tt


start = tt.time()
file = gzip.open("data/activities/2689519102.fit.gz")

def parse_fit_file(file: IO[str]) -> pd.DataFrame:
    fitfile = fitparse.FitFile(file)

    points = []
    for record in fitfile.get_messages("record"):
        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        lat, lon = record.get("position_lat"), record.get("position_long")
        if lat.units == "semicircles" or lon.units == "semicircles":
            lat = lat.value / (2**32 / 360)
            lon = lon.value / (2**32 / 360)
        else:
            raise Exception(f"lat lon are not semicircles {lat}, {lon}")

        time     = record.get("timestamp")
        speed    = record.get("speed")
        if speed.units != "m/s":
            raise Exception(f"speed units are not m/s{speed}")

        points.append((lat, lon, time.value, speed.value))

    return pd.DataFrame(points, columns=['lat', 'lon', 'time', 'speed'])