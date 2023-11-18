import sqlite3
from ipaddress import IPv4Address, IPv4Network, AddressValueError
from pathlib import Path


def ip2asn_find(ip: str) -> (dict, str):
    data = dict()
    try:
        conn = sqlite3.connect(Path.cwd() / 'res' / 'ip2asn_v4.db')
        cur = conn.cursor()
        for row in cur.execute(f"SELECT * FROM ip2asn"):
            cidr = row[0]
            asn = row[1]
            c_code = row[2]
            country = row[3]
            owner = row[4]
            if IPv4Address(ip) in IPv4Network(cidr):
                data.update({"asn": asn, "country_code": c_code, "country": country, "owner": owner, "cidr": cidr})
                cur.close()
                conn.close()
                return data
        cur.close()
        conn.close()
        return "IP Not Found"
    except AddressValueError:
        return "Bad IP"


def asn_find(asn: str) -> (dict, str):
    data_asn = dict()
    conn = sqlite3.connect(Path.cwd() / 'res' / 'ip2asn_v4.db')
    cur = conn.cursor()
    try:
        select = f"SELECT * FROM ip2asn WHERE asn = ?"
        cur.execute(select, (asn, ))
        data = cur.fetchall()
        _, asn, c_code, country, owner = data[0]
        cidr = []
        for row in data:
            cidr.append(row[0])
        data_asn.update({asn: {"cidr": cidr, "country_code": c_code, "country": country, "owner": owner}})
        cur.close()
        conn.close()
        return data_asn if data_asn else "ASN Not Found"
    except TypeError:
        cur.close()
        conn.close()
        return "ASN Not Found"


def owner_find(owner: str) -> (dict, str):
    data_owner = dict()
    conn = sqlite3.connect(Path.cwd() / 'res' / 'ip2asn_v4.db')
    cur = conn.cursor()
    try:
        select = f"SELECT * FROM ip2asn WHERE owner = ?"
        cur.execute(select, (owner,))
        data = cur.fetchall()
        _, asn, c_code, country, owner = data[0]
        cidr = []
        for row in data:
            cidr.append(row[0])
        data_owner.update({owner: {"cidr": cidr, "asn": asn, "country_code": c_code, "country": country}})
        cur.close()
        conn.close()
        return data_owner if data_owner else "Owner Not Found"
    except TypeError:
        cur.close()
        conn.close()
        return "Owner Not Found"


def ccode_find(c_code: str) -> (dict, str):
    data_ccode = dict()
    conn = sqlite3.connect(Path.cwd() / 'res' / 'ip2asn_v4.db')
    cur = conn.cursor()
    try:
        select = f"SELECT * FROM ip2asn WHERE country_code = ?"
        cur.execute(select, (c_code,))
        data = cur.fetchall()
        if data:
            data_ccode[c_code] = dict()
        for item in data:
            cidr_s = []
            cidr, asn, c_code, country, owner = item
            if owner not in data_ccode[c_code]:
                data_ccode[c_code][owner] = dict()
            if data_ccode[c_code][owner].get("cidr"):
                cidr_s.extend(data_ccode[c_code][owner].get("cidr"))
            cidr_s.append(cidr)
            data_ccode[c_code][owner].update({"asn": asn, "cidr": cidr_s, "country": country})
        cur.close()
        conn.close()
        return data_ccode if data_ccode else "Country Code Not Found"
    except TypeError:
        cur.close()
        conn.close()
        return "Country Code Not Found"


def help_msg():
    txt = f"""
Reference information on the keys used in the script:\n{'-'*55}\n

"-i" - search ASN by ip address.

Example: python ip2asn_db.py -i 185.253.217.208 
{'-'*55}\n
"-a" - search for ASN information, including ip address ranges included. 

Example: python ip2asn_db.py -a 38803

In this case, only the numeric value of the ASN is entered;
{'-'*55}\n
"-o" - selects information on the owners of ip address ranges and ASNs.

Example: python ip2asn_db.py -o CLOUDFLARENET

Sampling is performed by partial matching of the owner's name. 
For more accurate selection it is desirable to use the 
exact name of the owner, which can be viewed in the database;
{'-'*55}\n
"-c" - selection of information by country code. All ASN owners and the ranges 
of ip-addresses that belong to them are selected.

Example: python ip2asn_db.py -c CZ;
{'-'*55}\n
"-h" - output reference information. The "s" key is not specified for this key.

Example: python ip2asn_db.py -h
{'-'*55}\n
Adding the "s" key to any of the above keys saves the resulting dictionary, 
in addition to its output in the terminal. 

Example: python ip2asn_db.py -cs CZ
"""
    print(txt)
