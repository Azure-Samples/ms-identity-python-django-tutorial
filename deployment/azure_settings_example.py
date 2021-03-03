
# This is a python file to set up the environment variables you'll need for your deployment.
# The UPPER_CASE_VALUES will be sent as env vars to your deployment

# This will tell your deployed app to use the settings file in Sample/Azure.py (with your postgreSQL DB settings) 
# instead of the default Sample.settings.py
DJANGO_SETTINGS_MODULE='Sample.azure'

# This tells Azure App service to run this shell file after deployment
# By default, it contains a migrate command
POST_BUILD_COMMAND='deployment/post-build.sh'

# The Azure App name, Resource Group, and Location to use for you application.
# FILL IN THESE VALUES! THEY ARE REQUIRED
APP_SERVICE_APP_NAME=''
AZ_RESOURCE_GROUP=''
AZ_LOCATION=''

# Server Name, Admin User and Admin Password for creating the PostgreSQL server on Azure, and the application DB name you want to use.
# FILL IN THESE VALUES! THEY ARE REQUIRED
POSTGRES_SERVER_NAME=''
POSTGRES_ADMIN_USER=''
POSTGRES_ADMIN_PASSWORD=''
APP_DB_NAME=''

# Public IP address of the machine you're working from
# This is required if you're looking to manage the Django database from your local machine's command line
# Find this by going to Bing search or Google search with the search term "What is my IP"
# This is REQUIRED if you plan on using manage.py commands on the PostgreSQL DB from your local machine.
MY_IP_ADDRESS='0.0.0.0'

# The Azure PostgreSQL server host.
# This will not be available until after creating the database server.
# (Will be output at end if running `createdb.py`)
# copy and paste the the "fully qualified domain name" here.
POSTGRES_FULLY_QUALIFIED_DOMAIN_NAME=''
