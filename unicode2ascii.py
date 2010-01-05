#!/usr/bin/env python

import sys
from optparse import OptionParser
import gzip
import zipfile
import unicodedata

ENCODE_NORMALIZE_OPTIONS = ('NFC', 'NFKC', 'NFD', 'NFKD')
ENCODE_NORMALIZE = ENCODE_NORMALIZE_OPTIONS[3]
ENCODE_TARGET_TYPE_OPTIONS = ('ascii',)
ENCODE_TARGET_TYPE = ENCODE_TARGET_TYPE_OPTIONS[0]
ENCODE_ACTION_OPTIONS = ('ignore',)
ENCODE_ACTION = ENCODE_ACTION_OPTIONS[0]
FILE_TYPES = {'tar_gz': ('.tar.gz', '.tar.gzip'),
                     'gz': ('.gzip', '.gz'),
                     'zip': ('.zip',)}

def init_params():
    #global options, source, destination
    usage = "./unicode2ascii.py [options] source"
    parser = OptionParser(usage)
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    parser.add_option('-i', '--inplace', action='store_true', dest='inplace',
        help='Overwrite source')
    parser.add_option('-s', '--strip_ending', action='store_true', dest='strip_ending',
        help='Destination file name is same as source with compression ending stripped')
    parser.add_option('-o', '--output', action='store', dest='output')
    (options, args) = parser.parse_args()
    try:
        source = args
        print ('source', args)
    except Exception, ex:
        print 'Missing source file'
        sys.exit(1)
    if not len(source):
        print 'Missing source file'
        sys.exit(1)
    destination = None
    if options.inplace and options.strip_ending:
        print '--inplace and --strip_ending collide'
        sys.exit(1)
    if options.inplace and options.output:
        print '--inplace and --output collide'
        sys.exit(1)
    if options.strip_ending and options.output:
        print '--strip_ending and --output collide'
        sys.exit(1)
    destination = options.output
    print ('args', args)
    return options, source, destination


def unicode_to_ascii(source_text):
    if type(source_text) == type(str()):
        try:
            source_text = unicode(source_text, "utf-8")
        except Exception, ex:
            print 'Unicode Exception', ex
    try:
        converted_text = unicodedata.normalize(ENCODE_NORMALIZE, source_text).\
            encode(ENCODE_TARGET_TYPE, ENCODE_ACTION)
    except Exception, ex:
        print 'unicode_to_ascii error', ex
        print ('ENCODE_NORMALIZE', ENCODE_NORMALIZE)
        print ('ENCODE_TARGET_TYPE', ENCODE_TARGET_TYPE)
        print ('ENCODE_ACTION', ENCODE_ACTION)
        print ('source_text type', type(source_text))
        sys.exit(4)
    return converted_text


def read_file(source_file):
    return source_file.read()


def open_source(source):
    # .zip, .gz, .tar.gz
    if source.endswith(FILE_TYPES['tar_gz']):
        print '.tar.gz Not implemented yet'
        sys.exit(3)
    elif source.endswith(FILE_TYPES['gz']):
        source_file = gzip.open(source, 'rb')
    elif source.endswith(FILE_TYPES['zip']):
        source_file = zipfile.ZipFile(source, 'rb')
    return source_file


def strip_ending(destination):
    for endings in FILE_TYPES.itervalues():
        for ending in endings:
            if destination.endswith(ending):
                destination = destination[:-len(ending)]
                if destination.endswith('.tar'):
                    destination = destination[:-len('.tar')]
                return destination

        
def write_file_helper(options, source, destination, converted_text):
    print ('begin', 'write_file')
    if options.strip_ending:
        destination = strip_ending(source)
        dest_fp = open(destination, 'w')
        dest_fp.write(converted_text)
        dest_fp.close()
    elif options.inplace:
        destination = source
        if source.endswith(FILE_TYPES['gz']):
            dest_fp = gzip.open(destination, 'wb')
            dest_fp.write(converted_text)
            dest_fp.close()
        else:
            print 'Unsupported file format', source
    else:
        print 'Not stripping end.  Doing nothing'
        
   

if __name__ == '__main__':
    options, sources, destination = init_params()
    for source in sources:
        print ('source', source)
        source_file = open_source(source)
        source_text = read_file(source_file)
        converted_text = unicode_to_ascii(source_text)
        write_file_helper(options, source, destination, converted_text)
