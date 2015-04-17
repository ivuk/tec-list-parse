#!/usr/bin/env python3


from xml.dom import minidom
import urllib.request
import datetime
import os
import argparse


def getDataFile(Url, FileName):
    """
    Generic function for opening an URL and saving its content to file
    """
    if not os.path.isfile(FileName) and not os.access(FileName, os.R_OK):
        try:
            DataFile = urllib.request.urlopen(Url)
        except urllib.error.URLError as e:
            print("Got URLError from urllib2, reason: {}".format(e.reason))
        else:
            Output = open(FileName, 'wb')
            Output.write(DataFile.read())
            Output.close()
    else:
        print("File '{}' already exists, using existing data.".format(FileName))


def getHNBDataFile(Currency):
    """
    Get the required data file from HNB
    """
    now = datetime.datetime.now()
    HnbUrl = "http://www.hnb.hr/tecajn/f{}.dat".format(now.strftime("%d%m%y"))
    HnbFileName = "f{}.dat".format(now.strftime("%d%m%y"))
    getDataFile(HnbUrl, HnbFileName)

    if Currency == 'all':
        getHNBData(HnbFileName, 'all')
    else:
        getHNBData(HnbFileName, Currency)


def getPBZDataFile(Currency):
    """
    Get the required data file from PBZ
    """
    PBZUrl = 'http://www.pbz.hr/Downloads/PBZteclist.xml'
    getDataFile(PBZUrl, 'PBZteclist.xml')

    if Currency == 'all':
        getPBZData('PBZteclist.xml', 'all')
    else:
        getPBZData('PBZteclist.xml', Currency)


def getHNBData(FileName, Currency):
    """
    Print out data from HNB
    """
    print("--- HNB ---\nName\tMean Rate")
    try:
        HnbFile = open(FileName, "r")
    except IOError as e:
        print("Got IOError, '{}: {}'".format(e.errno, e.strerror))
    else:
        HeaderLine = HnbFile.readline()
        for elem in HnbFile:
            elem = elem.strip()
            column = elem.split()

            if Currency == 'all':
                print("{}\t{}".format(str(column[0])[3:6], column[2]))
            elif Currency == str(column[0])[3:6]:
                print("{}\t{}".format(str(column[0])[3:6], column[2]))

        HnbFile.close()


def getPBZData(FileName, Currency):
    """
    Print out data from PBZ
    """
    print("--- PBZ ---\nName\tMean Rate")
    try:
        doc = minidom.parse(FileName)
    except IOError as e:
        print("Got IOError, '{}: {}'".format(e.errno, e.strerror))
    else:
        currencies = doc.getElementsByTagName("Currency")
        for elem in currencies:
            currname = elem.getElementsByTagName('Name')
            currval = elem.getElementsByTagName('MeanRate')
            for elem in currname:
                ValName = elem.childNodes[0].nodeValue
                for elem in currval:
                    ValMeanRate = elem.childNodes[0].nodeValue

                    if Currency == 'all':
                        print("{}\t{}".format(ValName, ValMeanRate))
                    elif Currency == ValName:
                        print("{}\t{}".format(ValName, ValMeanRate))


def RemoveDataFiles():
    """
    Function for removing the downloaded data files
    """
    now = datetime.datetime.now()
    HnbFileName = "f{}.dat".format(now.strftime("%d%m%y"))
    PBZFileName = 'PBZteclist.xml'
    FileNames = [HnbFileName, PBZFileName]

    for DataFile in FileNames:
        if os.path.isfile(DataFile) and os.access(DataFile, os.W_OK):
            try:
                os.remove(DataFile)
                print("Removing {}...".format(DataFile))
            except OSError as e:
                print("Got OSError, '{}: {}'".format(e.errno, e.strerror))


def doit():
    """
    Set up the available program options
    Call the proper functions with proper parameters depending on user
    input
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all', help='Show values for all available \
            currencies', action="store_true", dest='All')
    parser.add_argument('-c', '--currency', help='Set the currency for which \
            the value is shown', type=str, dest='currency')
    parser.add_argument('-r', '--reset', help='Remove the data files that \
            have been downloaded', action="store_true", dest='reset')

    args = parser.parse_args()

    if not args.All and not args.currency and not args.reset:
        parser.print_help()

    if args.All:
        getPBZDataFile('all')
        getHNBDataFile('all')
    elif args.currency:
        getPBZDataFile(args.currency)
        getHNBDataFile(args.currency)
    elif args.reset:
        RemoveDataFiles()


if __name__ == "__main__":
    doit()
