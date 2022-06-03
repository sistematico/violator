#!/usr/bin/env bash

if [ "$1" == "off" ]; then
  heroku ps:scale web=0
  heroku maintenance:on
fi

if [ "$1" == "on" ]; then
  heroku ps:scale web=1
  heroku maintenance:off
fi