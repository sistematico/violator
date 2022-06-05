#!/usr/bin/env bash

if [ "$1" == "off" ]; then
  heroku ps:scale web=0 --app violator-tgbot
  heroku maintenance:on --app violator-tgbot
fi

if [ "$1" == "on" ]; then
  heroku ps:scale web=1 --app violator-tgbot
  heroku maintenance:off --app violator-tgbot
fi