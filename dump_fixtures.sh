#!/bin/bash
./manage.py dumpdata --format=json --indent=4 tms > ./adlibre_tms/apps/tms/fixtures/initial_data.json
