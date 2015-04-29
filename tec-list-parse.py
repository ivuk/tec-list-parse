#!/usr/bin/env python3


import argparse
from collections import OrderedDict
from datetime import datetime
from urllib.request import urlopen
from xml.dom import minidom


def get_hnb_data(currency):
    '''
    Get the required data from HNB's website
    Print out the data
    '''
    now = datetime.now()
    hnb_file_name = 'f{}.dat'.format(now.strftime('%d%m%y'))
    hnb_url = 'http://www.hnb.hr/tecajn/{}'.format(hnb_file_name)

    print('--- HNB ---\nName\tMean Rate')

    with urlopen(hnb_url) as Url:
        # Skip the header line
        Url.readline()
        for elem in Url:
            column = elem.strip().decode('utf-8').split()

            if currency == 'all':
                print('{}\t{}'.format(str(column[0])[3:6], column[2]))
            elif currency == str(column[0])[3:6]:
                print('{}\t{}'.format(str(column[0])[3:6], column[2]))


def get_pbz_data(currency):
    '''
    Get the required data from PBZ's website
    Print out the data
    '''
    pbz_url = 'http://www.pbz.hr/Downloads/PBZteclist.xml'

    print('--- PBZ ---\nName\tMean Rate')

    with urlopen(pbz_url) as Url:
        doc = minidom.parse(Url)
        currencies = doc.getElementsByTagName('Currency')

        currency_name = [elem.getElementsByTagName('Name')[0].firstChild.data
                         for elem in currencies]
        currency_value = \
            [elem.getElementsByTagName('MeanRate')[0].firstChild.data
             for elem in currencies]

        '''
        # This is neater, but uses ordinary dict()
        currency_list = \
            {elem.getElementsByTagName('Name')[0].firstChild.data:
             elem.getElementsByTagName('MeanRate')[0].firstChild.data
             for elem in currencies}
        for name, value in currency_list.items():
            print('{}\t{}'.format(name, value))
        '''

        currency_list = OrderedDict(zip(currency_name, currency_value))

        for name, value in currency_list.items():
            if currency == 'all':
                print('{}\t{}'.format(name, value))
            elif currency == name:
                print('{}\t{}'.format(name, value))


def get_erste_data(currency):
    '''
    Get the required data from Erste's website
    Print out the data
    '''
    now = datetime.now()
    erste_file_name = 'TL_{}.xml'.format(now.strftime('%Y%m%d'))
    erste_url = 'http://local.erstebank.hr/alati/SaveAsXML.aspx?ime={}'.format(
        erste_file_name)

    print('--- ERSTE ---\nName\tMean Rate')

    with urlopen(erste_url) as Url:
        doc = minidom.parse(Url)
        currencies = doc.getElementsByTagName('valuta')
        currency_name = [elem.getElementsByTagName('opis')[0].firstChild.data
                         for elem in currencies]
        currency_value = [elem.getElementsByTagName('t3')[0].firstChild.data
                          for elem in currencies]

    currency_list = OrderedDict(zip(currency_name, currency_value))

    for name, value in currency_list.items():
        if currency == 'all':
            print('{}\t{}'.format(name, value))
        elif currency == name:
            print('{}\t{}'.format(name, value))


def doit():
    '''
    Set up the available program options
    Call the proper functions with proper parameters depending on user
    input
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all', help='Show values for all available \
            currencies', action='store_true', dest='all')
    parser.add_argument('-c', '--currency', help='Set the currency for which \
            the value is shown', type=str, dest='currency')
    parser.add_argument('-s' '--source', help='Set the source from which the \
            data is retrieved', type=str, dest='source')

    args = parser.parse_args()

    if not args.all and not args.currency and not args.source:
        parser.print_help()

    if args.all and not args.source:
        get_pbz_data('all')
        get_erste_data('all')
        get_hnb_data('all')
    elif args.all and args.source:
        if args.source.lower() == 'HNB'.lower():
            get_hnb_data('all')
        if args.source.lower() == 'PBZ'.lower():
            get_pbz_data('all')
        if args.source.lower() == 'ERSTE'.lower():
            get_erste_data('all')
    elif args.currency and not args.source:
        get_pbz_data(args.currency)
        get_erste_data(args.currency)
        get_hnb_data(args.currency)
    elif args.currency and args.source:
        if args.source.lower() == 'HNB'.lower():
            get_hnb_data(args.currency)
        if args.source.lower() == 'PBZ'.lower():
            get_pbz_data(args.currency)
        if args.source.lower() == 'ERSTE'.lower():
            get_erste_data(args.currency)


if __name__ == '__main__':
    doit()
