#!/bin/bash

if [ $# -ne 1 ]; then
  echo you need to specify the folder to clear out!
  echo valid values are:
  echo                        jes == JES2\\OUTPUT\\
  echo                  converted == converted\\
  exit 1
fi

if [ "$1" != "jes" ] && [ "$1" != "converted" ]; then
  echo you need to specify the folder to clear out!
  echo valid values are:
  echo                        jes == JES2/OUTPUT/
  echo                  converted == converted/
  exit 1
fi

if [ "$1" == "jes" ]; then
    echo clear jes
    rm -f JES2/OUTPUT/*
fi

if [ "$1" == "converted" ]; then
    echo clear converted
    rm -f converted/*.py
    rm -f converted/maps/*.*
fi
