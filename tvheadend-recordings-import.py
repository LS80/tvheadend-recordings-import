#!/usr/bin/env python3

import argparse
import datetime
import glob
import json
import os
import pathlib
import re
import sys
import urllib.parse
import urllib.request

from pymediainfo import MediaInfo


def recording_data(filename, channel, title, subtitle, start, stop):
    return json.dumps(
        {
            "enabled": True,
            "start": start,
            "stop": stop,
            "channelname": channel,
            "title": {
                "eng": title
            },
            "subtitle": {
                "eng": subtitle
            },
            "description": {
                "eng": ""
            },
            "comment": "",
            "files": [
                {
                    "filename": filename
                }
            ]
        }, separators=(',', ':')
    )


def recordings(path, date_limit, output_path):
    for filename in glob.glob(str(pathlib.Path(path) / '*/*.ts')):
        media_info = MediaInfo.parse(filename)
        channel = next(track for track in media_info.tracks if track.track_type == 'Menu').service_name

        title, subtitle = os.path.basename(filename).split(' - - ')
        subtitle = re.sub(r'(-\d+)?\.ts$', '', subtitle)

        video = next(track for track in media_info.tracks if track.track_type == 'Video')
        if video.duration is None:
            continue

        stop = os.path.getmtime(filename)
        start = stop - video.duration/1000

        if datetime.datetime.fromtimestamp(start).date() < date_limit:
            yield recording_data(
                filename=filename.replace(str(path), output_path),
                channel=channel,
                title=title,
                subtitle=subtitle,
                start=stop - video.duration/1000,
                stop=stop
            )


def create_entry(data, host, port):
    url = "http://{host}:{port}/api/dvr/entry/create?{qs}".format(
      host=host,
      port=port,
      qs=urllib.parse.urlencode(dict(conf=data))
    )
    urllib.request.urlopen(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Tvheadend import recordings.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--path', default='.',
                        help='path to recorded files')
    parser.add_argument('--date-limit', type=datetime.date.fromisoformat, default=datetime.date.today(),
                        help='maximum recording date to start import')
    parser.add_argument('--output-path', default='.',
                        help='recordings path')
    parser.add_argument('--host', default='localhost',
                        help='host name for HTTP API')
    parser.add_argument('--port', type=int, default=9981,
                        help='port number for HTTP API')
    args = parser.parse_args()

    for recording in recordings(args.path, args.date_limit, args.output_path):
        create_entry(recording, args.host, args.port)
