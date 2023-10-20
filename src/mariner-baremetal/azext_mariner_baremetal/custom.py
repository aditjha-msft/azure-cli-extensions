# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError
from knack.log import get_logger

from ._constants import *
from azure.cli.core.commands.client_factory import get_subscription_id
from azure.cli.core.commands.validators import get_default_location_from_resource_group
from azure.cli.core._profile import Profile
import yaml, json, requests, uuid

logger = get_logger(__name__)


def create_mariner_baremetal_installer(
    cmd,
    resource_group_name,
    storage_account_name,
    blob_container_name,
    host_configuration,
    installer_name=DEFAULT_INSTALLER_RESOURCE_NAME,
    location=None,
    tags=None,
):
    # Get Entra Id (AAD) token
    profile = Profile(cmd.cli_ctx)
    access_token = profile.get_raw_token()[0][2].get("accessToken")
    if access_token is None:
        raise CLIError(
            "Error retrieving AAD access token! Please log in and try again."
        )

    location = (
        get_default_location_from_resource_group(cmd, resource_group_name)
        if location is None
        else location
    )

    # Create the PUT request URL
    endpoint_url = _construct_endpoint_url(
        get_subscription_id(cmd.cli_ctx), resource_group_name, installer_name
    )

    user_storage_account = _generate_storage_account_url(storage_account_name)

    # Read the host configuration file
    host_config = _create_host_config_dict(host_configuration)
    if host_config is None:
        raise CLIError("Error parsing provided host configuration file")

    # Create the PUT request
    req_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "x-ms-client-request-id": str(uuid.uuid1()),
    }
    logger.debug(f"Request headers: {req_headers}\n")

    # Generate the request body
    request_body = _generate_create_request_body(
        location, user_storage_account, blob_container_name, installer_name, host_config
    )
    logger.debug(f"Request body: {request_body}")

    response = requests.put(
        endpoint_url,
        headers=req_headers,
        data=request_body,
    )

    # Log the response
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response headers: {response.headers}")
    logger.debug(f"Response content: {response.json()}")

    # Check the response status code
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        logger.error(
            f"Failed to create Mariner Baremetal installer image {installer_name} with status code {response.status_code}"
        )


def list_mariner_baremetal_installer(
    cmd,
    resource_group_name,
    location=None,
    tags=None,
):
    # Get Entra Id (AAD) token
    profile = Profile(cmd.cli_ctx)
    access_token = profile.get_raw_token()[0][2].get("accessToken")
    if access_token is None:
        raise CLIError(
            "Error retrieving AAD access token! Please log in and try again."
        )

    location = (
        get_default_location_from_resource_group(cmd, resource_group_name)
        if location is None
        else location
    )

    # Create the GET request URL
    endpoint_url = _construct_endpoint_url(
        get_subscription_id(cmd.cli_ctx), resource_group_name, None
    )

    # Create the GET request
    req_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "x-ms-client-request-id": str(uuid.uuid1()),
    }
    logger.debug(f"Request headers: {req_headers}\n")

    response = requests.get(
        endpoint_url,
        headers=req_headers,
    )

    # Log the response
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response headers: {response.headers}")
    logger.debug(f"Response content: {response.json()}")

    # Check the response status code
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        logger.error(
            f"Failed to list Mariner Baremetal installer image resources with status code {response.status_code}"
        )


def show_mariner_baremetal_installer(
    cmd,
    resource_group_name,
    installer_name,
    location=None,
    tags=None,
):
    # Get Entra Id (AAD) token
    profile = Profile(cmd.cli_ctx)
    access_token = profile.get_raw_token()[0][2].get("accessToken")
    if access_token is None:
        raise CLIError(
            "Error retrieving AAD access token! Please log in and try again."
        )

    location = (
        get_default_location_from_resource_group(cmd, resource_group_name)
        if location is None
        else location
    )

    # Create the GET request URL
    endpoint_url = _construct_endpoint_url(
        get_subscription_id(cmd.cli_ctx), resource_group_name, installer_name
    )

    # Create the GET request
    req_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "x-ms-client-request-id": str(uuid.uuid1()),
    }
    logger.debug(f"Request headers: {req_headers}")

    response = requests.get(
        endpoint_url,
        headers=req_headers,
    )

    # Log the response
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response headers: {response.headers}")
    logger.debug(f"Response content: {response.json()}")

    # Check the response status code
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        logger.error(
            f"Failed to show Mariner Baremetal installer image {installer_name} with status code {response.status_code}"
        )


def delete_mariner_baremetal_installer(
    cmd,
    resource_group_name,
    installer_name,
    location=None,
    tags=None,
):
    # Get Entra Id (AAD) token
    profile = Profile(cmd.cli_ctx)
    access_token = profile.get_raw_token()[0][2].get("accessToken")
    if access_token is None:
        raise CLIError(
            "Error retrieving AAD access token! Please log in and try again."
        )

    location = (
        get_default_location_from_resource_group(cmd, resource_group_name)
        if location is None
        else location
    )

    # Create the DELETE request URL
    endpoint_url = _construct_endpoint_url(
        get_subscription_id(cmd.cli_ctx), resource_group_name, installer_name
    )

    # Create the DELETE request
    req_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "x-ms-client-request-id": str(uuid.uuid1()),
    }
    logger.debug(f"Request headers: {req_headers}")

    response = requests.delete(
        endpoint_url,
        headers=req_headers,
    )

    # # Log the response
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response headers: {response.headers}")

    # # Check the response status code
    if response.status_code == 200:
        print(
            f"Successfully deleted Mariner Baremetal installer image {installer_name}"
        )
    elif response.status_code == 204:
        print(f"Already deleted Mariner Baremetal installer image {installer_name}")
    else:
        logger.error(
            f"Failed to delete Mariner Baremetal installer image {installer_name} with status code {response.status_code}"
        )


# Helper functions for processing input data


def _generate_storage_account_url(storage_account_name):
    # Define the base URL template
    base_url = "https://{}.blob.core.windows.net/"

    # Use string formatting to insert the storage account name into the URL
    storage_account_url = base_url.format(storage_account_name)
    return storage_account_url


def _construct_endpoint_url(sub_id, resource_group_name, name):
    base_url = BASE_ENDPOINT_URL
    api_version = DEFAULT_API_VERSION

    # If no name is provided, return the URL template for listing all resources
    if name is None:
        endpoint_url = f"{base_url}subscriptions/{sub_id}/resourcegroups/{resource_group_name}/providers/{USER_RP_NAME}/installerimage?api-version={api_version}"
        return endpoint_url

    # Use string formatting to insert the parameters into the URL template
    endpoint_url = f"{base_url}subscriptions/{sub_id}/resourcegroups/{resource_group_name}/providers/{USER_RP_NAME}/installerimage/{name}?api-version={api_version}"

    return endpoint_url


def _create_host_config_dict(host_configuration_path):
    try:
        with open(host_configuration_path, "r") as host_config:
            host_config_data = yaml.safe_load(host_config)
            return host_config_data
    except Exception as e:
        logger.error(f"Error parsing host configuration file: {e}")
        return None


def _generate_create_request_body(
    location, storage_account, blob_container, installer_file, host_config
):
    # Define the request body template
    request_body = {
        "location": location,
        "properties": {
            "blob-storage-configuration": {
                "account-url": storage_account,
                "container-name": blob_container,
                "blob-name": installer_file,
            },
            "host-configuration": host_config["host-configuration"],
        },
    }
    json_request_body = json.dumps(request_body)
    return json_request_body
