#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to the web servers.

execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric import task
from fabric.connection import Connection
from datetime import datetime
from os.path import exists, isdir
from invoke import UnexpectedExit

env.hosts = ['54.159.37.237', '54.90.3.106']

@task
def do_pack(c):
    """Generates a tgz archive."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            c.run("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        c.run("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print(f"Error creating archive: {e}")
        return None

@task
def do_deploy(c, archive_path):
    """Distributes an archive to the web servers."""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        c.put(archive_path, '/tmp/')
        c.run('mkdir -p {}{}/'.format(path, no_ext))
        c.run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        c.run('rm /tmp/{}'.format(file_n))
        c.run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        c.run('rm -rf {}{}/web_static'.format(path, no_ext))
        c.run('rm -rf /data/web_static/current')
        c.run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except UnexpectedExit as e:
        print(f"Deployment failed: {e}")
        return False

@task
def deploy(c):
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack(c)
    if archive_path is None:
        return False
    result = do_deploy(c, archive_path)
    return result
