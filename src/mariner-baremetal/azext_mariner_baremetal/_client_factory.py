# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands.client_factory import get_mgmt_service_client

from azure.cli.core.profiles import ResourceType


def cf_mariner_baremetal(cli_ctx, *_):
    return None


# def get_resource_groups_client(cli_ctx, subscription_id=None):
#     return get_mgmt_service_client(
#         cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES, subscription_id=subscription_id
#     ).resource_groups
