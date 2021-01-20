#!/usr/bin/env python3

import html
import json
import os
import re
import sys
from glob import glob

if len(sys.argv) < 3:
    print('Usage:', sys.argv[0], 'src-dir', 'out-dir')

src_dir = sys.argv[1]
out_dir = sys.argv[2]

if not(os.path.exists(out_dir)):
    os.makedirs(out_dir)

domain_re = re.compile("https?://([^/]+)/.*")
def get_domain(url):
    m = domain_re.match(url)
    if m:
        return m.group(1)
    else:
        return url


def domain_key(args):
    url, ts = args
    key = ",".join(reversed(get_domain(url).split(".")))
    return key


for path in glob(os.path.join(src_dir, "*.json")):
    isocode = os.path.basename(path).replace(".json", "")
    with open(path) as f:
        sites = json.load(f)

    with open(os.path.join(out_dir, isocode + ".html"), "w") as outfile:
        outfile.write("""<!doctype html>
    <link rel=stylesheet href=../../labs.css>
    <title>""" + isocode + """ - Language Analysis - PANDORA Labs</title>
    <main>
    <a href=../../>PANDORA Labs</a> - <a href=../>Language Analysis</a>
    <h2>""" + isocode + """</h2>
    <ul>""")

        for url, snapshots in sorted(sites.items(), key=domain_key):
            host = url

            dates = {}
            for ts in snapshots:
                year = ts[0:4]
                dates[year] = ts

            outfile.write("<li>" + html.escape(get_domain(url)) + "\n")
            for year, ts in sorted(dates.items()):
                outfile.write("  <a href='" + html.escape('https://webarchive.nla.gov.au/awa/' + ts + '/' + url) + "'>" + html.escape(year) + "</a>\n")

        outfile.write("</main>\n")