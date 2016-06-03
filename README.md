# Description

Backup a set of hosted source projects to a local directory.


# Configuration file format

* One item per line
* Supported item types:
  - Full git url to a bare repository (ends in ".git")
  - Service-specific owner or project

    {service}/{owner}[/{project}]

Supported services:

| Service | Identifier   | Owner terminology    | Project terminology |
| ------- | ------------ | -------------------- | ------------------- |
| GitLab  | `gitlab.com` | user or group        | project             |
| GitHub  | `github.com` | user or organization | repository          |

Example configuration file:

    # Comment and blank lines are ignored
    
    # A GitLab user
    gitlab.com/example-user

    # A GitLab project
    gitlab.com/example-user/example-project

    # A GitLab group
    gitlab.com/example-group

    # A GitHub user
    github.com/example-user

    # A GitHub repository
    github.com/example-user/example-repository

    # A GitHub organization
    github.com/example-organization


# Usage

Change to the directory that will hold the backups.

    cd /Volumes/UNTITLED/backups

Run `backup_hosted_source_projects` specifying the configuration file.

    backup_hosted_source_projects ../example.txt
