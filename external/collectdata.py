__author__ = 'Maria G'

import config
import csv
import math
from core import station_event
from obspy.core.utcdatetime import UTCDateTime
from obspy.geodetics.base import gps2dist_azimuth
from obspy.taup import TauPyModel



events_coordinates = None
stations_coordinates = None

def collect_data(filename):
    global events_coordinates, stations_coordinates

    station, event = station_event(filename)

    if stations_coordinates is None:
        stations_coordinates = _load_stations_coordinates(config.STATIONS_DATA)

    if events_coordinates is None:
        events_coordinates = _load_events_coordinates(config.EVENTS_DATA)

    ev_lat, ev_lon, ev_time, ev_depth = events_coordinates[event]
    stat_lat, stat_lon = stations_coordinates[station]

    print ( (stat_lat, stat_lon, ev_lat, ev_lon))
    dist_m, azimuth, _ = gps2dist_azimuth(stat_lat, stat_lon, ev_lat, ev_lon)

    dist_deg = 180 * dist_m / (config.EARTH_RADIUS * math.pi)

    model = TauPyModel(model="iasp91")
    arr = model.get_travel_times(source_depth_in_km = ev_depth,
                                 distance_in_degree = dist_deg, phase_list=['P'])[0]

    slowness = arr.ray_param * 1000 / config.EARTH_RADIUS

    return azimuth, slowness


def _load_events_coordinates(filepath):
    result = {}
    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            label = row[1][-2:] + row[2] + row[3] + '_' + row[4][:-3]
            result[label] = (float(row[5]), float(row[6]), UTCDateTime(row[1]+row[2]+row[3] + 'T' + row[4]), float(row[7]))
    return result


def _load_stations_coordinates(filepath):
    result = {}
    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)
        for row in reader:
            if len(row): # Windows line ending creates empty rows
                result[row[0]] = (float(row[1]), float(row[2]))

    return result
