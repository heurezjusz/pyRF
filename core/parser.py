# parsing arguments
import argparse
import config

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_folder', type=str,
        help='name of a folder with datafiles',
        nargs='?',
        default=config.DATAFOLDER)
    args = vars(parser.parse_args())

    config.DATAFOLDER = args['data_folder']