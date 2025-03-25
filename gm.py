import json
import threading
import os
GROUPS_FILE = 'groups.json'
lock = threading.Lock()

# Load groups from file
def load_groups():
    try:
        with open(GROUPS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # No groups exist yet

# Save groups to file
def save_groups(groups):
    with open(GROUPS_FILE, 'w') as f:
        json.dump(groups, f, indent=4)

#yw
def priorget_next_group():
    with lock:
        #try:
            #create_groups_json('xgroups.txt','groups.json')
        #except:
            #pass
        groups = load_groups()
        # Prioritize groups based on their status (0 first, then 1, etc., -1 at the end)
        groups.sort(key=lambda group: group['status'] if group['status'] != 'invalid' else float('inf'))

        for group in groups:
            if group['status'] >= 0:  # Valid groups
                group['status'] += 1  # Increment priority to avoid re-selection too soon
                save_groups(groups)
                return group['id']

        # Handle temporary invalid groups (-1) if no valid groups are found
        for group in groups:
            if group['status'] == -1:
                group['status'] += 1  # Mark them as being processed
                save_groups(groups)
                return group['id']

        return None  # No available groups


def mark_group_temporary_invalid(group_id):
    with lock:
        groups = load_groups()
        for group in groups:
            if group['id'] == group_id:
                group['status'] = -1  # Mark as temporarily invalid
                save_groups(groups)
                print(f"Group {group_id} marked as temporarily invalid.")
                return
        print(f"Group {group_id} not found. Cannot mark as temporarily invalid.")


def mark_group_invalid(group_id):
    with lock:
        groups = load_groups()
        for group in groups:
            if group['id'] == group_id:
                group['status'] = "invalid"  # Mark as permanently invalid
                save_groups(groups)
                print(f"Group {group_id} marked as permanently invalid.")
                return
        print(f"Group {group_id} not found. Cannot mark as permanently invalid.")



# Get the next available group (with None status)
def fget_next_group():
    with lock:
        groups = load_groups()
        for group in groups:
            if group['status'] is None:
                assigned_group = group
                groups.remove(group)
                save_groups(groups)
                return assigned_group['id']
        return None  # No available groups

# Add a group back to the list with an error status
def add_group_back(group_id, error_message):
    with lock:
        groups = load_groups()
        groups.append({'id': group_id, 'status': error_message})
        save_groups(groups)



import os
#thiss
def anotherget_next_group() -> str:
    file_path = "xgroups.txt"
    temp_file_path = file_path + ".tmp"
    try:
        with open(file_path, 'r') as file:
            groups = file.readlines()

        if not groups:
            print("No groups available.")
            return None

        # Rotate the first line to the end
        group = groups.pop(0).strip()
        groups.append(group + '\n')

        # Write the updated list to a temporary file
        with open(temp_file_path, 'w') as temp_file:
            temp_file.writelines(groups)

        # Replace the original file atomically
        os.replace(temp_file_path, file_path)

        return group

    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_next_group():
    try:
        file_path = 'xgroups.txt'
        # Open the file in read and write mode ('r+' allows reading and writing)
        with open(file_path, "r+") as file:
            # Read the first line
            first_line = file.readline().strip()

            if not first_line:
                print("The file is empty.")
                return None

            # Read the remaining lines and write them back, effectively removing the first line
            remaining_lines = file.read()
            file.seek(0)  # Move the pointer back to the beginning of the file
            file.write(remaining_lines)  # Write the rest of the content back to the file
            file.truncate()  # Remove any leftover data after the new content

        return first_line

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


lock = threading.Lock()

# Function to get the next group
def newget_next_group() -> str:
    file_path = "xgroups.txt"
    with lock:  # Ensure only one thread accesses this section at a time
        try:
            with open(file_path, 'r') as file:
                groups = file.readlines()

            if not groups:
                print("No groups available.")
                return None

            # Get the top group, remove it from the top, and append it to the end
            group = groups.pop(0).strip()
            groups.append(group + '\n')

            # Write the updated list back to the file
            with open(file_path, 'w') as file:
                file.writelines(groups)

            return group

        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return None

#def create_groups_json()
def create_groups_json(input_file, output_file):
    #print('called')
    with open(input_file, 'r') as f:
        group_ids = f.readlines()
    group_ids = [group_id.strip() for group_id in group_ids]

    try:
        with open(output_file, 'r') as f:
            existing_groups = json.load(f)
    except FileNotFoundError:
        existing_groups = []

    # Keep valid groups and reset their status to 0
    for group in existing_groups:
        #print("also did")
        if group['status'] != "invalid":
                group['status'] = 0  # Reset valid groups
        # Leave invalid groups unchanged

    # Add new groups
    existing_ids = {group['id'] for group in existing_groups}
    for group_id in group_ids:
        if group_id not in existing_ids:
            existing_groups.append({'id': group_id, 'status': 0})  # New groups start with status 0

    with open(output_file, 'w') as f:
        json.dump(existing_groups, f, indent=4)

def write_unique_lines(source_file: str, target_file: str):
    try:
        # Read lines from source file and remove duplicates
        with open(source_file, 'r') as src:
            unique_lines = set(line.strip() for line in src if line.strip())

        # Write unique lines to target file
        with open(target_file, 'w') as tgt:
            for line in sorted(unique_lines):  # Sorted for consistent output, optional
                tgt.write(line + '\n')

        print(f"Unique lines from {source_file} have been written to {target_file}.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def fcreate_groups_json(input_file, output_file):
    #load existing groups from the JSON file if it exists
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r') as f:
                existing_groups_data = json.load(f)
                existing_groups = {group['id'] for group in existing_groups_data}
        except Exception as e:
            print(f"Error reading existing JSON file: {e}")

    # Read new groups from the input file
    new_groups = []
    try:
        with open(input_file, 'r') as f:
            for line in f:
                group_id = line.strip()
                if group_id and group_id not in existing_groups:
                    new_groups.append({'id': group_id, 'status': None})
    except FileNotFoundError:
        print(f"Input file {input_file} not found.")
        return

    # Combine existing and new groups
    combined_groups = []
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            combined_groups = json.load(f)  # Keep existing groups
    combined_groups.extend(new_groups)

    # Save the updated group list to the JSON file
    try:
        with open(output_file, 'w') as f:
            json.dump(combined_groups, f, indent=4)
        print(f"Groups successfully updated in {output_file}.")
    except Exception as e:
        print(f"Error saving updated groups: {e}")

# Example usage
#create_groups_json('xgroups.txt', 'groups.json')

# Function to mark a group as invalid
def mark_invalid(group_str):
    file_path = "xgroups.txt"
    with lock:  # Ensure thread safety
        try:
            with open(file_path, 'r') as file:
                groups = file.readlines()

            # Remove the group if it exists
            groups = [group for group in groups if group.strip() != group_str]

            # Write the updated list back to the file
            with open(file_path, 'w') as file:
                file.writelines(groups)

            print(f"Group '{group_str}' marked as invalid and removed.")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
