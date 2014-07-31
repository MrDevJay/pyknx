#!/usr/bin/python3

# Copyright (C) 2012-2014 Cyrille Defranoux
#
# This file is part of Pyknx.
#
# Pyknx is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyknx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyknx. If not, see <http://www.gnu.org/licenses/>.
#
# For any question, feature requests or bug reports, feel free to contact me at:
# knx at aminate dot net

"""
Modifies an XML config for Linknx so that it allows for communication with an instance of pyknxcommunicator.py
This script adds an ioport and a rule for each object that holds a pyknxcallback attribute in the source XML.
It always starts by cleaning any autogenerated rule from the input file and generates new ones unless the --clean option is passed.
Source XML configuration is read from standard input unless the -i option is set.
"""

from pyknx.configurator import Configurator
import argparse
import getopt
import sys
import logging
from pyknx import logger

def parseAddress(addrStr, option):
    ix = addrStr.find(':')
    if ix < 0:
        raise Exception('Malformed value for ' + option +'. Expecting a tuple (hostname:port)')
    return (addrStr[0:ix], addrStr[ix + 1:])

def makeArgumentParser(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input-file', dest='linknxConfig', help='use LKNCONF as the source linknx configuration rather than reading from standard input.', metavar='LKNCONF')
    parser.add_argument('-o', '--output-file', dest='outputFile', help='write the modified linknx configuration to FILE rather than to standard output.', metavar='FILE')
    parser.add_argument('-c', '--comm-addr', dest='communicatorAddress', help='Address of the communicator. This argument must specify the hostname or the ip address followed by a colon and the port to listen on. Default is "localhost:1029"', default='localhost:1029')
    parser.add_argument('-n', '--comm-name', dest='communicatorName', help='Name of the communicator. Used to prefix name of rules generated by this script and to name the ioport service as well. Default is "pyknxcommunicator"', default='pyknxcommunicator')
    parser.add_argument('--clean', help='Clean rules that were generated by this script but do not generate new rules.', action='store_true')
    parser.add_argument('-v', '--verbose', dest='verbosityLevel', help='set verbosity level. Default is "error".', metavar='LEVEL', choices=[l.lower() for l in logger.getLevelsToString()], default='error')
    return parser

if __name__ == '__main__':
    parser = makeArgumentParser(__doc__)
    args = parser.parse_args()

    # Configure logger.
    logger.initLogger(None, args.verbosityLevel.upper())

    args.communicatorAddress = parseAddress(args.communicatorAddress, 'communicator address')

    # Start configurator.
    configurator = Configurator(args.linknxConfig, args.outputFile, args.communicatorAddress, args.communicatorName)

    # Generate config.
    configurator.cleanConfig()
    if not args.clean:
        configurator.generateConfig()
    configurator.writeConfig()
