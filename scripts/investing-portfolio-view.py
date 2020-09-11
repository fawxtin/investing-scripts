#!/usr/bin/env python3


import os
import sys
import json
from collections import defaultdict
from termcolor import colored

"""
Colorize text.

Available text colors:
red, green, yellow, blue, magenta, cyan, white.
Available text highlights:
on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.
Available attributes:
bold, dark, underline, blink, reverse, concealed.
Example:
colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink']) colored('Hello, World!', 'green')
"""

def usage(script):
    print("[Usage] {} filename".format(script))

def parse_jsonfile(filename):
    with open(filename, 'r') as freader:
        return json.load(freader)


def print_row(row): # transform this function into a colored one!
    print("{: >15} {: >15} {: >15} {: >15} {: >15} {: >15} {: >15}".format(*row))


def pretty_print_portfolio(pairs):
    # header
    print_row(['----------', '----------', '----------', '----------', '----------', '----------', '----------'])
    print_row(['Symbol/Name', 'Price', 'Open', 'High', 'Low', 'Change', 'Volume'])
    print_row(['----------', '----------', '----------', '----------', '----------', '----------', '----------'])
    for pair in pairs:
        print_row([pair['pairSymbol'] or pair['pairName'],
                   pair['priceLast'], pair['priceOpen'], pair['priceHigh'], pair['priceLow'],
                   pair['priceChange'], pair['volume']])
    print_row(['----------', '----------', '----------', '----------', '----------', '----------', '----------'])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        prices = parse_jsonfile(sys.argv[1])
        pretty_print_portfolio(prices)
    else:
        usage(sys.argv[0])


"""
MQn4zhnOYFzbqVEu6nB62A==

wss://stream204.forexpros.com/echo/068/nm0ipxsd/websocket


Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,pt;q=0.8
Cache-Control: no-cache
Connection: Upgrade
Host: stream204.forexpros.com
Origin: https://www.investing.com
Pragma: no-cache
Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits
Sec-WebSocket-Key: MQn4zhnOYFzbqVEu6nB62A==
Sec-WebSocket-Version: 13
Upgrade: websocket
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36



[			 {"_event":"bulk-subscribe","tzID":8,"message":"pid-8874:%%pid-8884:%%pid-166:%%pid-525:%%pid-8839:%%pid-169:%%pid-17920:%%pid-941612:%%pid-13666:%%pid-8867:%%pid-172:%%pid-8826:%%pid-8838:%%pid-40820:%%pid-8984:%%pid-8859:%%pid-8830:%%pid-9227:%%pid-8836:%%pid-8910:%%pid-8883:%%pid-44657:%%pid-8827:%%pid-956731:%%pid-1010796:%%pid-997650:%%pid-1:%%pid-9:%%pid-6:%%pid-11:%%pid-2:%%pid-3:%%pid-155:%%pid-2111:%%pid-961728:%%pid-2186:%%pid-2103:%%pid-8916:%%pid-8917:%%pid-8918:%%pid-8849:%%pid-8833:%%pid-8862:%%pid-8831:%%pid-956470:%%pid-49768:%%pid-49784:%%pid-27604:%%pid-20063:%%pid-44794:%%pid-18599:%%pid-18604:%%pid-18606:%%pid-18666:%%pid-18667:%%pid-18669:%%pid-18706:%%pid-18707:%%pid-18708:%%pid-18749:%%pid-18750:%%pid-18770:%%pid-18775:%%pid-18814:%%pid-18815:%%pid-50516:%%pidExt-8874:%%pidExt-8884:%%pidExt-166:%%pidExt-525:%%pidExt-8839:%%pidExt-169:%%pidExt-17920:%%pidExt-941612:%%pidExt-13666:%%pidExt-8867:%%pidExt-172:%%pidExt-8826:%%pidExt-8838:%%pidExt-40820:%%pidExt-8984:%%pidExt-8859:%%pidExt-8830:%%pidExt-9227:%%pidExt-8836:%%pidExt-8910:%%pidExt-8883:%%pidExt-44657:%%pidExt-8827:%%pidExt-956731:%%pidExt-1010796:%%pidExt-997650:%%pidExt-1:%%pidExt-9:%%pidExt-6:%%pidExt-11:%%pidExt-2:%%pidExt-3:%%pidExt-155:%%pidExt-2111:%%pidExt-961728:%%pidExt-2186:%%pidExt-2103:%%pidExt-8916:%%pidExt-8917:%%pidExt-8918:%%pidExt-8849:%%pidExt-8833:%%pidExt-8862:%%pidExt-8831:%%pidExt-956470:%%pidExt-49768:%%pidExt-49784:%%pidExt-27604:%%pidExt-20063:%%pidExt-44794:%%pidExt-18599:%%pidExt-18604:%%pidExt-18606:%%pidExt-18666:%%pidExt-18667:%%pidExt-18669:%%pidExt-18706:%%pidExt-18707:%%pidExt-18708:%%pidExt-18749:%%pidExt-18750:%%pidExt-18770:%%pidExt-18775:%%pidExt-18814:%%pidExt-18815:%%pidExt-50516:"} ]


			 ["{"_event":"heartbeat","data":"h"}"]

"""
