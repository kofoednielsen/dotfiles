#!/usr/bin/env bash
grim -g "$(slurp)" - | tesseract - - -l eng+dan | tr -d "" | wl-copy
