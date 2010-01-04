#!/usr/bin/env python

import sys
from optparse import OptionParser
import gzip
import zipfile
import unicodedata

ENCODE_NORMALIZE_OPTIONS = ('NFC', 'NFKC', 'NFD', 'NFKD')
ENCODE_NORMALIZE = ENCODE_NORMALIZE_OPTIONS[3]
ENCODE_TARGET_TYPE_OPTIONS = ('ascii')
ENCODE_TARGET_TYPE = ENCODE_TARGET_TYPE_OPTIONS[0]
ENCODE_ACTION_OPTIONS = ('ignore')
ENCODE_ACTION = ENCODE_ACTION_OPTIONS[0]

def init_params():
    #global options, source, destination
    usage = "./unicode2ascii.py [options] source dest"
    parser = OptionParser(usage)
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    parser.add_option('-o', '--overwrite', action='store_true', dest='overwrite',
        help='Overwrite source')
    (options, args) = parser.parse_args()
    try:
        source = args[0]
        print ('source', args[0])
    except Exception, ex:
        print 'Missing source file'
        sys.exit(1)
    destination = None
    try:
        destination = args[1]
        print ('dest', args[1])
    except Exception, ex:
        print 'Missing destination file.  Using default destination by stripping ending'
    return options, source, destination


def unicode_to_asii(source_text):
    if type(source_text) == type(str()):
        return source_text
    try:
        converted_text = unicodedata.normalize(ENCODE_NORMALIZE, input_string).\
            encode(ENCODE_TARGET_TYPE, ENCODE_ACTION)
    except Exception, ex:
        print 'unicode_to_ascii error', ex
        print ('source_text type', type(source_text))
        sys.exit(4)
    return converted_text


def read_file(source_file):
    return source_file.read()


def open_source(source):
    # .zip, .gz, .tar.gz
    if any(source.endswith(ending) for ending in ('.tar.gz', '.tar.gzip')):
        print '.tar.gz Not implemented yet'
        sys.exit(3)
    elif any(source.endswith(ending) for ending in ('.gzip', '.gz')):
        source_file = gzip.open(source, 'rb')
    elif any(source.endswith(ending) for ending in ('.zip')):
        source_file = zipfile.ZipFile(source, 'rb')
    return source_file


if __name__ == '__main__':
    options, source, destination = init_params()
    source_file = open_source(source)
    source_text = read_file(source_file)
    converted_text = unicode_to_ascii(source_text)
