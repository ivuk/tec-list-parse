#!/usr/bin/env python


from xml.dom import minidom
import urllib2
import datetime
import os
import argparse


def getDataFile(Url, FileName):
    """
    Generic function for opening an URL and saving its content to file
    """
    if not os.path.isfile(FileName) and not os.access(FileName, os.R_OK):
        try:
            DataFile = urllib2.urlopen(Url)
        except urllib2.URLError, e:
            print "Got URLError from urllib2, reason: %s" % e.reason
        else:
            Output = open(FileName, 'wb')
            Output.write(DataFile.read())
            Output.close()
    else:
        print "File '%s' already exists, using existing data." % FileName


def getHNBDataFile(Currency):
    """
    Get the required data file from HNB
    """
    now = datetime.datetime.now()
    HnbUrl = "http://www.hnb.hr/tecajn/f%s.dat" % (now.strftime("%d%m%y"))
    HnbFileName = "f%s.dat" % (now.strftime("%d%m%y"))
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
    print "--- HNB ---\nName\tMean Rate"
    try:
        HnbFile = open(FileName, "r")
    except IOError, e:
        print "Got IOError, '%s: %s'" % (e.errno, e.strerror)
    else:
        HeaderLine = HnbFile.readline()
        for elem in HnbFile:
            elem = elem.strip()
            column = elem.split()

            if Currency == 'all':
                print "%s\t%s" % (str(column[0])[3:6], column[2])
            elif Currency == str(column[0])[3:6]:
                print "%s\t%s" % (str(column[0])[3:6], column[2])

        HnbFile.close()


def getPBZData(FileName, Currency):
    """
    Print out data from PBZ
    """
    print "--- PBZ ---\nName\tMean Rate"
    try:
        doc = minidom.parse(FileName)
    except IOError, e:
        print "Got IOError, '%s: %s'" % (e.errno, e.strerror)
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
                        print "%s\t%s" % (ValName, ValMeanRate)
                    elif Currency == ValName:
                        print "%s\t%s" % (ValName, ValMeanRate)


def RemoveDataFiles():
    """
    Function for removing the downloaded data files
    """
    now = datetime.datetime.now()
    HnbFileName = "f%s.dat" % (now.strftime("%d%m%y"))
    PBZFileName = 'PBZteclist.xml'
    FileNames = [HnbFileName, PBZFileName]

    for DataFile in FileNames:
        if os.path.isfile(DataFile) and os.access(DataFile, os.W_OK):
            try:
                os.remove(DataFile)
                print "Removing %s..." % DataFile
            except OSError, e:
                print "Got OSError, '%s: %s'" % (e.errno, e.strerror)


def doit():
    """
    Set up the available program options
    Call the proper functions with proper parameters depending on user
    input
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all', help='Show values for all available \
            currencies', action="store_true")
    parser.add_argument('-c', '--currency', help='Set the currency for which \
            the value is shown', type=str)
    parser.add_argument('-r', '--reset', help='Remove the data files that \
            have been downloaded', action="store_true")

    args = parser.parse_args()

    if args.all:
        getPBZDataFile('all')
        getHNBDataFile('all')
    elif args.currency:
        getPBZDataFile(args.currency)
        getHNBDataFile(args.currency)
    elif args.reset:
        RemoveDataFiles()


if __name__ == "__main__":
    doit()
