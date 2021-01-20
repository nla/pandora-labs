#!/usr/bin/env python3

import json
import os
import re
import sys
from glob import glob
from os.path import basename

if len(sys.argv) <= 1:
    print("Usage: " + sys.argv[0] + " out-dir")
    sys.exit(1)

out_dir = sys.argv[1]

lang_dirs=[
    "/derivative/data/nla.arc/au/013/language-buckets",
    "/derivative/data/nla.arc/au/014/language-buckets",
    "/derivative/data/nla.arc/au/015/LANGUAGE-ANALYSIS",
    "/derivative/data/nla.arc/au/016/language-analysis"
]

#
# Group input files by language
#

langs = {}

for dir in lang_dirs:
    for path in glob(dir + '/*.txt'):
        f = basename(path)
        isocode = f.replace(".txt", "")
        if isocode == 'en':
            continue
        if isocode not in langs:
            langs[isocode] = {"files": []}
        lang = langs[isocode]
        lang['files'].append(path)

#
# Read each file, extract just homepages and group snapshots by URL
#

url_re = re.compile("https?://[^/]+.archive.org/[^/]+/([0-9]+)/(.*)")
homepage_re = re.compile("https?://[^/]+\.au/?")

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for isocode, lang in langs.items():
    sites = {}
    for file in lang['files']:
        with open(file) as f:
            for raw_url in f:
                raw_url = raw_url.strip()
                if '\t' in raw_url: raw_url = raw_url.split('\t', 2)[1]
                m = url_re.fullmatch(raw_url)
                if not m:
                    print("Bad url", raw_url)
                    continue

                timestamp = str(m.group(1))
                url = str(m.group(2))

                if homepage_re.fullmatch(url):
                    print(isocode, timestamp, url)
                    if url not in sites: sites[url] = []
                    sites[url].append(timestamp)

    if len(sites) == 0:
        continue

    with open(os.path.join(out_dir, isocode + ".json"), 'w') as f:
        json.dump(sites, f, indent=2)
