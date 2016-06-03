#!/bin/bash

set -e

cd "$( dirname "$0" )/example"

../backup_hosted_source_projects.bash ../example.txt
