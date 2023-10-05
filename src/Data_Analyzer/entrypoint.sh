#!/bin/bash

# Author: Marc Nebel
# Beschreibung: Skript für das Ausführen mehrerer Python Programme in einem Container. Data Analysis wird dabei als Backgound Thread gestartet.

# This script can break when modified by windows, as EOL is CRLF. If something bash related goes wrong, change it to LF by hand
# This can also be caused by git crlf converter.

python3 -u initdb.py
python3 -u data_analysis.py &
python3 -u main.py