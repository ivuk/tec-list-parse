#!/usr/bin/env python
# vim: set ts=4 expandtab:

from xml.dom import minidom
import urllib2

def getDataFile(param):
    DataFile = urllib2.urlopen(param)
    Output = open('PBZteclist.xml','wb')
    Output.write(DataFile.read())
    Output.close()

def getData(param):
    """
    Print out data
    """
    doc = minidom.parse(param)
    currencies = doc.getElementsByTagName("Currency")

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
