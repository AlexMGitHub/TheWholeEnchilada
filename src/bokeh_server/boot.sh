#!/bin/sh
# Read secret key from Docker secrets file and set environment variable
export BOKEH_SECRET_KEY=`cat $BOKEH_SECRET_KEY_FILE`
# Start Bokeh server in directory mode with externally signed session IDs
if [ $BOKEH_ENV = 'development' ];
then
    # Dev mode (--dev) can only accept one app at a time
    # To use dev mode, remove all but one directory from the command and add
    # --dev *after* the directory and before the other options
    bokeh serve src/bokeh_server/eda src/bokeh_server/train src/bokeh_server/results  --address 0.0.0.0 --session-ids external-signed
else
    bokeh serve src/bokeh_server/eda src/bokeh_server/train src/bokeh_server/results --address 0.0.0.0 --session-ids external-signed
fi
