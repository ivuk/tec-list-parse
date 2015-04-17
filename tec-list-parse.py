#!/usr/bin/env python3


from xml.dom import minidom
import urllib.request
import datetime
import os
import argparse


def getHNBData(Currency):
    """
    Print out data from HNB
    """
    now = datetime.datetime.now()
    HnbFileName = "f{}.dat".format(now.strftime("%d%m%y"))
    HnbUrl = "http://www.hnb.hr/tecajn/{}".format(HnbFileName)

    print("--- HNB ---\nName\tMean Rate")

    with urllib.request.urlopen(HnbUrl) as Url:
        HeaderLine = Url.readline().decode('utf-8')
        for elem in Url:
            elem = elem.strip().decode('utf-8')
            column = elem.split()

            if Currency == 'all':
                print("{}\t{}".format(str(column[0])[3:6], column[2]))
            elif Currency == str(column[0])[3:6]:
                print("{}\t{}".format(str(column[0])[3:6], column[2]))


def getPBZData(Currency):
    """
    Print out data from PBZ
    """
    PBZUrl = 'http://www.pbz.hr/Downloads/PBZteclist.xml'

    print("--- PBZ ---\nName\tMean Rate")

    with urllib.request.urlopen(PBZUrl) as Url:
        doc = minidom.parse(Url)
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

    args = parser.parse_args()

    if not args.All and not args.currency:
        parser.print_help()

    if args.All:
        getPBZData('all')
        getHNBData('all')
    elif args.currency:
        getPBZData(args.currency)
        getHNBData(args.currency)


if __name__ == "__main__":
    doit()
