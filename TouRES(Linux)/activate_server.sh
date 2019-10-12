#!/bin/sh
export FLASK_APP=server.py
flask run --no-reload --host=0.0.0.0 --port 6060
