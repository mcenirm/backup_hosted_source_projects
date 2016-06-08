#!/usr/bin/env python
from __future__ import print_function
import logging
import os
import subprocess
import sys

import gitlab


def usage():
    print('Usage: ' + __name__ + ' <configuration_file>\n'
          'Backup the hosted source projects listed in <configuration_file>',
          file=sys.stderr)


def main(configuration_file):
    backup_gitlab = None

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
            if len(parts) < 2:
                error('Too few path parts at line '+str(line_no)+': '+url)
                return 2

            if backup_gitlab is None:
                backup_gitlab = BackupGitlab()

            owner_name = parts[1]
            project_name = parts[2] if len(parts) > 2 else None
            backup_gitlab.backup(owner_name, project_name)

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


def backup_github_repository(owner, repository):
    backup_gitXXb_repository('github.com', owner, repository)


def backup_github_owner(owner):
    error('TODO')


def backup_gitXXb_repository(service, owner, repository):
    local_dir = os.path.join(service, owner, repository+'.git')
    rewritten_url = 'git@'+service+':'+owner+'/'+repository+'.git'
    backup_git_repository(local_dir, url=rewritten_url)


def backup_git_repository(local_dir, url):
    logger = logging.getLogger(__name__)
    logger.debug('backup_git_repository: local_dir=%s url=%s', local_dir, url)
    if not os.path.isdir(local_dir):
        cmd = ['git', 'clone', '--quiet', '--mirror', url, local_dir]
    else:
        cmd = ['git', '--git-dir='+local_dir, 'remote', 'update']
    logger.debug('                     : cmd=%s', repr(cmd))
    subprocess.check_call(cmd)


class BackupGitlab():
    def __init__(self):
        self.gitlab = gitlab.Gitlab.from_config()
        self.gitlab.auth()
        self.name = 'gitlab.com'
        self.logger = logging.getLogger(__name__)

    def backup(self, owner_name, project_name=None):
        self.logger.debug('backup: owner=%s project=%s', owner_name, project_name)
        if project_name is None:
            group = self.gitlab.groups.get(owner_name)
            self.backup_group(group)
        else:
            project_path = u'{}/{}'.format(owner_name, project_name)
            project = self.gitlab.projects.get(project_path)
            self.backup_project(project)

    def backup_group(self, group):
        for project in group.projects:
            self.backup_project(project)

    def backup_project(self, project):
        owner_path = project.namespace.path
        local_dir = os.path.join(self.name, owner_path, project.path+'.git')
        backup_git_repository(local_dir, project.ssh_url_to_repo)


def setup_logging(config_file='logging.ini'):
    if os.path.isfile(config_file):
        import logging.config
        logging.config.fileConfig(config_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage
        sys.exit(1)
    setup_logging()
    rc = main(sys.argv[1])
    sys.exit(rc)
