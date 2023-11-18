import csv
from ipaddress import IPv4Address, summarize_address_range
import json

from tools.ip2asn_base import create_base, save_base

ip2asn = []

with open("country_code.json", "r", encoding="utf-8") as js:
    ccode = json.load(js)


def converter(start_ip, end_ip):
    return [ipaddr for ipaddr in summarize_address_range(IPv4Address(start_ip), IPv4Address(end_ip))]


def dict_update(data):
    global ip2asn
    start_ip, end_ip, asn, c_code, owner = data
    print(owner)
    cidr = str(converter(start_ip, end_ip)[0])
    country = ccode.get(c_code)
    if not country:
        country = "None"
    ip2asn.append((cidr, asn, c_code, country, owner))


def main():
    global ip2asn
    create_base()
    path = input("path tsv >>> ").replace('"', '').replace("'", "")
    with open(path, "r", encoding="utf-8") as tsv:
        data = csv.reader(tsv, delimiter="\t")
        for dt in data:
            dict_update(tuple(dt))
            if len(ip2asn) == 10000:
                save_base(ip2asn)
                ip2asn.clear()
        if 0 < len(ip2asn) < 10000:
            save_base(ip2asn)
            ip2asn.clear()


if __name__ == "__main__":
    main()
