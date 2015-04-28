#!/usr/bin/env python3


import argparse
from collections import OrderedDict
import datetime
import urllib.request
from xml.dom import minidom


def getHNBData(Currency):
    """
    Get the required data from HNB's website
    Print out the data
    """
    now = datetime.datetime.now()
    HnbFileName = "f{}.dat".format(now.strftime("%d%m%y"))
    HnbUrl = "http://www.hnb.hr/tecajn/{}".format(HnbFileName)

    print("--- HNB ---\nName\tMean Rate")

    with urllib.request.urlopen(HnbUrl) as Url:
        # Skip the header line
        Url.readline()
        for elem in Url:
            elem = elem.strip().decode('utf-8')
            column = elem.split()

            if Currency == 'all':
                print("{}\t{}".format(str(column[0])[3:6], column[2]))
            elif Currency == str(column[0])[3:6]:
                print("{}\t{}".format(str(column[0])[3:6], column[2]))


def getPBZData(Currency):
    """
    Get the required data from PBZ's website
    Print out the data
    """
    PBZUrl = 'http://www.pbz.hr/Downloads/PBZteclist.xml'

    print("--- PBZ ---\nName\tMean Rate")

    with urllib.request.urlopen(PBZUrl) as Url:
        doc = minidom.parse(Url)
        currencies = doc.getElementsByTagName("Currency")

        currency_name = [elem.getElementsByTagName('Name')[0].firstChild.data
                         for elem in currencies]
        currency_value = \
            [elem.getElementsByTagName('MeanRate')[0].firstChild.data
             for elem in currencies]

        """
        # This is neater, but uses ordinary dict()
        currency_list = \
            {elem.getElementsByTagName('Name')[0].firstChild.data:
             elem.getElementsByTagName('MeanRate')[0].firstChild.data
             for elem in currencies}
        for name, value in currency_list.items():
            print("{}\t{}".format(name, value))
        """

        currency_list = OrderedDict(zip(currency_name, currency_value))

        for name, value in currency_list.items():
            if Currency == 'all':
                print("{}\t{}".format(name, value))
            elif Currency == name:
                print("{}\t{}".format(name, value))


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
    parser.add_argument('-s' '--source', help='Set the source from which the \
            data is retrieved', type=str, dest='source')

    args = parser.parse_args()

    if not args.All and not args.currency and not args.source:
        parser.print_help()

    if args.All and not args.source:
        getPBZData('all')
        getHNBData('all')
    elif args.All and args.source:
        if args.source == 'HNB':
            getHNBData('all')
        if args.source == 'PBZ':
            getPBZData('all')
    elif args.currency and not args.source:
        getPBZData(args.currency)
        getHNBData(args.currency)
    elif args.currency and args.source:
        if args.source == 'HNB':
            getHNBData(args.currency)
        if args.source == 'PBZ':
            getPBZData(args.currency)


if __name__ == "__main__":
    doit()
