# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from azure.cli.core.commands import CliCommandType


def load_command_table(self, _):
    with self.command_group("mariner-baremetal", is_preview=True) as g:
        pass
        # g.generic_update_command('update', setter_name='update', custom_func_name='update_mariner-baremetal')

    with self.command_group("mariner-baremetal installer", is_preview=True) as g:
        g.custom_command("create", "create_mariner_baremetal_installer")
        g.custom_command("update", "create_mariner_baremetal_installer")
        g.custom_command("list", "list_mariner_baremetal_installer")
        g.custom_command("show", "show_mariner_baremetal_installer")
        g.custom_command("delete", "delete_mariner_baremetal_installer")
