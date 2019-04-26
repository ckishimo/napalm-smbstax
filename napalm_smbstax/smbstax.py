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

    def get_version(self):
        """Get the current version from the device."""
        return self.cli(['show version'])