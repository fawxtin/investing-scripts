#!/usr/bin/env python3

from time import sleep
import sys
import os
import random
import threading
from glob import glob
import curses
from collections import defaultdict
import json
import websocket
from queue import Queue

"""
https://finnhub.io/api/v1/forex/exchange?token=
https://finnhub.io/api/v1/forex/symbol?exchange=oanda&token=


NDA0YmUyM2Y0am1kNWM0MQ== <- portfolio forex
Z2NiNGYyN2k0amtlYzE1MA== <- portfolio indexes
"""

tmp_dir = os.environ['HOME'] + "/tmp/scrapy/"
tmp_files = glob(tmp_dir + "investing.com_portfolio*.json")

grid = defaultdict(lambda: dict(pair=dict(), order=0)) # by pairId
grid_header_offset = 2

token = os.environ.get('FINNHUB_IO_TOKEN')
queue_info_pairs = Queue()


def parse_jsonfile(filename):
    with open(filename, 'r') as freader:
        return json.load(freader)

def mount_grid(grid, content):
    max_order = max([x['order'] for x in grid.values()] or [0]) + grid_header_offset
    for pair in content:
        if pair['pairId'] in grid: # update grid row values
            grid[pair['pairId']]['pair'] = pair
        else: # add new row
            max_order += 1
            grid[pair['pairId']]['order'] = max_order
            grid[pair['pairId']]['pair'] = pair

##
## TODO: move these functions to a websocket class, thread stuff too!
##
def on_message(ws, message):
    refresh = False
    msg_obj = json.loads(message)
    if msg_obj.get('type', '') == 'trade':
        queue_info_pairs.put(msg_obj)
    else:
        queue_info_pairs.put(msg_obj)

def on_error(ws, error):
    queue_info_pairs.put({"message": error, "type": "error"})

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    subscriptions = "subcriptions: "
    for pair_id in grid.keys():
        subscription = '{"type":"subscribe","symbol":"FXPRO:' + str(pair_id) + '"}'
        subscriptions += subscription
        ws.send(subscription)
    queue_info_pairs.put({"message": subscriptions, "type": "subscription"})


def main(stdscr):
    def string_row(row):
        return "| {: >15} | {: >15} | {: >15} | {: >15} | {: >15} | {: >15} | {: >15} | {: >15} |".format(*row)

    def grid_print(line, elements, key_seq=[]):
        if type(elements) == list: # header?
            stdscr.addstr(line, 0, string_row(elements), curses.color_pair(1))
        elif type(elements) == dict or type(elements) == defaultdict:
            cidx = 0
            col_sep = "|"
            row_color = curses.color_pair(0)
            if (line % 2) == 0:
                row_color = curses.color_pair(2)
            stdscr.addstr(line, cidx, col_sep + " ", row_color)
            cidx += 2
            for key in key_seq:
                col_value = ""
                if type(key) == tuple:
                    value = "-"
                    for k in key:
                        if elements.get(k, ''):
                            value = elements[k]
                            break
                    col_value = "{: >15}".format(value)
                    stdscr.addstr(line, cidx, col_value, row_color)
                elif type(key) == dict:
                    col_value = "{: >15}".format(elements.get(key['key']))
                    if key.get('effect'):
                        stdscr.addstr(line, cidx, col_value, key.get('effect') | row_color)
                    else:
                        stdscr.addstr(line, cidx, col_value, row_color)
                else:
                    col_value = "{: >15}".format(elements.get(key, "-"))
                    stdscr.addstr(line, cidx, col_value, row_color)
                cidx += 15
                stdscr.addstr(line, cidx, " " + col_sep + " ", row_color)
                cidx += 3

    def print_grid_element(element):
        pair = element['pair']
        price = pair['priceLast']
        if type(price) == str:
            price = price.replace(',', '')
        pair['priceLast'] = '{:,.4f}'.format(float(price))
        if element['order'] < 50:
            grid_print(element['order'], pair, 
                       [('pairSymbol', 'pairName'), 'priceLast',
                        {"key": 'pricePrev', "effect": curses.A_DIM},
                        'priceOpen', 'priceHigh', 'priceLow',
                        'priceChange', 'volume'])
        
    def parse_message(message):
        if message.get("type", "") == "trade":
            for msg in message.get("data", []):
                pair_symbol = msg.get('s', '').split(':')
                if len(pair_symbol) == 2:
                    grid_pair = int(pair_symbol[1])
                    if grid_pair in grid:
                        grid[grid_pair]['pair']['priceLast'] = msg['p']
                        print_grid_element(grid[grid_pair])

    if len(sys.argv) == 1:
        sys.exit(1)
    
    tmp_portfolio_file = sys.argv[1]
    content = parse_jsonfile(tmp_portfolio_file)

    stdscr.clear()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)

    grid_print(0, ['---------------'] * 8)
    grid_print(1, ['Symbol/Name', 'Price', 'Prev', 'Open', 'High', 'Low', 'Change', 'Volume'])
    grid_print(2, ['---------------'] * 8)

    
    mount_grid(grid, content)
    for element in grid.values():
        print_grid_element(element)
    stdscr.refresh()
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=" + token,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    wst = threading.Thread(target=ws.run_forever)
    wst.setDaemon(True)
    wst.start()
    count = 0
    while True:
        while queue_info_pairs.empty() == False:
            message = queue_info_pairs.get()
            parse_message(message)

        count += 1
        stdscr.refresh()
        sleep(3)


if __name__ == '__main__':
    curses.wrapper(main)

