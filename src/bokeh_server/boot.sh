#!/bin/sh
# Read secret key from Docker secrets file and set environment variable
export BOKEH_SECRET_KEY=`cat $BOKEH_SECRET_KEY_FILE`
# Start Bokeh server in directory mode with externally signed session IDs
bokeh serve src/bokeh_server/eda --address 0.0.0.0 --session-ids external-signed