
# ip-info-downloader

***Easy way to download ip databases in CSV format from https://lite.ip2location.com/***


Getting Started
-------------

Linux
1. ```git clone https://github.com/bralbral/ip-info-downloader.git```
2. ```cd ip-info-downloader```
3. ```pip install -r requirements.txt```
4. ```bash start```
5. Grab results from ip-info-downloader/temp

docker-compose
1. ```git clone https://github.com/bralbral/ip-info-downloader.git```
2. ```cd ip-info-downloader```
3. ```docker-compose up```
5. Grab results from ip-info-downloader/temp


Files
-------------
Source

1. [Proxy info](https://lite.ip2location.com/database/px11-ip-proxytype-country-region-city-isp-domain-usagetype-asn-lastseen-threat-residential-provider)
2. [Asn](https://lite.ip2location.com/database-asn)
3. [GeoIp](https://lite.ip2location.com/database/db11-ip-country-region-city-latitude-longitude-zipcode-timezone)

Converted

For each source file, a ```converted_*``` file will be created.
Mapping is equivalent to the original one and in addition a [cidr](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) field has been added
