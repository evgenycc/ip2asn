# ip2asn
Two versions of a small script that can be used to select asn information.

The "res" directory contains archives, which must be unpacked before running the script. The size of the files is larger than github allows downloading, so I had to archive them.

The ip2asn.py script searches only by ip, since it uses a json file as the base for the ASN search.
The ip2asn_db.py script does various selections, which are described below. The base used here is sqlite3.


*****************************************************
REFERENCE INFORMATION ON THE KEYS USED IN THE SCRIPT:
*****************************************************

"-i" - search ASN by ip address.
Example: 
```
python ip2asn_db.py -i 185.253.217.208
```
*****************************************************

"-a" - search for ASN information, including ip address ranges included. 

Example: 
```
python ip2asn_db.py -a 38803
```

In this case, only the numeric value of the ASN is entered;
***********************************************************

"-o" - selects information on the owners of ip address ranges and ASNs. 

Example: 
```
python ip2asn_db.py -o CLOUDFLARENET
```

Sampling is performed by partial matching of the owner's name. 
For more accurate selection it is desirable to use the exact name of the owner, 
which can be viewed in the database;
*******************************************************************************

"-c" - selection of information by country code. All ASN owners and the ranges of ip-addresses that belong to them are selected. 

Example: 
```
python ip2asn_db.py -c CZ;
```
*****************************************************

"-h" - output reference information. The "s" key is not specified for this key.
Example: 
```
python ip2asn_db.py -h
```
*****************************************************

Adding the "s" key to any of the above keys saves the resulting dictionary, in addition to its output in the terminal. 
Example: 
```
python ip2asn_db.py -cs CZ
```
