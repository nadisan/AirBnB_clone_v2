#!/usr/bin/python3
"""Deploy archive!"""
from fabric.api import put, run, env
from os import path

env.hosts = ['54.210.60.5', '54.236.56.239']


def do_deploy(archive_path):
    """Deploys compressed web static file to my web servers"""

    if not path.exists(archive_path) or path.isfile(archive_path) is False:
        return False

    fileNameWithTgz = archive_path.split('/')[-1]
    fileNameWithoutExt = archive_path.split('/')[-1].split('.')[0]
    webServerFolder = '/data/web_static/releases/{}'.format(fileNameWithoutExt)

    put(archive_path, '/tmp/{}'.format(fileNameWithTgz))

    run('sudo mkdir -p {}/'.format(webServerFolder))
    run('sudo tar -xzf /tmp/{} -C {}/'.
        format(fileNameWithTgz, webServerFolder))

    run('sudo rm /tmp/{}'.format(fileNameWithTgz))
    run('sudo mv {}/web_static/* {}/'.format(webServerFolder, webServerFolder))
    run('sudo rm -rf {}/web_static'.format(webServerFolder))

    # deleting & creating symbolic link
    run('sudo rm -rf /data/web_static/current')
    run('sudo ln -s {}/ /data/web_static/current'.format(webServerFolder))
    print('New version deployed!')
    return True