Value local_interface (.*)
# Missing: parent_interface
Value remote_chassis_id (\S+)
Value remote_system_name (\S+)
Value remote_port (\S+)
Value remote_port_description (.*)
Value remote_system_description (.*)
Value remote_system_capab (.*)
# Missing: remote_system_enable_capab

Start
  ^Local Interface\s+:\s+${local_interface}
  ^Chassis ID\s+:\s+${remote_chassis_id}
  ^Port ID\s+:\s+${remote_port}
  ^Port Description\s+:\s+${remote_port_description}
  ^System Name\s+:\s+${remote_system_name}
  ^System Description\s+:\s+${remote_system_description}
  ^System Capabilities\s+:\s+${remote_system_capab} -> Record

EOF
