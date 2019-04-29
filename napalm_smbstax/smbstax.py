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
from napalm.base.exceptions import ConnectionException
import napalm.base.helpers

import os
import sys
from pprint import pprint


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
        self.port = optional_args.get("port", 22)

    def open(self):
        """Connect with the device."""
        try:
            self.device = ConnectHandler(
                device_type="cisco_ios_telnet",
                ip=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=self.timeout,
                verbose=True,
            )
        except Exception:
            raise ConnectionException(
                "Cannot connect to switch: %s:%s" % (self.hostname, self.port)
            )

    def close(self):
        """Disconnect from the device."""
        self.device.disconnect()

    def cli(self, commands):
        """Run any cli command."""
        cli_output = dict()
        if type(commands) is not list:
            raise TypeError("Please enter a valid list of commands!")

        for com in commands:
            output = self.device.send_command(com)
            if ("Invalid input" or "Incomplete command") in output:
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
        age (float)         : Not supported
        """
        arp_table = list()

        output = self.device.send_command("show ip arp")
        output = output.split("\n")

        for line in output:
            fields = line.split()

            if len(fields) == 3:
                address, via, vlan_mac = fields
                vlan, mac = vlan_mac.split(":")
                entry = {
                    "interface": vlan,
                    "mac": napalm.base.helpers.mac(mac),
                    "ip": address,
                    "age": -1,
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
        static (boolean)    : Not implemented
        moves (int)         : Not supported
        last_move (float)   : Not supported
        """
        mac_table = list()

        output = self.device.send_command("show mac address-table")
        output = output[1:]
        output = output.split("\n")

        for line in output:
            fields = line.split()

            if len(fields) == 5:
                dynamic, vlan, mac, iface, port = fields
                # FIXME: Include also static mac entries
                if "Dynamic" in dynamic:
                    entry = {
                        "interface": iface + port,
                        "mac": napalm.base.helpers.mac(mac),
                        "vlan": vlan,
                        "static": False,
                        "active": True,
                        "moves": -1,
                        "last_move": -1,
                    }
                    mac_table.append(entry)

        return mac_table

    def get_config(self, retrieve=u"all"):
        """
        Return the configuration of a device.

        The object returned is a dictionary with a key for each configuration stored.
        """
        configs = {"startup": "", "running": "", "candidate": ""}
        # Candidate: Device doesn't differentiate between running and startup configuration
        # this will an empty string
        if retrieve in ("startup", "all"):
            command = "more flash:startup-config"
            output = self.device.send_command(command)
            configs["startup"] = output

        if retrieve in ("running", "all"):
            command = "show running-config"
            output = self.device.send_command(command)
            configs["running"] = output

        return configs

    def get_optics(self):
        """
        Fetches the power usage on the various transceivers installed.
        Returns a dictionary
        """
        output = {}

        _data = napalm.base.helpers.textfsm_extractor(
            self,
            "optics",
            self.device.send_command("show interface 10GigabitEthernet * transceiver"),
        )
        if _data:
            # FIXME: Only 10GbE has been tested
            # FIXME: Need to complete with the rest of information
            for d in _data:
                values = {}
                values["index"] = 0
                values["state"] = {}
                values["state"]["input_power"] = {}
                values["state"]["input_power"]["instant"] = 0
                values["state"]["input_power"]["avg"] = d["current_rx"]
                values["state"]["input_power"]["min"] = d["min_rx"]
                values["state"]["input_power"]["max"] = d["max_rx"]

                output[d["interface"]] = {}
                output[d["interface"]]["physical_channels"] = {}
                output[d["interface"]]["physical_channels"]["channel"] = values

        return output

    def get_interfaces_counters(self):
        """
        Returns a dictionary of dictionaries

        The first key is an interface name and the inner dictionary contains

        tx_errors (int)
        rx_errors (int)
        tx_discards (int)
        rx_discards (int)
        tx_octets (int)
        rx_octets (int)
        tx_unicast_packets (int)
        rx_unicast_packets (int)
        tx_multicast_packets (int)
        rx_multicast_packets (int)
        tx_broadcast_packets (int)
        rx_broadcast_packets (int)
        """
        output = {}

        _data = napalm.base.helpers.textfsm_extractor(
            self, "statistics", self.device.send_command("show interface * statistics")
        )
        if _data:
            for iface in _data:
                name = iface["interface"]

                output[name] = {}
                output[name]["tx_multicast_packets"] = iface["tx_multicast"]
                output[name]["rx_multicast_packets"] = iface["rx_multicast"]
                output[name]["tx_broadcast_packets"] = iface["tx_broadcast"]
                output[name]["rx_broadcast_packets"] = iface["rx_broadcast"]
                output[name]["tx_unicast_packets"] = iface["tx_octets"]
                output[name]["rx_unicast_packets"] = iface["rx_octets"]
                # FIXME: drops ?
                output[name]["tx_discards"] = 0
                output[name]["rx_discards"] = 0
                output[name]["tx_errors"] = -1
                output[name]["rx_errors"] = iface["crc"]
                output[name]["tx_octets"] = iface["tx_octets"]
                output[name]["rx_octets"] = iface["rx_octets"]

        return output

    def get_probes_results(self):
        raise NotImplemented

    def get_probes_config(self):
        raise NotImplemented

    def traceroute(self):
        raise NotImplemented

    def ping(self):
        raise NotImplemented

    def rollback(self):
        raise NotImplemented

    def pre_connection_tests(self):
        raise NotImplemented

    def post_connection_tests(self):
        raise NotImplemented

    def load_template(self):
        raise NotImplemented

    def load_replace_candidate(self):
        raise NotImplemented

    def load_merge_candidate(self):
        raise NotImplemented

    def is_alive(self):
        raise NotImplemented

    def get_users(self):
        raise NotImplemented

    def get_snmp_information(self):
        raise NotImplemented

    def get_route_to(self):
        raise NotImplemented

    def get_probes_results(self):
        raise NotImplemented

    def get_probes_config(self):
        raise NotImplemented

    def get_ntp_stats(self):
        raise NotImplemented

    def get_ntp_servers(self):
        raise NotImplemented

    def get_ntp_peers(self):
        raise NotImplemented

    def get_network_instances(self):
        raise NotImplemented

    def get_lldp_neighbors_detail(self):
        raise NotImplemented

    def get_lldp_neighbors(self):
        raise NotImplemented

    def get_ipv6_neighbors_table(self):
        raise NotImplemented

    def get_interfaces_ip(self):
        raise NotImplemented

    def get_interfaces(self):
        raise NotImplemented

    def get_firewall_policies(self):
        raise NotImplemented

    def get_facts(self):
        raise NotImplemented

    def get_environment(self):
        raise NotImplemented

    def get_bgp_neighbors_detail(self):
        raise NotImplemented

    def get_bgp_neighbors(self):
        raise NotImplemented

    def get_bgp_config(self):
        raise NotImplemented

    def discard_config(self):
        raise NotImplemented

    def connection_tests(self):
        raise NotImplemented

    def compliance_report(self):
        raise NotImplemented

    def compare_config(self):
        raise NotImplemented

    def commit_config(self):
        raise NotImplemented
