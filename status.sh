#!/bin/bash

pid=$(pgrep -f api_register)
if [ $? -eq  0 ]
then
    echo $(date '+%s.%3N') "api_register OK running as PID $pid"
else
	echo $(date '+%s.%3N') "api_register not running"
fi
