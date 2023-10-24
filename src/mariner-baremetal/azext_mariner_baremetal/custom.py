# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long
# pylint: disable=broad-except
# pylint: disable=unused-argument
# pylint: disable=wildcard-import

import json
import uuid
import requests
import yaml

from knack.util import CLIError
from knack.log import get_logger
from azure.cli.core._profile import Profile
from azure.cli.core.commands.client_factory import get_subscription_id
from ._constants import *


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
    access_token = _get_access_token(cmd)

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
    req_headers = _set_request_headers(access_token)

    # Generate the request body
    request_body = _generate_create_request_body(
        location, user_storage_account, blob_container_name, installer_name, host_config
    )

    # Create the PUT request
    response = requests.put(
        endpoint_url,
        headers=req_headers,
        data=request_body,
        timeout=DEFAULT_TIMEOUT,
    )
    _log_response(response, "create")


def list_mariner_baremetal_installer(cmd, resource_group_name):
    # Get Entra Id (AAD) token
    access_token = _get_access_token(cmd)

    # Create the GET request URL
    endpoint_url = _construct_endpoint_url(
        get_subscription_id(cmd.cli_ctx), resource_group_name, None
    )

    # Create the GET request
    req_headers = _set_request_headers(access_token)

    response = requests.get(
        endpoint_url,
        headers=req_headers,
        timeout=DEFAULT_TIMEOUT,
    )
    _log_response(response, "list")


def show_mariner_baremetal_installer(
    cmd,
    resource_group_name,
    installer_name,
):
    # Get Entra Id (AAD) token
    access_token = _get_access_token(cmd)

    # Create the GET request URL
    endpoint_url = _construct_endpoint_url(
        get_subscription_id(cmd.cli_ctx), resource_group_name, installer_name
    )

    # Create the GET request
    req_headers = _set_request_headers(access_token)

    response = requests.get(
        endpoint_url,
        headers=req_headers,
        timeout=DEFAULT_TIMEOUT,
    )
    _log_response(response, "show")


def delete_mariner_baremetal_installer(cmd, resource_group_name, installer_name):
    # Get Entra Id (AAD) token
    access_token = _get_access_token(cmd)

    # Create the DELETE request URL
    endpoint_url = _construct_endpoint_url(
        get_subscription_id(cmd.cli_ctx), resource_group_name, installer_name
    )

    # Create the DELETE request
    req_headers = _set_request_headers(access_token)

    response = requests.delete(
        endpoint_url,
        headers=req_headers,
        timeout=DEFAULT_TIMEOUT,
    )
    _log_response(response, "delete")


# Helper functions for processing input data


def _get_access_token(cmd):
    profile = Profile(cmd.cli_ctx)
    access_token = profile.get_raw_token()[0][2].get("accessToken")
    if access_token is None:
        raise CLIError(
            "Error retrieving AAD access token! Please log in and try again."
        )
    return access_token


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
        with open(host_configuration_path, "r", encoding="utf-8") as host_config:
            host_config_data = yaml.safe_load(host_config)
            return host_config_data
    except Exception as e:
        logger.error("Error parsing host configuration file: %s", e)
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
    logger.debug("Request body: %s", json_request_body)
    return json_request_body


def _set_request_headers(access_token):
    req_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "x-ms-client-request-id": str(uuid.uuid1()),
    }
    logger.debug("Request headers: %s", req_headers)
    return req_headers


def _log_response(response, method):
    logger.debug("Response status code: %d", response.status_code)
    logger.debug("Response headers: %s", response.headers)
    # Delete operation doesn't have a response body
    if method == "delete":
        if response.status_code == 200:
            print("Successfully deleted Mariner Baremetal installer image resource")
        else:
            logger.error(
                "Failed to delete Mariner Baremetal installer image resource with status code: %d",
                response.status_code,
            )
    else:
        logger.debug("Response content: %s", response.content)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            logger.error(
                "Failed to %s Mariner Baremetal installer image resource with status code: %d",
                method,
                response.status_code,
            )
            logger.error("Response content: %s", response.json())
