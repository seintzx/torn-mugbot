#!/usr/bin/env bash

botdir="/home/alarm/mugbot"
botname="mugbot.py"
process=`ps auxwww | grep ${botname} | grep -v grep | awk '{print $2}'`

cd $botdir
if [[ -z $process ]]; then
    screen -A -d -m -S mugbot ./${botname}
fi
