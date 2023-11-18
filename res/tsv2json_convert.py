import csv
from ipaddress import IPv4Address, summarize_address_range
import json

ip2asn = dict()

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
    if cidr not in ip2asn:
        ip2asn[cidr] = dict()
    ip2asn[cidr].update({"asn": asn, "c_code": c_code, "country": country, "owner": owner})


def main():
    global ip2asn
    with open("ip2asn-v4.tsv", "r", encoding="utf-8") as tsv:
        data = csv.reader(tsv, delimiter="\t")
        for dt in data:
            dict_update(tuple(dt))
    with open("ip2asn_v4.json", "w", encoding="utf-8") as jsn:
        json.dump(ip2asn, jsn, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
