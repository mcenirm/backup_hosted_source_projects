#!/bin/bash

set -e

cd "$( dirname "$0" )/example"

python ../backup_hosted_source_projects.py ../example.txt
