#!/bin/bash

# Check if the correct number of arguments is provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <add/delete> <script_name>"
    exit 1
fi

operation="$1"
script_name="$2"
file_path="/home/mechatronics/install/install/launch/startupConfig.json"

# Read the JSON file
json_data=$(<"$file_path")

# Determine the operation
if [ "$operation" == "add" ]; then
    # Check if the script name is already in the list
    if echo "$json_data" | grep -q "\"$script_name\""; then
        echo "Script '$script_name' is already in the list."
    else
        # If the script name is not in the list, add it
        updated_json=$(echo "$json_data" | jq --arg script "$script_name" '.scripts += [{"command": [$script]}]')
        echo "$updated_json" > "$file_path"
        echo "Script '$script_name' added to the list."
    fi
elif [ "$operation" == "delete" ]; then
    # Check if the script name is in the list
    if echo "$json_data" | grep -q "\"$script_name\""; then
        # If the script name is in the list, remove it
        updated_json=$(echo "$json_data" | jq '.scripts |= map(select(.command[0] != "'"$script_name"'"))')
        echo "$updated_json" > "$file_path"
        echo "Script '$script_name' removed from the list."
    else
        echo "Script '$script_name' is not in the list."
    fi
else
    echo "Invalid operation. Please specify 'add' or 'delete'."
    exit 1
fi
