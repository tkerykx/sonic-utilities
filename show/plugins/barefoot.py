#!/usr/bin/env python

import click
import json
import subprocess
from sonic_py_common import device_info

@click.group()
def barefoot():
    pass

@barefoot.command()
def profile():
    # Check if profile can be changed
    completed_process = subprocess.run(['docker', 'exec', '-it', 'syncd',
        'test', '-h', '/opt/bfn/install'])
    if completed_process.returncode != 0:
        click.echo('Current profile: default')
        return
    
    # Get chip family
    hwsku_dir = device_info.get_path_to_hwsku_dir()
    with open(hwsku_dir + '/switch-tna-sai.conf') as file:
        chip_family = json.load(file)['chip_list'][0]['chip_family'].lower()
    
    # Print current profile
    click.echo('Current profile: ', nl=False)
    subprocess.run('docker exec -it syncd readlink /opt/bfn/install | sed '
        r's/install_\\\(.\*\\\)_profile/\\1/'
        r' | sed s/install_\\\(.\*\\\)_tofino\\\(.\*\\\)/\\1/', check=True, shell=True)

    opts = ''
    # Check if profile naming format contains tofino family information 
    suffix = '_profile'
    if '_tofino' in subprocess.check_output(['docker', 'exec', '-it', 'syncd', 'ls', '/opt/bfn']).strip().decode():
        suffix = '_' + chip_family

    # Check supported profiles 
    if chip_family == 'tofino':
        opts = r' -name install_x\*' + suffix
    elif chip_family == 'tofino2':
        opts = r' -name install_y\*' + suffix
    elif chip_family == 'tofino3':
        opts = r' -name install_y\*' + suffix + r' -o -name install_z\*' + suffix

    # Print profile list
    click.echo('Available profile(s):')
    subprocess.run('docker exec -it syncd find /opt/bfn -mindepth 1 '
        r'-maxdepth 1 -type d,l ' + opts + '| sed '
        r's%/opt/bfn/install_\\\(.\*\\\)_profile%\\1%'
        r' | sed s%/opt/bfn/install_\\\(.\*\\\)_tofino\\\(.\*\\\)%\\1%', shell=True)

def register(cli):
    version_info = device_info.get_sonic_version_info()
    if version_info and version_info.get('asic_type') == 'barefoot':
        cli.commands['platform'].add_command(barefoot)
