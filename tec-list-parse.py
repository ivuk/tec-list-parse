#!/usr/bin/env python3


import argparse
from collections import OrderedDict
from datetime import datetime
from urllib.request import urlopen
from xml.dom import minidom


rate_titles = ['Buy', 'Mean', 'Sell']


def get_hnb_data(currency, rate_type):
    '''
    Get the required data from HNB's website
    Print out the data
    '''
    now = datetime.now()
    hnb_file_name = 'f{}.dat'.format(now.strftime('%d%m%y'))
    hnb_url = 'http://www.hnb.hr/tecajn/{}'.format(hnb_file_name)

    with urlopen(hnb_url) as url:
        # Skip the header line
        url.readline()
        hnb_data = [elem.strip().decode('utf-8').split() for elem in url]

    print('--- HNB ---\nName\t{} Rate'.format(rate_titles[rate_type]))

    for elem in hnb_data:
        if currency == 'all':
            print('{}\t{}'.format(str(elem[0])[3:6],
                                  elem[rate_type + 1]))
        elif currency.lower() == str(elem[0])[3:6].lower():
            print('{}\t{}'.format(str(elem[0])[3:6],
                                  elem[rate_type + 1]))


def get_pbz_data(currency, rate_type):
    '''
    Get the required data from PBZ's website
    Print out the data
    '''
    rate_types = ['BuyRateForeign', 'MeanRate', 'SellRateForeign']

    pbz_url = 'http://www.pbz.hr/Downloads/PBZteclist.xml'


    with urlopen(pbz_url) as url:
        doc = minidom.parse(url)
        currencies = doc.getElementsByTagName('Currency')

        currency_name = [elem.getElementsByTagName('Name')[0].firstChild.data
                         for elem in currencies]
        currency_value = \
            [elem.getElementsByTagName(rate_types[rate_type])[0].firstChild.data
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

    print('--- PBZ ---\nName\t{} Rate'.format(rate_titles[rate_type]))

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
    rate_types = ['t1', 't2', 't3']

    now = datetime.now()
    erste_file_name = 'TL_{}.xml'.format(now.strftime('%Y%m%d'))
    erste_url = 'http://local.erstebank.hr/alati/SaveAsXML.aspx?ime={}'.format(
        erste_file_name)

    with urlopen(erste_url) as url:
        doc = minidom.parse(url)
        currencies = doc.getElementsByTagName('valuta')
        currency_name = [elem.getElementsByTagName('opis')[0].firstChild.data
                         for elem in currencies]
        currency_value = [elem.getElementsByTagName(
            rate_types[rate_type])[0].firstChild.data for elem in currencies]

    currency_list = OrderedDict(zip(currency_name, currency_value))

    print('--- ERSTE ---\nName\t{} Rate'.format(rate_titles[rate_type]))

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
    parser.add_argument('-r', '--rate', help='Set the currency rate type for \
            which the value is shown', type=str, dest='rate_type',
                        default='mean')
    parser.add_argument('-s' '--source', help='Set the source from which the \
            data is retrieved', type=str, dest='source')

    args = parser.parse_args()

    if not args.all and not args.currency and not args.source:
        parser.print_help()

    if args.rate_type.lower() == 'buy':
        rate_type = 0
    elif args.rate_type.lower() == 'sell':
        rate_type = 2
    else:
        rate_type = 1

    if args.all and not args.source:
        get_pbz_data('all', rate_type)
        get_erste_data('all', rate_type)
        get_hnb_data('all', rate_type)
    elif args.all and args.source:
        if args.source.lower() == 'hnb':
            get_hnb_data('all', rate_type)
        if args.source.lower() == 'pbz':
            get_pbz_data('all', rate_type)
        if args.source.lower() == 'erste':
            get_erste_data('all', rate_type)
    elif args.currency and not args.source:
        get_pbz_data(args.currency, rate_type)
        get_erste_data(args.currency, rate_type)
        get_hnb_data(args.currency, rate_type)
    elif args.currency and args.source:
        if args.source.lower() == 'hnb':
            get_hnb_data(args.currency, rate_type)
        if args.source.lower() == 'pbz':
            get_pbz_data(args.currency, rate_type)
        if args.source.lower() == 'erste':
            get_erste_data(args.currency, rate_type)


if __name__ == '__main__':
    doit()
