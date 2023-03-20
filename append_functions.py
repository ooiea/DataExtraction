import pandas as pd

# Split all the directory names
#from re import split
#parameters = list_of_files.split("\\")

def append_recording_system_to_df(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Recording System" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_recording_system : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Recording System".
        """

    #rec_sys_list = ["HDMEA", "MEA", "None"]

    list = []
    for index, row in df["Format"].items():
        if row == ".brw":
            #print("HDMEA")
            list.append("HDMEA")
        elif row == ".dat":
            #print("MEA")
            list.append("MEA")
        else:
            #print(None)
            list.append("None")

    df_with_recording_system = pd.DataFrame(list, columns=["Recording system"])
    df = pd.concat([df, df_with_recording_system], axis=1)

    return df


def append_df_with_culture_type(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Culture type" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_culture_type : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Culture type".
        """

    list_neuro = ["Neuro", "neuro", "NS", "ns"]

    pattern_neuro = '|'.join(list_neuro)
    df["Culture type"] = df["Location"].str.contains(pattern_neuro)
    df["Culture type"] = df["Culture type"].map({True:"Neuro", False: "Not identified"})

    #list_cardio = ["Cardio", "cardio"]
    #pattern_cardio = '|'.join(list_cardio)
    #cardio = df['Location'].str.contains(pattern_cardio)
    #df['Culture type'] = cardio.replace(to_replace=(True, False), value=('Cardio', None))
    #df = pd.concat([df, df_with_culture_type], axis=1)

    return df


def append_df_with_drug_application(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Drug application" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_drug_application : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Drug application".
        """

    #Searching for experiments with "Bicucullin" application
    bic = ["Bicuculline","bicuculline", "Bic", "bic"]
    #pattern_bic = '|'.join(bic)
    #df["Drug application"] = df["Location"].str.contains(pattern_bic)
    #df["Drug application"] = df["Drug application"].map({True: "Bicucullin", False: None})

    #Searching for experiments with "PEI"
    pei = ["PEI"]

    # Searching for experiments with "LSD"
    lsd = ["LSD", "lsd"]

    list_of_patterns = [bic, pei, lsd]
    series_list = []
    for index, pattern in enumerate(list_of_patterns):

        pattern = '|'.join(pattern)
        series = df["Location"].str.contains(pattern)
        series = series.map({True: list_of_patterns[index][0], False: None})
        series_list.append(series)

    series_to_one = series_list[0].combine_first(series_list[1])

    for index in range(len(series_list)-1):
        series_to_one = series_to_one.combine_first(series_list[index+1])
    #print(series_to_one)

    return df


def append_df_with_labor(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Labor" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_drugs_application : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Labor".
        """

    #Searching for experiments from biomems labor
    biomems = ["BioMEMS", "BIOMEMS", "biomems", "Biomems"]
    pattern_biomems = '|'.join(biomems)
    df["Labor"] = df["Location"].str.contains(pattern_biomems)
    df["Labor"] = df["Labor"].map({True: "BioMEMS", False: "Not identified"})

    return df


def append_df_with_performer(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Performer" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_experiment : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Performer".
        """
    df_with_performer = ["Philipp Steigerwald", "Not identified"]

    return df_with_performer
