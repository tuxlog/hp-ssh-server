#!/usr/bin/env python3
# coding: utf-8

import requests
import sys
import matplotlib
# Anti-Grain Geometry (AGG) backend so PyGeoIpMap can be used 'headless'
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import GeoIP

#
# Get all coordinates for the ips in ip_list using GeoIP and save them to lat and lon
#
def geoip_lat_lon(gi, ip_list=[], ips=[], lats=[], lons=[]):
    print("Calculating Coords for {} IPs...".format(len(ip_list)))
    for ip in ip_list:
        try:
            gir = gi.record_by_addr(ip)
        except Exception:
            print("Unable to find IP: %s" % ip)
            continue
        if gir is None or gir['latitude'] is None or gir['longitude'] is None:
            print("Unable to find coords for IP: %s" % ip)
            continue

        # save coords to lists
        ips.append(ip)
        lats.append(gir['latitude'])
        lons.append(gir['longitude'])
    return ips, lats, lons


# Using Basemap and the matplotlib toolkit, this function generates a map and
# puts a red dot at the location of every IP addresses found in the list.
# The map is then saved in the file specified in `output`.
#
def generate_map(output, ip_list=[], lats=[], lons=[], wesn=None):

    print("Generating map and saving it to {}".format(output))
    if wesn:
        wesn = [float(i) for i in wesn.split('/')]
        m = Basemap(projection='cyl', resolution='l', llcrnrlon=wesn[0], llcrnrlat=wesn[2], urcrnrlon=wesn[1], urcrnrlat=wesn[3])
    else:
        m = Basemap(projection='cyl', resolution='l')
    m.bluemarble()
    ipsize = {}
    for i in range(0,len(lons)):
        msize = 1
        if ip_list[i] in ipsize.keys():
            ipsize[ ip_list[i] ] = ipsize[ ip_list[i] ] + .01
        else:
            ipsize[ ip_list[i] ] = 1

        msize = ipsize[ ip_list[i] ]

        m.plot( x=lons[i], y=lats[i], color='#ff0000', alpha=0.3, marker='o', markersize=msize )
    plt.savefig(output, dpi=300, bbox_inches='tight')


def main():
    # read ip addresses from file
    ip_list=[]
    with open('sshlogins.txt') as file:
        for line in file:
            parts = line.rstrip().split(';')
            ip_list.append( parts[1] )

    gi = GeoIP.open("GeoIPCity.dat", GeoIP.GEOIP_STANDARD)
    ips, lats, lons = geoip_lat_lon(gi, ip_list=ip_list)

    generate_map('hackermap.png', ips, lats, lons, wesn=None)


if __name__ == '__main__':
    main()
