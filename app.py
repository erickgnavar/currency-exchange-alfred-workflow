# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import re
import sys
import urllib2


API = 'https://free.currencyconverterapi.com/api/v6/convert?q={}&compact=y'
CURRENCIES = {}


with open('currencies.json') as f:
    # This is the content of request
    # https://free.currencyconverterapi.com/api/v6/currencies
    CURRENCIES = json.loads(f.read())['results']


def fetch_currency_factor(from_, to):
    key = '{}_{}'.format(from_, to).upper()
    url = API.format(key)
    try:
        response = urllib2.urlopen(url).read()
        data = json.loads(response)
        return data[key]['val']
    except Exception:
        return None


def parse_input(raw_str):
    regex = re.compile(r'(\d+)\ (\w+)\ to\ (\w+)')
    result = regex.search(query.strip().lower())
    if result:
        return result.groups()
    else:
        return None


def prepare_output(value, key):
    currency = CURRENCIES[key.upper()]
    title = '{} {}'.format(currency['currencySymbol'], str(value))
    return {
        'uid': currency['id'],
        'title': title,
        'subtitle': currency['currencyName'],
        'type': 'default',
        'icon': {
            'path': './icons/{}.png'.format(key.lower()),
        },
        'arg': value,
    }


final_result = {
    'items': [],
}

query = ' '.join(sys.argv[1:])

result = parse_input(query)

if result:
    (value, from_, to) = result
    factor = fetch_currency_factor(from_, to)
    if factor:
        res = float(value) * factor
        final_result['items'].append(prepare_output(res, to))

sys.stdout.write(json.dumps(final_result))
