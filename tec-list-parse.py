#!/usr/bin/env python3


import argparse
from collections import OrderedDict
from datetime import datetime
from urllib.request import urlopen
from xml.dom import minidom


def get_hnb_data(currency, rate_type):
    '''
    Get the required data from HNB's website
    Print out the data
    '''
    if rate_type.lower() == 'buy':
        hnb_rate_type = 1
        hnb_rate_title = 'Buy'
    elif rate_type.lower() == 'sell':
        hnb_rate_type = 3
        hnb_rate_title = 'Sell'
    else:
        hnb_rate_type = 2
        hnb_rate_title = 'Mean'

    now = datetime.now()
    hnb_file_name = 'f{}.dat'.format(now.strftime('%d%m%y'))
    hnb_url = 'http://www.hnb.hr/tecajn/{}'.format(hnb_file_name)

    print('--- HNB ---\nName\t{} Rate'.format(hnb_rate_title))

    with urlopen(hnb_url) as Url:
        # Skip the header line
        Url.readline()
        for elem in Url:
            column = elem.strip().decode('utf-8').split()

            if currency == 'all':
                print('{}\t{}'.format(str(column[0])[3:6],
                                      column[hnb_rate_type]))
            elif currency.lower() == str(column[0])[3:6].lower():
                print('{}\t{}'.format(str(column[0])[3:6],
                                      column[hnb_rate_type]))


def get_pbz_data(currency, rate_type):
    '''
    Get the required data from PBZ's website
    Print out the data
    '''
    if rate_type.lower() == 'buy':
        pbz_rate_type = 'BuyRateForeign'
        pbz_rate_title = 'Buy'
    elif rate_type.lower() == 'sell':
        pbz_rate_type = 'SellRateForeign'
        pbz_rate_title = 'Sell'
    else:
        pbz_rate_type = 'MeanRate'
        pbz_rate_title = 'Mean'

    pbz_url = 'http://www.pbz.hr/Downloads/PBZteclist.xml'

    print('--- PBZ ---\nName\t{} Rate'.format(pbz_rate_title))

    with urlopen(pbz_url) as Url:
        doc = minidom.parse(Url)
        currencies = doc.getElementsByTagName('Currency')

        currency_name = [elem.getElementsByTagName('Name')[0].firstChild.data
                         for elem in currencies]
        currency_value = \
            [elem.getElementsByTagName(pbz_rate_type)[0].firstChild.data
             for elem in currencies]

        '''
        # This is neater, but uses ordinary dict()
        currency_list = \
            {elem.getElementsByTagName('Name')[0].firstChild.data:
             elem.getElementsByTagName(pbz_rate_type)[0].firstChild.data
             for elem in currencies}
        for name, value in currency_list.items():
            print('{}\t{}'.format(name, value))
        '''

        currency_list = OrderedDict(zip(currency_name, currency_value))

        for name, value in currency_list.items():
            if currency == 'all':
                print('{}\t{}'.format(name, value))
            elif currency.lower() == name.lower():
                print('{}\t{}'.format(name, value))


def get_erste_data(currency, rate_type):
    '''
    Get the required data from Erste's website
    Print out the data
    '''
    if rate_type.lower() == 'buy':
        erste_rate_type = 't1'
        erste_rate_title = 'Buy'
    elif rate_type.lower() == 'sell':
        erste_rate_type = 't3'
        erste_rate_title = 'Sell'
    else:
        erste_rate_type = 't2'
        erste_rate_title = 'Mean'

    now = datetime.now()
    erste_file_name = 'TL_{}.xml'.format(now.strftime('%Y%m%d'))
    erste_url = 'http://local.erstebank.hr/alati/SaveAsXML.aspx?ime={}'.format(
        erste_file_name)

    print('--- ERSTE ---\nName\t{} Rate'.format(erste_rate_title))

    with urlopen(erste_url) as Url:
        doc = minidom.parse(Url)
        currencies = doc.getElementsByTagName('valuta')
        currency_name = [elem.getElementsByTagName('opis')[0].firstChild.data
                         for elem in currencies]
        currency_value = [elem.getElementsByTagName(erste_rate_type)[0].firstChild.data
                          for elem in currencies]

    currency_list = OrderedDict(zip(currency_name, currency_value))

    for name, value in currency_list.items():
        if currency == 'all':
            print('{}\t{}'.format(name, value))
        elif currency.lower() == name.lower():
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
    parser.add_argument('-t', '--type', help='Set the currency rate type for \
            which the value is shown', type=str, dest='rate_type', default='mean')
    parser.add_argument('-s' '--source', help='Set the source from which the \
            data is retrieved', type=str, dest='source')

    args = parser.parse_args()

    if not args.all and not args.currency and not args.source:
        parser.print_help()

    if args.all and not args.source:
        get_pbz_data('all', args.rate_type)
        get_erste_data('all', args.rate_type)
        get_hnb_data('all', args.rate_type)
    elif args.all and args.source:
        if args.source.lower() == 'HNB'.lower():
            get_hnb_data('all', args.rate_type)
        if args.source.lower() == 'PBZ'.lower():
            get_pbz_data('all', args.rate_type)
        if args.source.lower() == 'ERSTE'.lower():
            get_erste_data('all', args.rate_type)
    elif args.currency and not args.source:
        get_pbz_data(args.currency, args.rate_type)
        get_erste_data(args.currency, args.rate_type)
        get_hnb_data(args.currency, args.rate_type)
    elif args.currency and args.source:
        if args.source.lower() == 'HNB'.lower():
            get_hnb_data(args.currency, args.rate_type)
        if args.source.lower() == 'PBZ'.lower():
            get_pbz_data(args.currency, args.rate_type)
        if args.source.lower() == 'ERSTE'.lower():
            get_erste_data(args.currency, args.rate_type)


if __name__ == '__main__':
    doit()
