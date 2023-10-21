# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps  # pylint: disable=unused-import


helps[
    "mariner-baremetal"
] = """
    type: group
    short-summary: CLI Extension to create Mariner Baremetal Installer Images through Azure.
"""

helps[
    "mariner-baremetal installer"
] = """
    type: group
    short-summary: CLI Extension to create Mariner Baremetal Installer Images through Azure.
"""

helps[
    "mariner-baremetal installer create"
] = """
    type: command
    short-summary: Creates the Baremetal Installer Image resource.
"""

helps[
    "mariner-baremetal installer list"
] = """
    type: command
    short-summary: Lists the Baremetal Installer Image resources by resource group.
"""

helps[
    "mariner-baremetal installer show"
] = """
    type: command
    short-summary: Gets the Baremetal Installer Image resource.
"""

helps[
    "mariner-baremetal installer delete"
] = """
    type: command
    short-summary: Deletes the Baremetal Installer Image resource.
"""
