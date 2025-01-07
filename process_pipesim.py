import os
import re
import subprocess


def one_time_pipesim(input_file_path, main_path):
    # Read all strings from the input file and save them in a list
    with open(input_file_path, "r") as file:
        file_list = [line.strip() for line in file if line.strip()]

    # Prepare the output file
    records_file = "pipesim_records.txt"
    if not os.path.exists(records_file):
        with open(records_file, "w") as f:
            f.write("job_name,argparse_flag,params,init_time,run_time,virtual_time\n")

    # Save the original directory
    original_path = os.getcwd()

    # Process each string
    total_files = len(file_list)
    for index, one_str in enumerate(file_list, start=1):
        print(f"[{index:02d}/{total_files:02d}] Start: {one_str}")

        # Extract job_name, argparse_flag, and params
        match = re.match(r"traces/([^_]+)_([^_]+)_(\d+)\.sqlite3", one_str)
        if not match:
            print(f"Skipping invalid format: {one_str}")
            continue

        job_name, argparse_flag, params = match.groups()
        argparse_flag = f"-{argparse_flag}"  # Add "-" before the argparse_flag

        # Change to the main path
        os.chdir(main_path)

        # Run the go command
        command = f"go run pipesim/main.go -database {one_str} -config=config.json"
        print(f"[{index:02d}/{total_files:02d}] Command: {command}")
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)

        # Parse the output
        output_lines = result.stdout.strip().split("\n")
        if len(output_lines) < 3:
            print(f"Unexpected output format: {result.stdout}")
            os.chdir(original_path)
            continue

        init_time = float(output_lines[0].split(":")[1].strip().replace("ms", "")) / 1000
        run_time = float(output_lines[1].split(":")[1].strip().replace("ms", "")) / 1000
        virtual_time = float(output_lines[2].split(":")[1].strip())

        # Change back to the original directory
        os.chdir(original_path)

        # Write the record to the file
        record = f"{job_name},{argparse_flag},{params},{init_time},{run_time},{virtual_time}\n"
        with open(records_file, "a") as f:
            f.write(record)

        # Print finish message and an empty row
        print(f"[{index:02d}/{total_files:02d}] Finish: {one_str}")
        print()


if __name__ == "__main__":
    one_time_pipesim("./db.txt", "../pipesim/")
