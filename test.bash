#!/bin/bash

set -e

cd "$( dirname "$0" )/example"

../dist/backup_hosted_source_projects ../example.txt
