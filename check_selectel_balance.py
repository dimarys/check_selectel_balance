#!/usr/bin/env python3
"""Selectel balance Nagios sensor."""

import sys
import argparse
import requests


def do_check_selectel_balance(api_token, service_name, days_warning, days_critical):
    """Check Selectel balance."""
    response = requests.get("https://api.selectel.ru/v3/billing/balance?billing={}&with_prediction=1".format(
        service_name), headers={"X-Token": api_token})
    if response.status_code != 200:
        print("API error code {}.".format(response.status_code))
        return 2
    data = response.json()
    days_left = data['data'][service_name]['prediction']['days']
    if days_left <= days_critical:
        print("CRITICAL: {} days left".format(days_left))
        return 2
    elif days_left <= days_warning:
        print("WARNING: {} days left".format(days_left))
        return 1
    else:
        print("OK: {} days left".format(days_left))
    return 0


def main():
    """Main."""
    parser = argparse.ArgumentParser(description='Nagios check of Selectel balance.')
    parser.add_argument('-t', '--token', help='Selectel API Token', required=True)
    parser.add_argument('-s', '--service', help='Type of service (primary, storage, vmware, vpc)', required=True,
                        choices=('primary', 'storage', 'vmware', 'vpc'))
    parser.add_argument('-w', '--warning', help='Number of predicated days until warning', type=int, required=True)
    parser.add_argument('-c', '--critical', help='Number of predicted days until critical', type=int, required=True)
    args = parser.parse_args()
    sys.exit(do_check_selectel_balance(args.token, args.service, args.warning, args.critical))


if __name__ == "__main__":
    main()
