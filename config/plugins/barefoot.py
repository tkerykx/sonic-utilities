#!/usr/bin/env python

import click
import json
import subprocess
from sonic_py_common import device_info
from swsscommon.swsscommon import ConfigDBConnector

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@click.group()
def barefoot():
    pass

@barefoot.command()
@click.option('-y', '--yes', is_flag=True, callback=abort_if_false,
    expose_value=False, prompt='Swss service will be restarted, continue?')
@click.argument('profile')
def profile(profile):
    # Check if profile can be changed
    completed_process = subprocess.run(['docker', 'exec', '-it', 'syncd',
        'test', '-h', '/opt/bfn/install'])
    if completed_process.returncode != 0:
        click.echo('Cannot change profile: default one is in use')
        raise click.Abort()
    
    # Get chip family
    hwsku_dir = device_info.get_path_to_hwsku_dir()
    with open(hwsku_dir + '/switch-tna-sai.conf') as file:
        chip_family = json.load(file)['chip_list'][0]['chip_family'].lower()
    
    # Check if profile is supported
    if chip_family == 'tofino' and profile[0] != 'x' or \
        chip_family == 'tofino2' and profile[0] != 'y':
        click.echo('Specified profile is unsupported on the system')
        raise click.Abort()

    # Check if profile <profile_name>_<chip_family> exists
    no_arch_information = False
    completed_process = subprocess.run(['docker', 'exec', '-it', 'syncd',
        'test', '-d', '/opt/bfn/install_' + profile + '_' + chip_family])

    # Otherwise, check if profile <profile_name>_profile exists (only for tofino and tofino2)
    if completed_process.returncode != 0:
        if chip_family == 'tofino' or chip_family == 'tofino2':
            completed_process = subprocess.run(['docker', 'exec', '-it', 'syncd',
            'test', '-d', '/opt/bfn/install_' + profile + '_profile'])
            no_arch_information = True

    if completed_process.returncode != 0:
        click.echo('No profile with the provided name found for {}'.format(chip_family))
        raise click.Abort()
    
    # Update configuration
    config_db = ConfigDBConnector()
    config_db.connect()
    profile += '_profile' if no_arch_information else '_' + chip_family
    config_db.mod_entry('DEVICE_METADATA', 'localhost', {'p4_profile': profile})

    subprocess.run(['systemctl', 'restart', 'swss'], check=True)

def register(cli):
    version_info = device_info.get_sonic_version_info()
    if version_info and version_info.get('asic_type') == 'barefoot':
        cli.commands['platform'].add_command(barefoot)
