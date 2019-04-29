# No spaces between values
Value INTERFACE (\S+)
Value VENDOR (\S+)
Value SERIAL (\S+)
Value PARTNUMBER (\S+)
Value CURRENTINST (\S+)
Value CURRENTMIN (\S+)
Value CURRENTMAX (\S+)
Value CURRENT_TX (\S+)
Value MAX_TX (\S+)
Value MIN_TX (\S+)
Value CURRENT_RX (\S+)
Value MAX_RX (\S+)
Value MIN_RX (\S+)

Start
  ^Vendor\s+\:\s+${VENDOR} 
  ^Part Number\s+\:\s+${PARTNUMBER}
  ^Serial Number\s+\:\s+${SERIAL} 
  ^10GigabitEthernet ${INTERFACE} 
  ^Tx Bias\(mA\)\s+${CURRENTINST}\s+${CURRENTMAX}\s+\S+\s+\S+\s+${CURRENTMIN} 
  ^Tx Power\(mW\)\s+${CURRENT_TX}\s+${MAX_TX}\s+\S+\s+\S+\s+${MIN_TX} 
  ^Rx Power\(mW\)\s+${CURRENT_RX}\s+${MAX_RX}\s+\S+\s+\S+\s+${MIN_RX} -> Record
  
EOF
