from typing import IO
import json
import pandas as pd
from flask import Flask, request

import pathlib
import gpxpy, fitparse

import gzip

app = Flask(__name__)

path = pathlib.Path("data")

activities = path.joinpath('activities.csv')
activities = pd.read_csv(activities)

activities = activities.dropna(axis=1, how='all')
columns = activities.count(axis=0)
columns = columns.index[columns < 20]

activities = activities.drop(columns, axis=1)
activities_json = activities.to_json(orient='split')


@app.route("/activities")
def activities_handler():
    return (activities_json, 200, {'Content-Type': 'Application/Json'})


@app.route("/activities/<id>")
def activity_handler(id):
    id = int(id)

    if (mask := (activities["Activity ID"] == id)).sum() != 1:
        return ("Not found", 404)

    filename: str = activities.Filename[mask].values[0]
    
    dataframe = None
    if filename.endswith('.gpx'):
        with open(path.joinpath(filename)) as file:
            pts = parse_gpx_file(file)

        return pts.to_json(), 200, {'Content-Type': 'Application/Json'}
    elif filename.endswith('.gpx.gz'):
        with gzip.open(path.joinpath(filename)) as file:
            pts = parse_gpx_file(file)

        return pts.to_json(), 200, {'Content-Type': 'Application/Json'}
    elif filename.endswith('.fit.gz'):
        with gzip.open(path.joinpath(filename)) as file:
            pts = parse_fit_file(file)
        
        return pts.to_json(), 200, {'Content-Type': 'Application/Json'}
    else:
        return (f"Activity file type not supported {filename}", 501)


def parse_gpx_file(file: IO[str]) -> pd.DataFrame:
    gpx = gpxpy.parse(file)

    pts = pd.DataFrame([(p.latitude, p.longitude, p.elevation, p.time) for p in gpx.tracks[0].segments[0].points],
                columns=['lat', 'lon', 'elevation', 'time'])
    return pts

def parse_fit_file(file: IO[str]) -> pd.DataFrame:
    fitfile = fitparse.FitFile(file)

    points = []
    for record in fitfile.get_messages("record"):
        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        lat, lon = record.get("position_lat"), record.get("position_long")
        if lat.units == "semicircles" or lon.units == "semicircles":
            if lat.value != None and lon.value != None:
                lat = lat.value / (2**32 / 360)
                lon = lon.value / (2**32 / 360)
            else:
                lat, lon = None, None
        else:
            raise Exception(f"lat lon are not semicircles {lat}, {lon}")

        time     = record.get("timestamp")
        speed    = record.get("speed")
        if speed.units != "m/s":
            raise Exception(f"speed units are not m/s{speed}")

        points.append((lat, lon, time.value, speed.value))

    return pd.DataFrame(points, columns=['lat', 'lon', 'time', 'speed'])

@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = '*'
    return response


