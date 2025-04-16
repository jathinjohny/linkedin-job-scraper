import pandas as pd
import os

def clean_and_merge_csv_files(input_folder, output_file, removed_rows_file):
    all_dataframes = []
    removed_rows = []

    # Iterate through all files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            file_path = os.path.join(input_folder, file_name)
            try:
                # Read the CSV file
                df = pd.read_csv(file_path)

                # Check if required columns exist
                if {'Job Title', 'Company Name', 'Location'}.issubset(df.columns):
                    # Identify rows where 'Job Title', 'Company Name', and 'Location' are all null
                    rows_to_remove = df[df[['Job Title', 'Company Name', 'Location']].isnull().all(axis=1)]

                    # Append removed rows to the list
                    removed_rows.append(rows_to_remove)

                    # Remove rows where 'Job Title', 'Company Name', and 'Location' are all null
                    df = df[~df[['Job Title', 'Company Name', 'Location']].isnull().all(axis=1)]

                    # Append the cleaned dataframe to the list
                    all_dataframes.append(df)
                    print(f"Processed file: {file_name}")
                else:
                    print(f"Skipped file (missing required columns): {file_name}")
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    # Merge all dataframes into one
    if all_dataframes:
        merged_df = pd.concat(all_dataframes, ignore_index=True)

        # Remove duplicate rows based on specific columns, ignoring rows with nulls in the subset
        merged_df = merged_df.drop_duplicates(
            subset=['Job Title', 'Company Name', 'Location', 'Post Date', 'Work Mode', 'Job Type'],
            keep='first'
        )

        # Save the merged dataframe to the output file
        merged_df.to_csv(output_file, index=False)
        print(f"Final merged data saved to: {output_file}")
    else:
        print("No valid data to merge.")

    # Merge all removed rows into one DataFrame and save to a separate file
    if removed_rows:
        removed_df = pd.concat(removed_rows, ignore_index=True)
        removed_df.to_csv(removed_rows_file, index=False)
        print(f"Removed rows saved to: {removed_rows_file}")
    else:
        print("No rows were removed.")

# Define input folder, output file, and removed rows file
input_folder = r"d:\DBS\PROGRAMMING FOR DATA ANALYSIS\project\daily linkedin data"
output_file = r"d:\DBS\PROGRAMMING FOR DATA ANALYSIS\project\final data\final_merged_data.csv"
removed_rows_file = r"d:\DBS\PROGRAMMING FOR DATA ANALYSIS\project\final data\removed_rows.csv"

# Run the function
clean_and_merge_csv_files(input_folder, output_file, removed_rows_file)