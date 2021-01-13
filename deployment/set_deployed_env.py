#! /usr/bin/env python3
import os
import subprocess
import sys

REQUIRED_ENV_VARS = (
    'AZ_GROUP',
    'AZ_LOCATION',
    'APP_SERVICE_APP_NAME',
    'POSTGRES_SERVER_NAME',
    'POSTGRES_ADMIN_USER',
    'POSTGRES_ADMIN_PASSWORD',
    'APP_DB_NAME',
    'DJANGO_SETTINGS_MODULE',
    'POST_BUILD_COMMAND'
)

missing = []
for v in REQUIRED_ENV_VARS:
    if v not in os.environ:
        missing.append(v)
if missing:
    print("Required Environment Variables Unset:")
    print("\t" + "\n\t".join(missing))
    print("Exiting.")
    exit()

SETTINGS_KEYS = (
    'POSTGRES_SERVER_NAME',
    'POSTGRES_ADMIN_USER',
    'POSTGRES_ADMIN_PASSWORD',
    'POSTGRES_HOST',
    'APP_DB_NAME',
    'DJANGO_SETTINGS_MODULE',
    'POST_BUILD_COMMAND'

)
settings_pairs = ['{}={}'.format(k, os.getenv(k)) for k in SETTINGS_KEYS]

# https://docs.microsoft.com/en-us/cli/azure/webapp/config/appsettings?view=azure-cli-latest#az-webapp-config-appsettings-set
settings_command = [
    'az', 'webapp', 'config', 'appsettings', 'set',
    '--name', os.getenv('APP_SERVICE_APP_NAME'),
    '--resource-group', os.getenv('AZ_GROUP'),
    '--settings',
] + settings_pairs

update_settings = input('Update App Settings? [y/n]: ')
if update_settings == 'y':
    sys.stdout.write("Updating App Settings... ")
    sys.stdout.flush()
    subprocess.check_output(settings_command)
    print("Done")
