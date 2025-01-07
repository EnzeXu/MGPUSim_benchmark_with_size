import os
import subprocess
import re
import shutil
import csv


def one_time_process(setting_list, main_path):
    traces_dir = "./traces"
    os.makedirs(traces_dir, exist_ok=True)  # Create the traces directory if it doesn't exist

    for idx, sub_list in enumerate(setting_list):
        # Extract job details
        job_name, argparse_flag, params = sub_list
        print(f"[{idx + 1:02d}/{len(setting_list):02d}] Start: {sub_list}")

        # Step 1: Run the command
        original_path = os.getcwd()
        job_path = os.path.join(main_path, job_name)
        os.chdir(job_path)
        # command = f"{job_path}/{job_name} {argparse_flag}={params} -timing -report-all -trace-vis"
        command = f"./{job_name} {argparse_flag}={params} -timing -report-all -trace-vis"
        print(f"[{idx + 1:02d}/{len(setting_list):02d}] Command: {command}")
        subprocess.run(command, shell=True, check=True)

        # Step 2: Detect akita_trace_xxxxxxxx.sqlite3
        os.chdir(original_path)
        trace_file_pattern = re.compile(r"akita_trace_[a-zA-Z0-9]+\.sqlite3")
        trace_file = None
        for file in os.listdir(job_path):
            # print(f"file: {file}")
            if trace_file_pattern.match(file):
                trace_file = file
                break
        if not trace_file:
            raise FileNotFoundError(f"No trace file found in {job_path}")

        # Step 3: Rename and copy the trace file
        new_trace_name = f"{job_name}_{argparse_flag.replace('-', '')}_{params}.sqlite3"
        old_trace_path = os.path.join(job_path, trace_file)
        new_trace_path = os.path.join(job_path, new_trace_name)
        if os.path.exists(new_trace_path):
            os.remove(new_trace_path)  # Remove the existing file if it exists
        os.rename(old_trace_path, new_trace_path)
        destination_file_path = os.path.join(traces_dir, os.path.basename(new_trace_path))
        if os.path.exists(destination_file_path):
            os.remove(destination_file_path)
        shutil.copy(new_trace_path, traces_dir)
        trace_size = os.path.getsize(new_trace_path) / (1024 * 1024)  # Convert to MB

        # Step 4: Process metrics.csv and append to records.csv
        metrics_csv_path = os.path.join(job_path, "metrics.csv")
        with open(metrics_csv_path, "r") as metrics_file:
            metrics_lines = metrics_file.readlines()
        assert "kernel_time" in metrics_lines[1]
        assert "total_time" in metrics_lines[2]
        kernel_time = float(metrics_lines[1].split(",")[-1].strip())
        total_time = float(metrics_lines[2].split(",")[-1].strip())

        records_csv_path = "./records.csv"  # os.path.join(traces_dir, "records.csv")
        record_row = [job_name, argparse_flag, params, trace_size, kernel_time, total_time]
        file_exists = os.path.isfile(records_csv_path)

        with open(records_csv_path, "a", newline="") as records_file:
            writer = csv.writer(records_file)
            if not file_exists:
                writer.writerow(["job_name", "argparse_flag", "params", "trace_size", "kernel_time", "total_time"])
            writer.writerow(record_row)

        # Step 5: Print completion message
        print(f"[{idx + 1:02d}/{len(setting_list):02d}] Done: {sub_list}\n")


if __name__ == "__main__":
    main_path = "../mgpusim/samples"

    # setting_list = [["relu", "-length", 2 ** i] for i in range(10, 20)]
    # one_time_process(setting_list, main_path)
    # setting_list = [["fir", "-length", 2 ** i] for i in range(7, 17)]
    # one_time_process(setting_list, main_path)
    # setting_list = [["matrixtranspose", "-width", 2 ** i] for i in range(2, 10)]
    # one_time_process(setting_list, main_path)
    # setting_list = [["spmv", "-dim", 2 ** i] for i in range(4, 12)]
    # one_time_process(setting_list, main_path)
    # setting_list = [["kmeans", "-points", 2 ** i] for i in range(3, 11)]
    # one_time_process(setting_list, main_path)
    # setting_list = [["matrixmultiplication", "-x", 2 ** i] for i in range(3, 13)]
    # one_time_process(setting_list, main_path)
    # setting_list = [["bfs", "-node", 2 ** i] for i in range(5, 15)]
    # one_time_process(setting_list, main_path)
    # setting_list = [["pagerank", "-node", 2 ** i] for i in range(1, 9)]
    # one_time_process(setting_list, main_path)
    setting_list = [["pagerank", "-iterations", 2 ** i] for i in range(0, 10)]
    one_time_process(setting_list, main_path)
