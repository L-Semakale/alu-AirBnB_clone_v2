#!/usr/bin/python3
"""Fabric function sends archived static site to webservers"""


from fabric.api import put, run, env
from os.path import exists
# remotely exexutes commands in both servers if run in one of them.
env.hosts = ["3.81.235.19", "3.85.12.239"]


def do_deploy(archive_path):
    """Archives to web-servers"""
    if exists(archive_path) is False:
        return False
    # If archive isn't even there archive nothing
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        # uploads archived folder to /tmp/
        put(archive_path, '/tmp/')

# commands to uncompress folder, delete compressed, delete link
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except BaseException:
        return False
