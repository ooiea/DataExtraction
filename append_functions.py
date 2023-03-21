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

    #Searching for experiments with "Carbamazepine"
    carba = ["Carbamazepine", "carbamazepine", "carba", "Carba"]

    # Searching for experiments with "LSD"
    lsd = ["LSD", "lsd"]

    # Searching for experiments with "Levetiracetam"
    lev = ["levetiracetam", "Levetiracetam", "lev"]

    # Searching for experiments with "Cisplatin"
    cisplatin = ["Cisplatin", "cisplatin"]

    list_of_patterns = [bic, carba, lsd, lev, cisplatin]
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


    list = series_to_one.to_list()
    df_with_drug_application = pd.DataFrame(list, columns=["Drug application"])
    df = pd.concat([df, df_with_drug_application], axis=1)
    return df

def append_df_with_radiation(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Radiation" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_radiation : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Radiation".
        """

    #Searching for experiments from biomems labor
    biomems = ["BioMEMS", "BIOMEMS", "biomems", "Biomems"]
    #pattern_biomems = '|'.join(biomems)
    #df["Labor"] = df["Location"].str.contains(pattern_biomems)
    #df["Labor"] = df["Labor"].map({True: "BioMEMS", False: "Not identified"})

    after = ["Radiation", "radiation", "Irradiation", "irradiation", "aR", "a.R."]
    before = ["Before radiation"]

    list_of_patterns = [before, after]
    series_list = []
    for index, pattern in enumerate(list_of_patterns):
        pattern = '|'.join(pattern)
        series = df["Location"].str.contains(pattern)
        series = series.map({True: list_of_patterns[index][0], False: None})
        series_list.append(series)

    series_to_one = series_list[0].combine_first(series_list[1])

    for index in range(len(series_list) - 1):
        series_to_one = series_to_one.combine_first(series_list[index + 1])
    #print(series_to_one)

    list = series_to_one.to_list()
    df_with_radiation = pd.DataFrame(list, columns=["Radiation"])
    df = pd.concat([df, df_with_radiation], axis=1)
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
    #pattern_biomems = '|'.join(biomems)
    #df["Labor"] = df["Location"].str.contains(pattern_biomems)
    #df["Labor"] = df["Labor"].map({True: "BioMEMS", False: "Not identified"})

    japan = ["Tokyo", "tokyo", "Tokio", "tokio", "Japan", "japan"]

    gsi = ["GSI", "gsi"]

    france = ["France", "france", "French", "french"]

    list_of_patterns = [biomems, japan, gsi, france]
    series_list = []
    for index, pattern in enumerate(list_of_patterns):
        pattern = '|'.join(pattern)
        series = df["Location"].str.contains(pattern)
        series = series.map({True: list_of_patterns[index][0], False: None})
        series_list.append(series)

    series_to_one = series_list[0].combine_first(series_list[1])

    for index in range(len(series_list) - 1):
        series_to_one = series_to_one.combine_first(series_list[index + 1])
    #print(series_to_one)

    list = series_to_one.to_list()
    df_with_labor = pd.DataFrame(list, columns=["Labor"])
    df = pd.concat([df, df_with_labor], axis=1)
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


    ad = ["Andreas Daus", "Daus", "daus"]
    cn = ["Christoph Nick", "Nick", "nick"]
    jf = ["Johannes Frieß", "Frieß", "frieß"]
    mm = ["Margot Mayer", "Mayer", "mayer"]
    ps = ["Philipp Steigerwald", "steigerwald"]
    bk = ["Berit Körbitzer", "Körbitzer", "körbitzer"]
    tk = ["Tim Köhler", "Köhler", "köhler"]
    sk = ["Steffen Künzinger", "Künziger", "künziger"]
    pr = ["Pascal Rüde", "Rüde", "rüde"]
    tkr = ["Tobias Kraus", "Kraus", "kraus"]
    mc = ["Manuel Ciba", "Ciba", "ciba"]
    nn = ["Nahid Nafez", "Nafez", "nafez"]
    os =["Oliver Smolin", "Smolin", "smolin"]
    eaf = ["Enes Aydin Furkan", "Furkan", "furkan"]
    mj = ["Melanie Jungblut", "Jungblut"]

    list_of_patterns = [ad, cn, jf, mm, ps, bk, tk, sk, pr, tkr, mc, nn, os, eaf, mj]
    series_list = []
    for index, pattern in enumerate(list_of_patterns):
        pattern = '|'.join(pattern)
        series = df["Location"].str.contains(pattern)
        series = series.map({True: list_of_patterns[index][0], False: None})
        series_list.append(series)

    series_to_one = series_list[0].combine_first(series_list[1])

    for index in range(len(series_list) - 1):
        series_to_one = series_to_one.combine_first(series_list[index + 1])
    #print(series_to_one)

    list = series_to_one.to_list()
    df_with_performer = pd.DataFrame(list, columns=["Performer"])
    df = pd.concat([df, df_with_performer], axis=1)

    return df


def copy_files_with_conditions(df, path):
    import shutil
    import os
    df = df[df["Drug application"] == 'Bicuculline']
    df = df[df["Recording system"] == "MEA"]
    df = df[df["Format"] == ".dat"]
    for row in df.iterrows():
        original_file_path = row[1]["Location"]
        file_name = os.path.basename(original_file_path)
        path_to_copy = os.path.join(path, file_name)
        new_file_path = os.path.normpath(path_to_copy)
        shutil.copyfile(original_file_path, new_file_path)
        csv_file_path = os.path.join(path, "info.csv")
        df.to_csv(csv_file_path)


