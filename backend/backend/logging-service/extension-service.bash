#!/bin/bash

find . -name 'log*' -print0 | while read -d $'\0' file; do
    if [ ! "${file: -5}" == ".json" ]
    then
        mv "$file" "$file.json"
    fi
done