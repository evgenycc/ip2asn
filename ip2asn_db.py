import json
import sys
from pprint import pprint

from tools.base_query import ip2asn_find, asn_find, owner_find, ccode_find, help_msg


def save_data(data: dict, item: str) -> None:
    with open(f"{item}_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    try:
        param = sys.argv[1]
        if param == "-i":
            ip_addr = sys.argv[2]
            pprint(ip2asn_find(ip_addr))
        elif param == "-a":
            asn_a = sys.argv[2]
            pprint(asn_find(asn_a))
        elif param == "-o":
            owner_a = sys.argv[2]
            pprint(owner_find(owner_a))
        elif param == "-c":
            ccode = sys.argv[2]
            pprint(ccode_find(ccode))
        elif param == "-is":
            ip_addr = sys.argv[2]
            data_d = ip2asn_find(ip_addr)
            pprint(data_d)
            if type(data_d) is dict:
                save_data(data_d, f"ip_{ip_addr}")
        elif param == "-as":
            asn_a = sys.argv[2]
            data_d = asn_find(asn_a)
            pprint(data_d)
            if type(data_d) is dict:
                save_data(data_d, f"asn_{asn_a}")
        elif param == "-os":
            owner_a = sys.argv[2]
            data_d = owner_find(owner_a)
            pprint(data_d)
            if type(data_d) is dict:
                save_data(data_d, f"owner_{owner_a}")
        elif param == "-cs":
            ccode = sys.argv[2]
            data_d = ccode_find(ccode)
            pprint(data_d)
            if type(data_d) is dict:
                save_data(data_d, f"ccode_{ccode}")
        elif param == "-h":
            help_msg()
        else:
            print("Key is Bad")
            print('Enter the "-h" key for help. Example: python ip2asn_db.py -h')
            exit(0)
    except IndexError:
        print("No Param")
        print('Enter the "-h" key for help. Example: python ip2asn_db.py -h')
        exit(0)
