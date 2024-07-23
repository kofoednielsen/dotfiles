#!/bin/sh
mkdir -p /tmp/trashbin
cp --remove-destination "$@" /tmp/trashbin
rm "$@"
