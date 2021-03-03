#!/usr/bin/env python3
import subprocess
import my_azure_settings


REQUIRED_VARS = (
    'AZ_RESOURCE_GROUP',
    'AZ_LOCATION',
    'POSTGRES_SERVER_NAME',
    'POSTGRES_ADMIN_USER',
    'POSTGRES_ADMIN_PASSWORD',
    'APP_DB_NAME',
    'MY_IP_ADDRESS'
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

# Ref: https://docs.microsoft.com/cli/azure/postgres/server?view=azure-cli-latest#az-postgres-server-create
# SKUs: https://docs.microsoft.com/azure/postgresql/concepts-pricing-tiers
#       {pricing tier}_{compute generation}_{vCores}
create_server_command = [
    'az', 'postgres', 'server', 'create',
    '--resource-group', my_azure_settings.AZ_RESOURCE_GROUP,
    '--location', my_azure_settings.AZ_LOCATION,
    '--name', my_azure_settings.POSTGRES_SERVER_NAME,
    '--admin-user', my_azure_settings.POSTGRES_ADMIN_USER,
    '--admin-password', my_azure_settings.POSTGRES_ADMIN_PASSWORD,
    '--sku-name', 'GP_Gen5_2',
]

create_server = input('Create PostgreSQL server? [y/n]: ')
if create_server == 'y':
    print("Creating PostgreSQL server...")
    print(" ".join(create_server_command))
    subprocess.run(create_server_command)


# Set up firewall.
# Ref: https://docs.microsoft.com/en-gb/cli/azure/postgres/server/firewall-rule?view=azure-cli-latest#az-postgres-server-firewall-rule-create
azure_firewall_command = [
    'az', 'postgres', 'server', 'firewall-rule', 'create',
    '--resource-group', my_azure_settings.AZ_RESOURCE_GROUP,
    '--server-name', my_azure_settings.POSTGRES_SERVER_NAME,
    '--start-ip-address', '0.0.0.0',
    '--end-ip-address', '0.0.0.0',
    '--name', 'AllowAllAzureIPs',
]

create_rule = input('Create Azure IPs firewall rules? [y/n]: ')
if create_rule == 'y':
    print("Allowing access from Azure...")
    print(" ".join(azure_firewall_command))
    subprocess.run(azure_firewall_command)

local_ip_firewall_command = [
    'az', 'postgres', 'server', 'firewall-rule', 'create',
    '--resource-group', my_azure_settings.AZ_RESOURCE_GROUP,
    '--server-name', my_azure_settings.POSTGRES_SERVER_NAME,
    '--start-ip-address', my_azure_settings.MY_IP_ADDRESS,
    '--end-ip-address', my_azure_settings.MY_IP_ADDRESS,
    '--name', 'AllowMyIP',
]

create_rule = input('Create local IP firewall rules? [y/n]: ')
if create_rule == 'y':
    print("Allowing access from local IP...")
    print(" ".join(local_ip_firewall_command))
    subprocess.run(local_ip_firewall_command)


create_db_command = [
    'az', 'postgres', 'db', 'create',
    '--resource-group', my_azure_settings.AZ_RESOURCE_GROUP,
    '--server-name', my_azure_settings.POSTGRES_SERVER_NAME,
    '--name', my_azure_settings.APP_DB_NAME,
]

create_app_db = input('Create App DB? [y/n]: ')
if create_app_db == 'y':
    print("Creating App DB...")
    print(" ".join(create_db_command))
    subprocess.run(create_db_command)


connect_details_command = [
    'az', 'postgres', 'server', 'show',
    '--resource-group', my_azure_settings.AZ_RESOURCE_GROUP,
    '--name', my_azure_settings.POSTGRES_SERVER_NAME,
]
print("Getting access details...")
print(" ".join(connect_details_command))
subprocess.run(connect_details_command)

# Connect to Azure using connection string format (to force SSL)
# psql "host=$POSTGRES_FULLY_QUALIFIED_DOMAIN_NAME sslmode=require port=5432 user=$POSTGRES_ADMIN_USER@$POSTGRES_SERVER_NAME dbname=postgres" -W