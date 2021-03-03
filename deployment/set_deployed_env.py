#! /usr/bin/env python3
import subprocess
import sys
import my_azure_settings

REQUIRED_VARS = (
    'AZ_RESOURCE_GROUP',
    'AZ_LOCATION',
    'APP_SERVICE_APP_NAME',
    'POSTGRES_SERVER_NAME',
    'POSTGRES_ADMIN_USER',
    'POSTGRES_ADMIN_PASSWORD',
    'APP_DB_NAME',
    'DJANGO_SETTINGS_MODULE',
    'POST_BUILD_COMMAND',
)

missing = []
for v in REQUIRED_VARS:
    try:
        value = my_azure_settings.__getattribute__(v)
        if not value or str(value).isspace():
            raise AttributeError
    except:
        missing.append(v)
if missing:
    print("Required variables not set in my_azure_settings.py:")
    print("\t" + "\n\t".join(missing))
    print("Exiting.")
    exit()

SETTINGS_KEYS = (
    'POSTGRES_SERVER_NAME',
    'POSTGRES_ADMIN_USER',
    'POSTGRES_ADMIN_PASSWORD',
    'POSTGRES_FULLY_QUALIFIED_DOMAIN_NAME',
    'APP_DB_NAME',
    'DJANGO_SETTINGS_MODULE',
    'POST_BUILD_COMMAND',

)
settings_pairs = [f'{k}={my_azure_settings.__getattribute__(k)}' for k in SETTINGS_KEYS]

# https://docs.microsoft.com/cli/azure/webapp/config/appsettings?view=azure-cli-latest#az-webapp-config-appsettings-set
settings_command = [
    'az', 'webapp', 'config', 'appsettings', 'set',
    '--name', my_azure_settings.APP_SERVICE_APP_NAME,
    '--resource-group', my_azure_settings.AZ_RESOURCE_GROUP,
    '--settings',
] + settings_pairs

update_settings = input('Update App Settings? [y/n]: ')
if update_settings == 'y':
    print("Updating App Settings... ")
    print(" ".join(settings_command))
    subprocess.run(settings_command)
    print("Done")
