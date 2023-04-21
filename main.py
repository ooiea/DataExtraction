import pandas as pd


def getListOfFiles(dirName, file_extension):
    import os
    extension_list = []
    if isinstance(file_extension, str):
        extension_list.append(file_extension)
    if isinstance(file_extension, list):
        extension_list = file_extension
    if file_extension is None:
        extension_list = None
    # create a list of files and subdirectories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath, extension_list)
        else:
            name, extension = os.path.splitext(fullPath)
            if extension_list is None:
                allFiles.append(fullPath)
            else:
                if any(extension in s for s in extension_list):
                    # if extension == file_extension:
                    allFiles.append(fullPath)

    return allFiles


def get_list_of_files(path, file_type):
    """
        Generates a list with all file path from a given path.
        Parameters
        ----------
        path : string
            Either a path from a single file or a path of a directory.
        file_type : string, list of string
            The extension of the file type which should be taken into account.
            Can be one or more than one extension.
        Returns
        -------
        list_of_files : list of string
            Returns the path of files in a chosen directories.
        """

    import os
    all_files = []
    # check if path is a file or directory
    if os.path.isdir(path):
        all_files = getListOfFiles(path, file_type)
    else:
        all_files.append(path)
    return all_files


def create_pandas_df(list_of_files):
    """
        Generates a list with all file path from a given path.
        Parameters
        ----------
        path : string
            Either a path from a single file or a path of a directory.
        file_type : string, list of string
            The extension of the file type which should be taken into account.
            Can be one or more than one extension.
        Returns
        -------
        list_of_files : list of string
            Returns the path of files in a chosen directories.
        """

    # Extract column "Format" from "Location" column
    import pandas as pd
    csv_data_frame = pd.DataFrame(data=list_of_files, index=None, columns=["Location"])
    extension_series = csv_data_frame["Location"].apply(func=get_extension)
    extension_df = extension_series.to_frame(name="Format")
    df = pd.concat([csv_data_frame, extension_df], axis=1)
    return df

def get_extension(string):
    import os
    return os.path.splitext(string)[1]


# Find all the formats in directory by splitting string after the dot
def get_all_extensions_in_directory(file_list):
    """
        Generates a list with all file formats from a given path.
        Parameters
        ----------
        path : string
            String with extensions from a path of a directory.
        file_type : string
            Can be one or more than one extension.
        Returns
        -------
        extension_list : string
            Returns all the formats in directory by splitting string after the dot.
        """
    import os
    extension_list = []
    for i in file_list:
        extensions = os.path.splitext(i)[1]
        extension_list.append(extensions)

    list_of_extensions = list(set(extension_list))
    return list_of_extensions


if __name__ == '__main__':
    import os
    import pandas as pd

    path = "C:/Users\Diana\Desktop\Studium\Master_project\Data_from_W8"

    norm_path = os.path.normpath(path)
    list_of_files = get_list_of_files(norm_path, None)
    #print(list_of_files)
    print(f"Total Number of files {len(list_of_files)}:")
    all_extensions = get_all_extensions_in_directory(list_of_files)
    print(f"All extensions in Working Directory: {all_extensions}")
    list_of_files = get_list_of_files(norm_path, [".brw", ".dat"])
    print(f"Number of object .brw and .dat: {len(list_of_files)}")



    # Write into .csv
    csv_data_frame = create_pandas_df(list_of_files)
    csv_path = "C:/Users/Diana/Info_extraction/list_of_files.csv"


    from append_functions import append_df_with_size
    csv_data_frame = append_df_with_size(csv_data_frame)

    from append_functions import append_recording_system_to_df
    csv_data_frame = append_recording_system_to_df(csv_data_frame)

    from append_functions import append_df_with_culture_type
    csv_data_frame = append_df_with_culture_type(csv_data_frame)

    from append_functions import append_df_with_cells_kind
    csv_data_frame = append_df_with_cells_kind(csv_data_frame)

    from append_functions import append_df_with_labor
    csv_data_frame = append_df_with_labor(csv_data_frame)

    from append_functions import append_df_with_performer
    csv_data_frame = append_df_with_performer(csv_data_frame)

    from append_functions import append_df_with_drug_application
    csv_data_frame = append_df_with_drug_application(csv_data_frame)

    from append_functions import append_df_with_radiation
    csv_data_frame = append_df_with_radiation(csv_data_frame)

    from append_functions import append_df_with_stimulation
    csv_data_frame = append_df_with_stimulation(csv_data_frame)

    from append_functions import append_cleaning_function
    csv_data_frame = append_cleaning_function(csv_data_frame)

    from append_functions import copy_files_with_conditions
    copy_files_with_conditions(csv_data_frame, "C:/Users/Diana/Info_extraction/copy_test")


    #print(csv_data_frame)
    #norm_csv_path = os.path.normpath(csv_path)
    csv_data_frame.to_csv(csv_path)
