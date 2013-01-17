#!/usr/bin/env python
# vim: set ts=4 expandtab:

from xml.dom import minidom
import urllib2
import datetime


def getHNBFile():
    """
    Get the required data file from HNB
    """
    now = datetime.datetime.now()
    HnbUrl = "http://www.hnb.hr/tecajn/f%s.dat" % (now.strftime("%d%m%y"))
    HnbFileName = "f%s.dat" % (now.strftime("%d%m%y"))
    DataFile = urllib2.urlopen(HnbUrl)
    Output = open(HnbFileName, 'wb')
    Output.write(DataFile.read())
    Output.close()


def getDataFile(param):
    """
    Get the required data file from PBZ
    """
    DataFile = urllib2.urlopen(param)
    Output = open('PBZteclist.xml', 'wb')
    Output.write(DataFile.read())
    Output.close()


def getHNBData():
    """
    Print out data from HNB
    """
    now = datetime.datetime.now()
    HnbFileName = "f%s.dat" % (now.strftime("%d%m%y"))

    print "--- HNB ---"
    HnbFile = open(HnbFileName, "r")
    HeaderLine = HnbFile.readline()
    for elem in HnbFile:
        elem = elem.strip()
        column = elem.split()
        print "%s %s" % (str(column[0])[3:6], column[2])
    HnbFile.close()


def getData(param):
    """
    Print out data from PBZ
    """
    doc = minidom.parse(param)
    currencies = doc.getElementsByTagName("Currency")

    print "--- PBZ ---"
    for elem in currencies:
        currname = elem.getElementsByTagName('Name')
        currval = elem.getElementsByTagName('MeanRate')
        for elem in currname:
            ValName = elem.childNodes[0].nodeValue
            for elem in currval:
                ValMeanRate = elem.childNodes[0].nodeValue
                print "%s %s" % (ValName, ValMeanRate)

if __name__ == "__main__":
    SourceUrl = 'http://www.pbz.hr/Downloads/PBZteclist.xml'
    getDataFile(SourceUrl)
    getData('PBZteclist.xml')
    getHNBFile()
    getHNBData()
