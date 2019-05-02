# SMBStaX
NAPALM Driver for Microsemi/SMBStaX switches

- Supported methods:
   - cli()
   - get_arp_table()
   - get_mac_address_table()
   - get_config()
   - get_optics()
   - get_interfaces_counters()
   - get_lldp_neighbors()
   - get_lldp_neighbors_detail()

- Example: Get the counters in all interfaces
```
res = dev.get_interfaces_counters()
print(json.dumps(res, sort_keys=True, indent=4))
exit()

# Output
{
    "10GigabitEthernet 1/4": {
        "rx_broadcast_packets": "0",
        "rx_discards": 0,
        "rx_errors": "0",
        "rx_multicast_packets": "0",
        "rx_octets": "0",
        "rx_unicast_packets": "0",
        "tx_broadcast_packets": "11",
        "tx_discards": 0,
        "tx_errors": -1,
        "tx_multicast_packets": "14",
        "tx_octets": "2408",
        "tx_unicast_packets": "2408"
    },
    "GigabitEthernet 1/1": {
        "rx_broadcast_packets": "0",
        "rx_discards": 0,
        "rx_errors": "0",
        "rx_multicast_packets": "8729",
        "rx_octets": "1117312",
        "rx_unicast_packets": "1117312",
        "tx_broadcast_packets": "11",
        "tx_discards": 0,
        "tx_errors": -1,
        "tx_multicast_packets": "190703",
        "tx_octets": "20640220",
        "tx_unicast_packets": "20640220"
    },
    ...
}
```
