#!/usr/bin/python3
"""
Fabric script to generate a tgz archive
execute: fab -f 1-pack_web_static.py do_pack
"""

from datetime import datetime
from fabric.api import local


def do_pack():
    """
    Creates an archive from the web_static folder.
    """
    time = datetime.now()
    archive = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.tgz'
    
    # Create the versions directory if it doesn't exist
    local('mkdir -p versions')
    
    # Create the tar archive
    result = local('tar -cvzf versions/{} web_static'.format(archive))
    
    # Check if the command succeeded
    if result.succeeded:
        return 'versions/' + archive
    else:
        return None
