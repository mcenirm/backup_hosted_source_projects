#!/bin/bash

set -e

Usage () { cat >&2 <<EOF
Usage: $0 <configuration_file>
Backup the hosted source projects listed in <configuration_file>
EOF
}

if [ $# -ne 1 ] ; then
  Usage
  exit 1
fi

configuration_file=$1

Main () {
  cat -n -- "$configuration_file" | while read -r line_no url ; do
    case "$url" in
      \#*|'')
        # Skip comment and blank lines
        continue
        ;;
      *.git)
        # Handle simple git repositories
        backup_simple_git
        ;;
      gitlab.com/*/*/*)
        Error "Too many parts to gitlab path at line ${line_no}: $url"
        exit 2
        ;;
      gitlab.com/*/*)
        # Handle gitlab-hosted projects
        backup_gitlab_project
        ;;
      gitlab.com/*)
        # Handle gitlab-hosted users and groups
        backup_gitlab_owner
        ;;
      github.com/*/*/*)
        Error "Too many parts to github path at line ${line_no}: $url"
        exit 2
        ;;
      github.com/*/*)
        # Handle github-hosted repositories
        backup_github_repository
        ;;
      github.com/*)
        # Handle github-hosted users and organizations
        backup_github_owner
        ;;
      *)
        # Unable to handle anything else
        Error "Unrecognized item type at line ${line_no}: $url"
        exit 2
        ;;
    esac
  done
}

Error () {
  echo >&2 "$@"
}

backup_simple_git () {
  :
}

backup_gitlab_project () {
  :
}

backup_gitlab_owner () {
  :
}

backup_github_repository () {
  :
}

backup_github_owner () {
  :
}

Main
