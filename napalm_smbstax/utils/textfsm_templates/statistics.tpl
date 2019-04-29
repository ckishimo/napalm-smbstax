# No spaces between values
Value INTERFACE (\S+)
Value RX_PACKETS (\d+)
Value TX_PACKETS (\d+)
Value RX_OCTETS (\d+)
Value TX_OCTETS (\d+)
Value RX_UNICAST (\d+)
Value TX_UNICAST (\d+)
Value RX_MULTICAST (\d+)
Value TX_MULTICAST (\d+)
Value RX_BROADCAST (\d+)
Value TX_BROADCAST (\d+)
Value RX_PAUSE (\d+)
Value TX_PAUSE (\d+)
Value RX_DROPS (\d+)
Value TX_DROPS (\d+)
Value CRC (\d+)
Value UNDERSIZE (\d+)
Value OVERSIZE (\d+)
Value FRAGMENTS (\d+)
Value JABBERS (\d+)
Value FILTERED (\d+)

Start
  ^(10GigabitEthernet|GigabitEthernet)\s+${INTERFACE}\s+Statistics:
  ^Rx Packets:\s+${RX_PACKETS}\s+Tx Packets:\s+${TX_PACKETS}
  ^Rx Octets:\s+${RX_OCTETS}\s+Tx Octets:\s+${TX_OCTETS}
  ^Rx Unicast:\s+${RX_UNICAST}\s+Tx Unicast:\s+${TX_UNICAST}
  ^Rx Multicast:\s+${RX_MULTICAST}\s+Tx Multicast:\s+${TX_MULTICAST}
  ^Rx Broadcast:\s+${RX_BROADCAST}\s+Tx Broadcast:\s+${TX_BROADCAST}
  ^Rx Pause:\s+${RX_PAUSE}\s+Tx Broadcast:\s+${TX_PAUSE}  
  ^Rx Drops:\s+${RX_DROPS}\s+Tx Drops:\s+${TX_DROPS}
  ^Rx CRC/Alignment:\s+${CRC}
  ^Rx Undersize:\s+${UNDERSIZE}
  ^Rx Oversize:\s+${OVERSIZE}
  ^Rx Fragments:\s+${FRAGMENTS}
  ^Rx Jabbers:\s+${JABBERS}
  ^Rx Filtered:\s+${FILTERED} -> Record
 
EOF
