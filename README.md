# Deploy your Python applications to Azure Cloud and use Azure App Service to manage your operations

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Registration](#registration)
  - [Register the web app](#register-the-web-app)
- [Deployment](#deployment)
  - [Step 1: Prepare the web app for deployment](#step-1-prepare-the-web-app-for-deployment)
  - [Step 2: Prepare the app service and database](#step-2-prepare-the-app-service-and-database)
  - [Step 3: Update your Azure AD App Registration](#step-3-update-your-azure-ad-app-registration)
  - [Step 4: Complete your app deployment settings](#step-4-complete-your-app-deployment-settings)
- [We'd love your feedback!](#wed-love-your-feedback)
- [More information](#more-information)
- [Community Help and Support](#community-help-and-support)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)

## Overview

This readme demonstrates how to deploy a Python Django web application to **Azure Cloud** using [Azure App Service](https://docs.microsoft.com/azure/app-service/). It is recommended that the code sample from [Enable your Python Django webapp to sign in users and call Microsoft Graph with the Microsoft identity platform](https://github.com/azure-samples/ms-identity-python-django-webapp-call-graph) is used for deployment. You may choose to follow these steps with a different sample or your own project.

## Prerequisites

- An Azure Active Directory (Azure AD) tenant. For more information on how to get an Azure AD tenant, see [How to get an Azure AD tenant](https://azure.microsoft.com/documentation/articles/active-directory-howto-tenant/)
- A [user account](https://docs.microsoft.com/azure/active-directory/fundamentals/add-users-azure-active-directory) in your **Azure AD** tenant.
- [Visual Studio Code](https://code.visualstudio.com/download) is recommended for running and editing this sample.
- [VS Code Azure Tools Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack) extension is recommended for interacting with **Azure** through VS Code interface.
- An **Azure subscription**. This sample uses the free tier of **Azure App Service**.

Recommended, though not strictly necessary if not running the sample locally as well:

- [Python 3.8](https://www.python.org/downloads/)
- A virtual environment to install packages in

## Setup

Follow the setup instructions in [Enable your Python Django webapp to sign in users and call Microsoft Graph with the Microsoft identity platform](https://github.com/azure-samples/ms-identity-python-django-webapp-call-graph) sample or another Django sample of your choosing from [Microsoft Identity Django Tutorial)](https://github.com/azure-samples/ms-identity-python-django-tutorial).

## Registration

### Register the web app

Use an Azure AD application registration and its matching sample that that you have completed previously.
If you have not completed a sample yet, we recommend you proceed to complete [Enable your Python Django webapp to sign in users and call Microsoft Graph with the Microsoft identity platform](https://github.com/azure-samples/ms-identity-python-django-webapp-call-graph) sample and use the app registration from it.

## Deployment

In order to get your deployed app fully functional, you must:

1. Prepare the web app for deployment.
1. Deploy your project to **Azure App Service** and obtain a published website in the form of `https://example-domain.azurewebsites.net.`
1. Update your **Azure AD App Registration**'s redirect URIs from the **Azure Portal**, in order to include the redirect URI of your deployed Django application.
1. Complete your app deployment settings.

### Step 1: Prepare the web app for deployment

1. (optional) If you plan on interacting with the production Django database from your local machine, you must install postgres dependencies. Go to the requirements.txt file. If you are running on Windows, uncomment the `psycopg2` dependency. If you are running on Mac, uncomment `psycopg2-binary` dependency.
2. (optional) To deploy your app more securely, you must omit any secrets from the aad.config.json and Sample/settings.py file and import them securely into your app.
You **may skip the rest of this section** and proceed to [Step 2: Prepare the app service and database](#step-2-prepare-the-app-service-and-database) if you are doing a test deployment with a development Azure Active Directory App registration that does not have any sensitive data. **It is not secure to deploy secrets in a config file to a production application**.

<details>

<summary> expand this section if you would like to do deploy app secrets more securely.</summary>

1. Supply a config file that omits secrets (i.e., `aad.config.json` that sets `"client_credential": null`)
2. Remove any secrets from the settings.py file.
3. After completing [Step 2: Prepare the app service and database](#step-2-prepare-the-app-service-and-database) and [Step 3: Update your Azure AD App Registration](#step-3-update-your-azure-ad-app-registration), do not forget to expand the optional section in [Step 4: Complete your app deployment settings](#step-4-complete-your-app-deployment-settings) and complete the instructions

</details>

If you are sure you want to continue, proceed to [Step 2: Prepare the app service and database](#step-2-prepare-the-app-service-and-database).

### Step 2: Prepare the app service and database

This guide is for deploying to **Azure App Service** via **VS Code Azure Tools Extension**.

1. Open the VSCode command palette (ctrl+shift+P on Windows and command+shift+P on Mac).
1. Choose  `Azure App Service: Create New Web App... (Advanced)`
   1. Enter a globally unique name for your web app (e.g. `sams-django-test`) and press enter. Make a note of this name.
   2. Click `+ Create new resource group` and choose a name for it (e.g. `sams-django-test-resource-group`). Press enter. Make a note of this name.
   3. Select `Python 3.8` for your runtime stack.
   4. Click `+ Create new App Service plan` and give it a name  (e.g. `sams-django-test-app-svc-plan`). Press enter.
   5. Choose an app service tier (e.g., `F1 Free`)
   6. Click `Skip for now` for application insights resource
   7. Select a location (e.g. `West US`). Make a note of this as `westus`
1. Make a copy of the env-example file in the `deployment` folder at the root of the repository, calling it, for example, `my-azure-settings`
1. Fill in the following details in it:
   1. APP_SERVICE_APP_NAME from step 2.1
   2. AZ_GROUP from step 2.2
   3. AZ_LOCATION from step 2.7
1. Now fill in the following values for the creating the Postgres DB.

   ```Shell
    POSTGRES_SERVER_NAME='choose a globally-unique name for your server, e.g. my-postgres-server'
    POSTGRES_ADMIN_USER='choose an admin user name, e.g. administrator'
    POSTGRES_ADMIN_PASSWORD='choose a password'
    APP_DB_NAME='db name for your app, e.g. my-django-db'
   ```

1. Now export all of the values in this `my-azure-settings` file to your shell. For example, `export VARIABLE = 'value'` in Linux/MacOS or `$env:VARIABLE = 'value'` in powershell. To quickly export all values that are not commented out in bulk in Linux/MacOS, use the command `export $(grep -v '^#' my-azure-settings | xargs)`
1. From the terminal, run the `create-db.py` file with `python deployment/create-db.py`. Answer all of the questions in the affirmative if it is your first run.
1. In the last step, you'll be presented with a summary of the postgres DB access details. Make a note of the `fullyQualifiedDomainName`. Copy and paste it into your `my-azure-settings` file under the value `POSTGRES_HOST`.
1. export this value to your shell  (`export POSTGRES_HOST = 'value that was copied'`) or run the bulk export command from the previous step.
1. From the terminal, run the `set-deployed-env.py` file to set required environment variables (copied from your shell) to the app service.
1. Disable App Service's default authentication:

    Navigate to the **Azure App Service** Portal and locate your project. Once you do, click on the **Authentication/Authorization** blade. There, make sure that the **App Services Authentication** is switched off (and nothing else is checked), as this sample is using MSAL for authentication.

    ![disable_easy_auth](./ReadmeFiles/disable_easy_auth.png)

### Step 3: Update your Azure AD App Registration

- Navigate to the home page of your deployed app; take note of and copy the **redirect_uri** displayed on the home page.
- Navigate back to to the [Azure Portal](https://portal.azure.com).
- In the left-hand navigation pane, select the **Azure Active Directory** service, and then select **App registrations**.
- In the resulting screen, select the name of your application.
- In the Authentication blade, paste the URI you copied earlier from your deployed app instance. If the app had multiple redirect URIs, make sure to add new corresponding entries using the App service's full domain in lieu of `localhost:8000` for each redirect URI. Save the configuration.
- From the *Branding* menu, update the **Home page URL**, to the address of your service, for example `https://example-domain.azurewebsites.net/`. Save the configuration.
- You're done! Try navigating to the hosted app!

### Step 4: Complete your app deployment settings

Modify your app's `Sample/azure.py` file's allowed hosts as follows, using the full domain name of your app that you recorded in [Step 2: Prepare the app service and database](#step-2-prepare-the-app-service-and-database)

```Python
ALLOWED_HOSTS = ['https://example-domain.azurewebsites.net']
```

You may **skip the following optional section** if you are running a non-production deployment or you have skipped the optional  in [Step 1: Prepare the web app for deployment](#step-1-prepare-the-web-app-for-deployment)
<details>

<summary> expand this section if you elected to deploy app secrets more securely.</summary>

You have several options for adding your app secrets more securely. The following two examples demonstrate using Azure Vault **or** environment variables to add secrets removed from the `aad.config.json` file. Other secrets from your settings files should also be added in a similar method.

 1. **Azure Vault**. Use the [Azure Key Vault Secret client library for Python](https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-secrets). Set the client secret value in vault, naming it `CLIENT_SECRET` for example. Then set up the Azure key vault client in your app, and modify the `Sample/settings.py` file as follows:

    ```Python
    # find the following line in the settings file.
    AAD_CONFIG = AADConfig.parse_json(file_path='aad.config.json')
    # directly after the above line, add the following line:
    AAD_CONFIG.client.client_credential=secret_client.get_secret("secret-name")
    # Note: secret_client is your fully set up Azure Key Vault Secret client library for Python (https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-secrets). You must set it up as per instructions on the Azure Key Vault Secret client library for Python page.
    ```

 2. **Environment Variables** (*Azure Portal > App Services > `Your App` > Configuration*). You must set the value for `CLIENT_SECRET`. Modify the `Sample/settings.py` file as follows:

    ```Python
    # find the following line in the settings file.
    AAD_CONFIG = AADConfig.parse_json(file_path='aad.config.json')
    # directly after the above line, add the following line:
    AAD_CONFIG.client.client_credential=os.environ.get("secret-name")
    ```

</details>

Go to the Azure tab on VSCode. Under the `APP SERVICE` toolbox, right click the app name that you created in [Step 2: Prepare the app service and database](#step-2-prepare-the-app-service-and-database) (You may need to refresh the list with the refresh button on the toolbox). Choose `Deploy to Webapp`

## We'd love your feedback!

Were we successful in addressing your learning objective? Consider taking a moment to [share your experience with us](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR73pcsbpbxNJuZCMKN0lURpUM0dYSFlIMzdHT0o3NlRNVFpJSzcwRVMxRyQlQCN0PWcu).

## More information

- [Azure App Services](https://docs.microsoft.com/azure/app-service/)

For more information about how OAuth 2.0 protocols work in this scenario and other scenarios, see [Authentication Scenarios for Azure AD](https://docs.microsoft.com/azure/active-directory/develop/authentication-flows-app-scenarios).

## Community Help and Support

Use [Stack Overflow](http://stackoverflow.com/questions/tagged/msal) to get support from the community.
Ask your questions on Stack Overflow first and browse existing issues to see if someone has asked your question before.
Make sure that your questions or comments are tagged with [`azure-ad` `azure-ad-b2c` `ms-identity` `msal`].

If you find a bug in the sample, please raise the issue on [GitHub Issues](../../issues).

To provide a recommendation, visit the following [User Voice page](https://feedback.azure.com/forums/169401-azure-active-directory).

## Contributing

If you'd like to contribute to this sample, see [CONTRIBUTING.MD](../../CONTRIBUTING.md).

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information, see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
