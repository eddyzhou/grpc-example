#!/bin/bash

#ps aux | grep "server.py" | grep -v grep | awk '{print $2}' | xargs kill -SIGTERM
for PID in `ps aux | grep "server.py" | grep -v grep | awk '{print $2}'`
do
echo "retart ${PID}"
kill -15 ${PID}
sleep 3
done
echo "done!"
