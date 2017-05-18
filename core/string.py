# functions for operating on filenames

import config
import ntpath
from os.path import splitext


def output_filename(path, prefix=''):
    return 'out/' + prefix + _extract_filemane(path) + '.' + config.SAVE_FORMAT


def _extract_filemane(path):
    return splitext(ntpath.basename(path))[0]