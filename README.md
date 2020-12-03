# Deploy your Python applications to Azure Cloud and use Azure App Service to manage your operations

- [Deploy your Python applications to Azure Cloud and use Azure App Service to manage your operations](#deploy-your-python-applications-to-azure-cloud-and-use-azure-app-service-to-manage-your-operations)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Registration](#registration)
    - [Register the web app](#register-the-web-app)
  - [Deployment](#deployment)
    - [Step 1: Prepare the web app for deployment](#step-1-prepare-the-web-app-for-deployment)
    - [Step 2: Deploy the web app](#step-2-deploy-the-web-app)
    - [Step 3: Update your Azure AD App Registration](#step-3-update-your-azure-ad-app-registration)
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

### Step 1: Prepare the web app for deployment

You **may skip this step** if you are doing a test deployment with a development Azure Active Directory App registration that does not have any sensitive data. **It is not secure to deploy secrets in a config file to a production application**. To deploy your app more securely, you must:

1. Supply a config file that omits secrets (i.e., `aad.config.json` that sets `"client_credential": null`)
1. After you've deployed your app in the next sections, come back and add the secrets from a secure location such as:
   1. **Azure Vault**. Use the [Azure Key Vault Secret client library for Python](https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-secrets). Set the client secret value in vault, naming it `CLIENT_SECRET` for example. Then set up the Azure key vault client in your app, and modify the `settings.py` file as follows:

         ```Python
         AAD_CONFIG = AADConfig.parse_json(file_path='aad.config.json')
         # after the above line, add the following lines:
         secret_client = "...set up your Azure Key Vault Secret client library for Python here"
         AAD_CONFIG.client.client_credential=secret_client.get_secret("secret-name")
         ```

   1. **Environment Variables** (*Azure Portal > App Services > `Your App` > Configuration*). You must set the value for `CLIENT_SECRET`. Modify the `settings.py` file as follows:

         ```Python
         AAD_CONFIG = AADConfig.parse_json(file_path='aad.config.json')
         # after the above line, add the following line:
         AAD_CONFIG.client.client_credential=os.environ.get("secret-name")
         ```

1. In your app's `settings.py`, modify the allowed hosts as follows:

    ```Python
    ALLOWED_HOSTS = ['*']
    ```

    After your first deployment, ou will later come back to this and add the URL of your deployed app, along with localhost for subsequent deployments, i.e., `['example.azurewebsites.net', 'localhost']`

1. If you are sure you want to continue, proceed to [step 2](#step-2-deploy-the-web-app).

### Step 2: Deploy the web app

This guide is for deploying to **Azure App Service** via **VS Code Azure Tools Extension**.

> You may watch the first 3 minutes of this [video tutorial](https://www.youtube.com/watch?v=dNVvFttc-sA) offered by Microsoft Dev Radio to get a video walk through of app deployment with VS Code.

- Follow the instructions in steps 1, 2, 3 and 5 in the official [Microsoft docs Python deployment tutorial](https://docs.microsoft.com/azure/developer/python/tutorial-deploy-app-service-on-linux-01).

- Work with the [Enable your Python Django webapp to sign in users and call Microsoft Graph with the Microsoft identity platform](https://github.com/azure-samples/ms-identity-python-django-webapp-call-graph) sample or your own chosen Django sample instead of the sample listed in the tutorial.

- Disable App Service's default authentication:

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
