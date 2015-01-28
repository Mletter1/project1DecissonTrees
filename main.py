#!/usr/bin/env python
__author__ = 'mletter1'
import sys
import os
import traceback
import optparse
import time
import re

doc = """
SYNOPSIS

    TODO helloworld [-h,--help] [-v,--verbose] [--version]

DESCRIPTION

    TODO This describes how to use this script. This docstring
    will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Name <name@example.org>

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    $Id$
"""

# from pexpect import run, spawn

def main():
    global options, args
    # TODO: Do something more interesting here...
    print 'Hello world!'


if __name__ == '__main__':
    try:
        print 'Hello world!'
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=doc,
                                       version='%prog 0.1')

        parser.add_option('-v', '--verbose', action='store_true', default=False, help='verbose output')

        (options, args) = parser.parse_args()
        print "opps", options
        print "args", args


        #if len(args) < 1:
        #    parser.error('missing argument')
        if options.verbose: print time.asctime()
        main()
        if options.verbose:
            print time.asctime()
        if options.verbose:
            print 'TOTAL TIME IN MINUTES:',
        if options.verbose:
            print (time.time() - start_time) / 60.0
        sys.exit(0)



    except KeyboardInterrupt, e:  # Ctrl-C
        raise e
    except SystemExit, e:  # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)