# -*- coding: utf-8 -*-
"""
Napalm driver for Microsemi switches running SMBStaX.

# Copyright 2019 Carles.Kishimoto@gmail.com. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

Read https://napalm.readthedocs.io for more information.
"""

from netmiko import ConnectHandler
from napalm.base import NetworkDriver
from napalm.base.exceptions import (
   ConnectionException,
)
import napalm.base.helpers


class SMBStaXDriver(NetworkDriver):
    """Napalm driver for Microsemi switches running SMBStaX."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Napalm driver for Microsemi switches running SMBStaX."""
        if optional_args is None:
            optional_args = {}

        self.device = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.port = optional_args.get('port', 22)

    def open(self):
        """Connect with the device."""
        try:
            self.device = ConnectHandler(device_type='cisco_ios_telnet',
                                         ip=self.hostname,
                                         port=self.port,
                                         username=self.username,
                                         password=self.password,
                                         timeout=self.timeout,
                                         verbose=True)
        except Exception:
            raise ConnectionException("Cannot connect to switch: %s:%s" % (self.hostname, self.port))

    def close(self):
        """Disconnect from the device."""
        self.device.disconnect()

    def cli(self, commands):
        """Run any cli command."""
        cli_output = dict()
        if type(commands) is not list:
            raise TypeError('Please enter a valid list of commands!')

        for com in commands:
            output = self.device.send_command(com)
            if ('Invalid input' or 'Incomplete command') in output:
                raise ValueError('Unable to execute command "{}"'.format(com))
            cli_output.setdefault(com, {})
            cli_output[com] = output

        return cli_output

    def get_arp_table(self):
        """
        Return a list of dictionaries having the following set of keys.

        interface (string)
        mac (string)
        ip (string)
        age (float)
        """
        arp_table = list()

        output = self.device.send_command('show ip arp')
        output = output.split('\n')

        for line in output:
            fields = line.split()

            if len(fields) == 3:
                address, via, vlan_mac = fields
                vlan, mac = vlan_mac.split(":")
                entry = {
                    'interface': vlan,
                    'mac': napalm.base.helpers.mac(mac),
                    'ip': address,
                    'age': -1
                }
                arp_table.append(entry)

        return arp_table

    def get_mac_address_table(self):
        """
        Return a list of dictionaries.

        Each dictionary represents an entry in the MAC Address Table, having the following keys:

        mac (string)
        interface (string)
        vlan (int)
        active (boolean)
        static (boolean)
        moves (int)
        last_move (float)
        """
        mac_table = list()

        output = self.device.send_command('show mac address-table')
        output = output[1:]
        output = output.split('\n')

        for line in output:
            fields = line.split()

            if len(fields) == 5:
                dynamic, vlan, mac, iface, port = fields
                # FIXME: Include also static mac entries
                if 'Dynamic' in dynamic:
                    entry = {
                        'interface': iface + port,
                        'mac': napalm.base.helpers.mac(mac),
                        'vlan': vlan,
                        'static': False,
                        'active': True,
                        'moves': -1,
                        'last_move': -1
                    }
                    mac_table.append(entry)

        return mac_table
