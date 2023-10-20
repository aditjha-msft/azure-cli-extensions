# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType


def load_arguments(self, _):
    from azure.cli.core.commands.parameters import tags_type
    from azure.cli.core.commands.validators import (
        get_default_location_from_resource_group,
    )

    with self.argument_context("mariner-baremetal installer") as c:
        c.argument(
            "host_configuration",
            options_list=["--host-configuration", "-hc"],
            help="Path to the host configuration file for use on baremetal machine.",
        )
        c.argument(
            "resource_group_name",
            options_list=["--resource-group", "-g"],
            help="Name of Azure resource group where the installer image resource will be created.",
        )
        c.argument(
            "installer_name",
            options_list=["--installer-name", "-n"],
            help="Name of the installer image resource.",
        )
        c.argument(
            "storage_account_name",
            options_list=["--storage-account-name", "-s"],
            help="Name of the storage account to upload the installer image ISO.",
        )
        c.argument(
            "blob_container_name",
            options_list=["--blob-container-name", "-c"],
            help="Name of the blob container to upload the installer image ISO.",
        )
        c.argument("tags", tags_type)
        c.argument("location", validator=get_default_location_from_resource_group)
