import os
import re


def custom_sort_key(filename):
    # Extract job, arg, and size
    match = re.match(r"traces/([^_]+)_([^_]+)_(\d+)\.sqlite3", filename)
    if match:
        job = match.group(1)
        arg = match.group(2)
        size = int(match.group(3))
        return (job, arg, size)
    else:
        return ("", "", 0)  # Fallback for unexpected formats


def one_time_create_trace_db_file(folder_path, destination_folder_path):
    file_list = os.listdir(folder_path)
    file_list = [item for item in file_list if ".sqlite3" in item]
    destination_file_list = [os.path.join(destination_folder_path, item) for item in file_list]
    destination_file_list.sort(key=custom_sort_key)
    print(f"{len(destination_file_list)} traces collected")
    with open("db.txt", "w") as f:
        for item in destination_file_list:
            f.write(f"{item}\n")


if __name__ == "__main__":
    one_time_create_trace_db_file("traces", "traces/")
