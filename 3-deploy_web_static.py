#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers.

execute: fab -f 3-deploy_web_static.py deploy --identity ~/.ssh/school --user ubuntu
"""

from fabric import task
from fabric import Connection
from datetime import datetime
from os.path import exists, isdir
import os

hosts = ['98.84.112.27', '54.234.223.92']

@task
def do_pack():
    """Generates a tgz archive."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            os.mkdir("versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print(f"Error in do_pack: {e}")
        return None


@task
def do_deploy(c, archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        print(f"Archive does not exist: {archive_path}")
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        
        # Using Connection to run commands
        c.put(archive_path, '/tmp/')
        c.run('mkdir -p {}{}/'.format(path, no_ext))
        c.run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        c.run('rm /tmp/{}'.format(file_n))
        c.run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        c.run('rm -rf {}{}/web_static'.format(path, no_ext))
        c.run('rm -rf /data/web_static/current')
        c.run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except Exception as e:
        print(f"Error in do_deploy: {e}")
        return False


@task
def deploy(c):
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(c, archive_path)
