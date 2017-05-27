__author__ = 'Maria G, Patryk Czajka'

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

    if not event in events_coordinates:
        raise KeyError('Event %s not found in file "%s"' % (event, config.EVENTS_DATA))

    if not station in stations_coordinates:
        raise KeyError('Station %s not found in file "%s"' % (station, config.STATIONS_DATA))

    ev_lat, ev_lon, ev_time, ev_depth = events_coordinates[event]
    stat_lat, stat_lon = stations_coordinates[station]

    dist_m, azimuth, _ = gps2dist_azimuth(stat_lat, stat_lon, ev_lat, ev_lon)

    dist_deg = 180 * dist_m / (config.EARTH_RADIUS * math.pi)

    model = TauPyModel(model="iasp91")
    arr = model.get_travel_times(source_depth_in_km = ev_depth,
                                 distance_in_degree = dist_deg, phase_list=['P'])[0]

    slowness = arr.ray_param * 1000 / config.EARTH_RADIUS

    return azimuth, slowness


def _load_stations_coordinates(filepath):
    result = {}
    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row): # Windows line ending creates empty rows
                result[row[1]] = (float(row[2]), float(row[3]))

    return result


def _load_events_coordinates(filepath):
    if config.EVENTS_FORMAT == 'EU':
        return _load_events_coordinates_EU(filepath)

    elif config.EVENTS_FORMAT == 'US':
        return _load_events_coordinates_US(filepath)

    else:
        raise NotImplementedError


def _load_events_coordinates_US(filepath):
    result = {}
    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter=",")
        next(reader)
        for row in reader:
            if len(row): # Windows line ending creates empty rows
                label = _datetime_to_label(row[0])
                result[label] = (float(row[1]), float(row[2]), UTCDateTime(row[0]), float(row[3]))
    return result


def _load_events_coordinates_EU(filepath):
    result = {}
    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            print (row )
            if len(row): # Windows line ending creates empty rows
                label = _datetime_to_label(row[0])
                result[label] = (float(row[3]), float(row[4]), UTCDateTime(row[0]), float(row[5]))
    return result


def _datetime_to_label(datetime):
    return datetime[2 : 19].replace('-', '').replace('T', '_').replace(':', '')
