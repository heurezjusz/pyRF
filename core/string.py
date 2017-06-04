# functions for operating on filenames

import config
import ntpath
from os.path import splitext


def output_filename(path, prefix='', extension=config.SAVE_FORMAT):
    return 'out/' + prefix + _extract_filemane(path) + '.' + extension


def station_event(path):
    res = _extract_filemane(path).split('_')
    return res[0], res[1] + '_' + res[2]


def _extract_filemane(path):
    return splitext(ntpath.basename(path))[0]