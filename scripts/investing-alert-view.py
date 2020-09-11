#!/usr/bin/env python3


import os
import sys
import json
from collections import defaultdict
from termcolor import colored, cprint

def usage(script):
    print("[Usage] {} filename".format(script))

def parse_jsonfile(filename):
    alerts = defaultdict(lambda: defaultdict(list))
    with open(filename, 'r') as freader:
        content = json.load(freader)
        for alert in content:
            if not alerts[alert['pairId']]:
                alerts[alert['pairId']]['pairName'] = alert['pairName']
            alerts[alert['pairId']][alert['threshold']].append(alert)

    return alerts


def pretty_print_alerts(alerts, filter_only=[]):
    for pair_id, pair_alerts in alerts.items():
        if not filter_only or pair_id in filter_only:
            cprint(colored("  ++++++++++++++++++++++++++++++".format(pair_alerts['pairName'])), 'cyan')
            cprint(colored("  ++++++    ", 'cyan') + colored(pair_alerts['pairName'], 'yellow'))
            cprint(colored("  ++++++++++++++++++++++++++++++".format(pair_alerts['pairName']), 'cyan'))
            alerts_over = sorted(pair_alerts["over"], key=lambda k: k["value"])
            alerts_under = sorted(pair_alerts["under"], key=lambda k: -k["value"])
            for i in range(0, max([len(alerts_over), len(alerts_under)])):
                price_over = str(alerts_over[i]['value']).replace(',', '') if i < len(alerts_over) else '-----'
                price_under = str(alerts_under[i]['value']).replace(',', '') if i < len(alerts_under) else '-----'
                cprint(colored("    {: <10}".format(price_under), 'red') + " / " +
                       colored("{: >10}".format(price_over), 'green'))
            print("")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        alerts = parse_jsonfile(sys.argv[1])
        if len(sys.argv) > 2 and sys.argv[2]:
            pretty_print_alerts(alerts, [int(x) for x in sys.argv[2].split(',')])
        else:
            pretty_print_alerts(alerts)
    else:
        usage(sys.argv[0])
