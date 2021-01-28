## tvheadend-recordings-import

Import old [Tvheadend](https://tvheadend.org/) recordings to the current recordings database.

```
usage: tvheadend-recordings-import.py [-h] [--path PATH] [--date-limit DATE_LIMIT] [--output-path OUTPUT_PATH] [--host HOST] [--port PORT]

Tvheadend import recordings.

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           path to recorded files (default: .)
  --date-limit DATE_LIMIT
                        maximum recording date to start import (default: 2021-01-28)
  --output-path OUTPUT_PATH
                        recordings path (default: .)
  --host HOST           host name for HTTP API (default: localhost)
  --port PORT           port number for HTTP API (default: 9981)
```
