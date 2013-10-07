#!/usr/bin/env python

from xml.dom import minidom
import urllib2
import datetime


def getDataFile(Url, FileName):
    """
    Generic function for opening an URL and saving its content to file
    """
    try:
        DataFile = urllib2.urlopen(Url)
    except urllib2.URLError, e:
        print "Got URLError from urllib2, reason: %s" % e.reason
    else:
        Output = open(FileName, 'wb')
        Output.write(DataFile.read())
        Output.close()


def getHNBFile():
    """
    Get the required data file from HNB
    """
    now = datetime.datetime.now()
    HnbUrl = "http://www.hnb.hr/tecajn/f%s.dat" % (now.strftime("%d%m%y"))
    HnbFileName = "f%s.dat" % (now.strftime("%d%m%y"))
    getDataFile(HnbUrl, HnbFileName)
    getHNBData(HnbFileName)


def getPBZDataFile():
    """
    Get the required data file from PBZ
    """
    PBZUrl = 'http://www.pbz.hr/Downloads/PBZteclist.xml'
    getDataFile(PBZUrl, 'PBZteclist.xml')
    getPBZData('PBZteclist.xml')


def getHNBData(FileName):
    """
    Print out data from HNB
    """
    print "--- HNB ---"
    try:
        HnbFile = open(FileName, "r")
    except IOError, e:
        print "Got IOError, '%s: %s'" % (e.errno, e.strerror)
    else:
        HeaderLine = HnbFile.readline()
        for elem in HnbFile:
            elem = elem.strip()
            column = elem.split()
            print "%s %s" % (str(column[0])[3:6], column[2])
        HnbFile.close()


def getPBZData(FileName):
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
                    print "%s\t%s" % (ValName, ValMeanRate)

if __name__ == "__main__":
    getPBZDataFile()
    getHNBFile()
