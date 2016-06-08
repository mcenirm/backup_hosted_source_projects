python_binary(
    name='backup_hosted_source_projects',
    dependencies=[
        '3rdparty/python:pygithub3',
        '3rdparty/python:python-gitlab',
    ],
    source='backup_hosted_source_projects.py',
)

python_tests(
    name='test',
    sources=globs('test_*.py'),
    dependencies=[
        ':backup_hosted_source_projects',
    ],
)
