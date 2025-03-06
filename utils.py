import pytz
import pandas as pd
import datetime


def get_now_string(time_string="%Y%m%d_%H%M%S_%f"):
    # return datetime.datetime.now().strftime(time_string)
    est = pytz.timezone('America/New_York')

    # Get the current time in UTC and convert it to EST
    utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    est_now = utc_now.astimezone(est)

    # Return the time in the desired format
    return est_now.strftime(time_string)



def generate_avg_csv(csv_file_path, group_target_list):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Group by the columns in group_target_list and calculate the mean for the rest
    group_by_cols = group_target_list
    rest_cols = [col for col in df.columns if col not in group_by_cols]
    
    # Group by the specified keys and calculate the average for the other columns
    df_avg = df.groupby(group_by_cols, as_index=False)[rest_cols].mean()
    
    # Save the result to a new CSV file
    avg_csv_file_path = csv_file_path.replace('.csv', '_avg.csv')
    df_avg.to_csv(avg_csv_file_path, index=False)

    print(f"Saved averaged CSV to: {avg_csv_file_path}")


if __name__ == "__main__":
    generate_avg_csv("results/mgpusim_records_time_only_20250306_160656_843574.csv", ["job_name", "argparse_flag", "params"])