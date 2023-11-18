import json
import sys
from ipaddress import IPv4Address, IPv4Network, AddressValueError
from pathlib import Path

with open(Path.cwd() / "res" / "ip2asn_v4.json", "r", encoding="utf-8") as js:
    ip2asn_v4 = json.load(js)


def ip2asn_find(ip: str) -> tuple:
    global ip2asn_v4
    try:
        for cidr in ip2asn_v4:
            if IPv4Address(ip) in IPv4Network(cidr):
                return (ip2asn_v4[cidr].get("asn"), ip2asn_v4[cidr].get("c_code"), ip2asn_v4[cidr].get("country"),
                        ip2asn_v4[cidr].get("owner"), cidr)
    except AddressValueError:
        print("Bad IP")
        exit(0)


def main(ip: str) -> None:
    data = dict()
    asn, c_code, country, owner, cidr = ip2asn_find(ip)
    data.update({"asn": asn, "country_code": c_code, "country": country, "owner": owner, "cidr": cidr})
    print(data)


if __name__ == "__main__":
    try:
        param = sys.argv[1]
        main(param)
    except IndexError:
        print("No IP address")
    exit(0)
