import os
import re
import time
import subprocess
import argparse

from utils import get_now_string, generate_avg_csv
from process_mgpusim import parse_time_output

def pipesim_virtual_time(input_file_path, main_path):
    # Read all strings from the input file and save them in a list
    with open(input_file_path, "r") as file:
        file_list = [line.strip() for line in file if line.strip()]

    # Prepare the output file
    timestring = get_now_string()
    results_dir = "./results"
    os.makedirs(results_dir, exist_ok=True)  
    records_file = f"{results_dir}/pipesim_records_virtual_time_{timestring}.csv"
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
        assert "ms" in output_lines[0] or "s" in output_lines[0]
        assert "ms" in output_lines[1] or "s" in output_lines[1]
        if "ms" in output_lines[0]:
            init_time = float(output_lines[0].split(":")[1].strip().replace("ms", "")) / 1000
        else:
            init_time = float(output_lines[0].split(":")[1].strip().replace("s", ""))

        if "ms" in output_lines[1]:
            run_time = float(output_lines[1].split(":")[1].strip().replace("ms", "")) / 1000
        else:
            run_time = float(output_lines[1].split(":")[1].strip().replace("s", ""))

        virtual_time = float(output_lines[2].split(":")[1].strip())

        # Change back to the original directory
        os.chdir(original_path)

        # Write the record to the file
        record = f"{job_name},{argparse_flag[1:] if argparse_flag[0] == '-' else argparse_flag},{params},{init_time},{run_time},{virtual_time}\n"
        with open(records_file, "a") as f:
            f.write(record)

        # Print finish message and an empty row
        print(f"[{index:02d}/{total_files:02d}] Finish: {one_str}")
        print()


def pipesim_real_time(input_file_path, main_path, suffix, repeat_time=3):
    timestring = get_now_string()
    results_dir = "./results"
    os.makedirs(results_dir, exist_ok=True)  
    # Read all strings from the input file and save them in a list
    with open(input_file_path, "r") as file:
        file_list = [line.strip() for line in file if line.strip()]

    # Prepare the output file
    records_file = f"{results_dir}/pipesim_records_real_time{f'_{suffix}' if suffix != '' else ''}_{timestring}.csv"
    if not os.path.exists(records_file):
        with open(records_file, "w") as f:
            f.write("job_name,argparse_flag,params,time_python,time_terminal_real,time_terminal_user,time_terminal_sys,init_time,run_time,virtual_time\n")

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



        # Run the go command
        # command = f"go run pipesim/main.go -database {one_str} -config=config.json"
        command = f"./pipesim/pipesim -database {one_str} -config=config.json"
        time_command = f"time {command}"
        print(f"[{index:02d}/{total_files:02d}] Command: {command}")
        print(f"[{index:02d}/{total_files:02d}] Time Command: {time_command}")

        for seed in range(repeat_time):
            os.chdir(main_path)
            start_time = time.time()
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, text=True)
            end_time = time.time()

            time_python = end_time - start_time

            # Parse the output
            output_lines = result.stdout.strip().split("\n")
            if len(output_lines) < 3:
                print(f"Unexpected output format: {result.stdout}")
                os.chdir(original_path)
                continue
            print(f"output_lines[0]: {output_lines[0]}\noutput_lines[1]: {output_lines[1]}")
            assert "ms" in output_lines[0] or "s" in output_lines[0]
            assert "ms" in output_lines[1] or "s" in output_lines[1]
            if "ms" in output_lines[0]:
                init_time = float(output_lines[0].split(":")[1].strip().replace("ms", "")) / 1000
            else:
                init_time = float(output_lines[0].split(":")[1].strip().replace("s", ""))

            if "ms" in output_lines[1]:
                run_time = float(output_lines[1].split(":")[1].strip().replace("ms", "")) / 1000
            else:
                run_time = float(output_lines[1].split(":")[1].strip().replace("s", ""))

            virtual_time = float(output_lines[2].split(":")[1].strip())

            result = subprocess.run(
                time_command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                executable="/bin/bash"  # Ensure Bash is used for the time command
            )

            time_terminal_real, time_terminal_user, time_terminal_sys = parse_time_output(result.stderr)

            # Write the record to the file
            record = f"{job_name},{argparse_flag[1:] if argparse_flag[0] == '-' else argparse_flag},{params},{time_python},{time_terminal_real},{time_terminal_user},{time_terminal_sys},{init_time},{run_time},{virtual_time}\n"
            print(record)
            os.chdir(original_path)
            with open(records_file, "a") as f:
                f.write(record)

        # Print finish message and an empty row

        print(f"[{index:02d}/{total_files:02d}] Finish: {one_str}")
        print()
    generate_avg_csv(records_file, ["job_name", "argparse_flag", "params"])



if __name__ == "__main__":
    # pipesim_virtual_time("./db.txt", "../pipesim/")
    parser = argparse.ArgumentParser()
    parser.add_argument('--suffix', type=str, default="", help='Suffix to be loaded')
    parser.add_argument('--repeat', type=int, default=3, help='Repeat times')
    args = parser.parse_args()

    pipesim_real_time("./db.txt", "../pipesim/", suffix=args.suffix, repeat_time=args.repeat)
