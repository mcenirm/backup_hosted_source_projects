#!/usr/bin/env python
from __future__ import print_function
import os
import subprocess
import sys


def usage():
    print('Usage: ' + __name__ + ' <configuration_file>\n'
          'Backup the hosted source projects listed in <configuration_file>',
          file=sys.stderr)


def main(configuration_file):
    with open(configuration_file, 'r') as f:
        configuration = f.readlines()
    for line_no in range(1, len(configuration)+1):
        url = configuration[line_no-1].strip()
        parts = url.split('/')
        if url.startswith('#') or url == '':
            # Skip comment and blank lines
            continue
        elif url.endswith('.git'):
            # Handle simple git repositories
            backup_simple_git(url)
        elif url.startswith('gitlab.com/'):
            if len(parts) > 3:
                error('Too many path parts at line '+str(line_no)+': '+url)
                return 2
            elif len(parts) == 3:
                # Handle gitlab-hosted projects
                backup_gitlab_project(owner=parts[1], project=parts[2])
            elif len(parts) == 2:
                # Handle gitlab-hosted users and groups
                backup_gitlab_owner(owner=parts[1])
            else:
                error('Too few path parts at line '+str(line_no)+': '+url)
                return 2
        elif url.startswith('github.com/'):
            if len(parts) > 3:
                error('Too many path parts at line '+str(line_no)+': '+url)
                return 2
            elif len(parts) == 3:
                # Handle github-hosted repositories
                backup_github_repository(owner=parts[1], repository=parts[2])
            elif len(parts) == 2:
                # Handle github-hosted users and organizations
                backup_github_owner(owner=parts[1])
            else:
                error('Too few path parts at line '+str(line_no)+': '+url)
                return 2
        else:
            # Unable to handle anything else
            error('Unrecognized item type at line '+str(line_no)+': '+url)
            return 2


def error(msg):
    print(msg, file=sys.stderr)


def backup_simple_git(url):
    error('TODO')


def backup_gitlab_project(owner, project):
    backup_gitXXb_repository('gitlab.com', owner, project)


def backup_gitlab_owner(owner):
    error('TODO')


def backup_github_repository(owner, repository):
    backup_gitXXb_repository('github.com', owner, repository)


def backup_github_owner(owner):
    error('TODO')


def backup_gitXXb_repository(service, owner, repository):
    local_dir = os.path.join(service, owner, repository+'.git')
    rewritten_url = 'git@'+service+':'+owner+'/'+repository+'.git'
    backup_git_repository(local_dir, url=rewritten_url)


def backup_git_repository(local_dir, url):
    if not os.path.isdir(local_dir):
        cmd = ['git', 'clone', '--quiet', '--mirror', url, local_dir]
    else:
        cmd = ['git', '--git-dir='+local_dir, 'remote', 'update']
    subprocess.check_call(cmd)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage
        sys.exit(1)
    rc = main(sys.argv[1])
    sys.exit(rc)
