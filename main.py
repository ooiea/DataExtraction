import pandas as pd
import os
import time

st = time.time()


def get_list_of_files(path, file_type):
    """
    Generates a list with all file paths from a given path.

    Parameters:
    ----------
    path : str
        Either a path to a single file or a directory path.
    file_type : str or list of str
        The extension(s) of the file(s) to retrieve. Can be a single extension or a list of extensions.

    Returns:
    -------
    list_of_files : list of str
        A list of file paths in the chosen directory and its subdirectories.
    """
    all_files = []

    if os.path.isdir(path):
        extension_list = []
        if isinstance(file_type, str):
            extension_list.append(file_type)
        elif isinstance(file_type, list):
            extension_list = file_type

        list_of_files = os.listdir(path)

        for entry in list_of_files:
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                all_files.extend(get_list_of_files(full_path, extension_list))
            else:
                name, extension = os.path.splitext(full_path)
                if extension_list is None or any(extension in s for s in extension_list):
                    all_files.append(full_path)
    else:
        all_files.append(path)

    return all_files


def create_pandas_df(list_of_files):
    """
    Generates a Pandas DataFrame from a list of file paths.

    Parameters:
    ----------
    list_of_files : list of str
        A list of file paths to be included in the DataFrame.

    Returns:
    -------
    df : pandas DataFrame
        A DataFrame containing the file paths and their corresponding formats.
    """

    # Extract the file format from each file path and create a DataFrame
    csv_data_frame = pd.DataFrame(data=list_of_files, columns=["Location"])
    extension_series = csv_data_frame["Location"].apply(func=get_extension)
    extension_df = extension_series.to_frame(name="Format")
    df = pd.concat([csv_data_frame, extension_df], axis=1)

    return df

def get_extension(string):
    """
    Extracts and returns the file extension from a given string.

    Parameters:
    ----------
    string : str
        The input string, typically a file path, from which the extension will be extracted.

    Returns:
    -------
    extension : str
        The extracted file extension (including the dot), or an empty string if not found.
    """
    return os.path.splitext(string)[1]


def get_all_extensions_in_directory(list_of_files):
    """
    Generates a list of all file formats found in a given list of file paths.

    Parameters:
    ----------
    list_of_files : list of str
        A list of file paths from which to extract formats.

    Returns:
    -------
    list(extensions) : list of str
        A list containing all the unique file formats present in the list of file paths,
        extracted by splitting the string after the dot.
    """
    extensions = set(os.path.splitext(file)[1] for file in list_of_files)
    return list(extensions)


if __name__ == '__main__':

    path = "C:/Users\Diana\Desktop\Studium\Master_project\Data_from_W8"

    norm_path = os.path.normpath(path)
    list_of_files = get_list_of_files(norm_path, None)
    #print(list_of_files)
    #print(f"Total Number of files {len(list_of_files)}:")
    #all_extensions = get_all_extensions_in_directory(list_of_files)
    #print(f"All extensions in Working Directory: {all_extensions}")
    list_of_files = get_list_of_files(norm_path, [".brw", ".dat"])
    print(f"Number of object .brw and .dat: {len(list_of_files)}")


    # Write into .csv
    csv_data_frame = create_pandas_df(list_of_files)
    csv_path = "C:/Users/Diana/Info_extraction/list_of_files.csv"


    from append_functions import append_df_with_size
    csv_data_frame = append_df_with_size(csv_data_frame)

    from append_functions import append_df_with_date_and_time
    csv_data_frame = append_df_with_date_and_time(csv_data_frame)

    from append_functions import append_df_with_recording_sys
    csv_data_frame = append_df_with_recording_sys(csv_data_frame)

    from append_functions import append_df_with_pitch
    csv_data_frame = append_df_with_pitch(csv_data_frame)

    from append_functions import append_df_with_sampling_rate
    csv_data_frame = append_df_with_sampling_rate(csv_data_frame)

    from append_functions import append_df_with_electrode
    csv_data_frame = append_df_with_electrode(csv_data_frame)

    from append_functions import append_df_with_culture_type
    csv_data_frame = append_df_with_culture_type(csv_data_frame)

    from append_functions import append_df_with_cells_kind
    csv_data_frame = append_df_with_cells_kind(csv_data_frame)

    from append_functions import append_df_with_div_dap
    csv_data_frame = append_df_with_div_dap(csv_data_frame)

    from append_functions import append_df_with_performer
    csv_data_frame = append_df_with_performer(csv_data_frame)

    from append_functions import append_df_with_lab
    csv_data_frame = append_df_with_lab(csv_data_frame)

    from append_functions import append_df_with_drug_application
    csv_data_frame = append_df_with_drug_application(csv_data_frame)

    from append_functions import append_df_with_drug_dose
    csv_data_frame = append_df_with_drug_dose(csv_data_frame)

    from append_functions import append_df_with_radiation
    csv_data_frame = append_df_with_radiation(csv_data_frame)

    from append_functions import append_df_with_rad_dose
    csv_data_frame = append_df_with_rad_dose(csv_data_frame)

    from append_functions import append_df_with_br_or_ar_time
    csv_data_frame = append_df_with_br_or_ar_time(csv_data_frame)

    from append_functions import append_df_with_nano
    csv_data_frame = append_df_with_nano(csv_data_frame)

    from append_functions import append_df_with_laser
    csv_data_frame = append_df_with_laser(csv_data_frame)

    from append_functions import append_df_with_timeframe
    csv_data_frame = append_df_with_timeframe(csv_data_frame)

    from append_functions import append_df_with_stimulation
    csv_data_frame = append_df_with_stimulation(csv_data_frame)

    from append_functions import append_df_with_control
    csv_data_frame = append_df_with_control(csv_data_frame)

    from append_functions import append_cleaning_function

    csv_data_frame = append_cleaning_function(csv_data_frame)

    csv_data_frame.to_csv(csv_path)
    et = time.time()
    time = et - st
    final_time = time / 60
    print("Execution time:", final_time, "minutes")
