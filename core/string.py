# functions for operating on filenames

import ntpath

def _extract_filemane(path):
    return ntpath.basename(path)

def output_filename(path, prefix=''):
    return 'out/' + prefix + _extract_filemane(path)