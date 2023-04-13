
import re
import pandas as pd



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
            list.append(None)

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

    neuro = ["Neuro", "neuro", "NS", "ns"]

    cardio = ["Cardio", "cardio", "Kardio", "myocytes", "HMZ"]

    list_of_patterns = [neuro, cardio]
    series_list = []
    for index, pattern in enumerate(list_of_patterns):
        pattern = '|'.join(pattern)
        series = df["Location"].str.contains(pattern)
        series = series.map({True: list_of_patterns[index][0], False: None})
        series_list.append(series)

    series_to_one = series_list[0].combine_first(series_list[1])

    for index in range(len(series_list) - 1):
        series_to_one = series_to_one.combine_first(series_list[index + 1])

    list = series_to_one.to_list()
    df_with_culture_type = pd.DataFrame(list, columns=["Culture type"])
    df = pd.concat([df, df_with_culture_type], axis=1)

    return df

def append_df_with_cells_kind(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Cell's kind" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_cells_kind : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Cell's kind".
        """

    rat = ["Rat neurons", "Rat cells", "Ratneuronen", "Rat", "rat"]
    hesc = ["hESC", "human embryonic stem cells", "hES", "human"]
    ipsc = ["iPSC", "induced pluripotent stem cells", "iPS", "induced"]
    chicken = ["Chicken", "chicken", "Hühn", "hühn"]

    list_of_patterns = [rat, hesc, ipsc, chicken]

    series_list = []
    for index, pattern in enumerate(list_of_patterns):
        pattern = '|'.join(pattern)
        series = df["Location"].str.contains(pattern)
        series = series.map({True: list_of_patterns[index][0], False: None})
        series_list.append(series)

    series_to_one = series_list[0].combine_first(series_list[1])

    for index in range(len(series_list) - 1):
        series_to_one = series_to_one.combine_first(series_list[index + 1])
    # print(series_to_one)

    list = series_to_one.to_list()
    df_with_cells_kind = pd.DataFrame(list, columns=["Cell's kind"])
    df = pd.concat([df, df_with_cells_kind], axis=1)

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

    #Searching for experiments with "Bicuculline" application
    bic = ["Bicuculline","bicuculline", "Bic", "bic"]

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

    list = series_to_one.to_list()
    df_with_drug_application = pd.DataFrame(list, columns=["Drug application"])
    df = pd.concat([df, df_with_drug_application], axis=1)
    return df

def append_df_with_drug_dose(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Drug dose" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_drug_dose : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Drug dose".
        """

    dose1 = ["10 microM", "10 muM", "10muM"]
    dose2 = ["5 microM", "5 muM", "5muM"]
    dose3 = ["2 microM", "2 muM", "2muM"]
    dose4 = ["1 microM", "1 muM", "1muM"]
    dose5 = ["0,5 microM", "0,5 muM", "05muM"]
    dose6 = ["0,1 microM", "0,1 muM", "01muM"]

    list_of_patterns = [dose1, dose2, dose3, dose4, dose5, dose6]
    series_list = []
    for index, pattern in enumerate(list_of_patterns):

        pattern = '|'.join(pattern)
        series = df["Location"].str.contains(pattern)
        series = series.map({True: list_of_patterns[index][0], False: None})
        series_list.append(series)

    series_to_one = series_list[0].combine_first(series_list[1])

    for index in range(len(series_list)-1):
        series_to_one = series_to_one.combine_first(series_list[index+1])

    list = series_to_one.to_list()
    df_with_drug_dose = pd.DataFrame(list, columns=["Drug dose"])
    df = pd.concat([df, df_with_drug_dose], axis=1)
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

    rad = ["Radiation", "radiation", "Irradiation", "irradiation", "aR", "a.R."]

    pattern_rad = '|'.join(rad)
    df["Radiation"] = df["Location"].str.contains(pattern_rad)
    df["Radiation"] = df["Radiation"].map({True: "Irradiated", False: None})

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

    biomems = ["BioMEMS", "BIOMEMS", "biomems", "Biomems"]
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
        df_with_performer : pd.DataFrame
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
    tkr = ["Tobias Kraus", "Tobias", "Kraus", "kraus"]
    mc = ["Manuel Ciba", "Ciba", "ciba"]
    nn = ["Nahid Nafez", "Nafez", "nafez"]
    os = ["Oliver Smolin", "Smolin", "smolin"]
    eaf = ["Enes Aydin Furkan", "Furkan", "furkan"]
    mj = ["Melanie Jungblut", "Jungblut"]
    il = ["Ismael Losano", "Losano"]
    nkr = ["Nico Kück", "Kück"]
    ah = ["Anja Heselide", "Heselide"]
    sg = ["Sebastian Gutsfeld", "Gutsfeld"]
    sh = ["Simone Hufgard", "Hufgard"]
    df = ["Dennis Flachs", "Flachs"]
    sho = ["Stefan Homes", "Homes"]
    ct = ["Christiane Thielemann"]
    ca = ["Sebastian Allig"]


    list_of_patterns = [ad, cn, jf, mm, ps, bk, tk, sk, pr, tkr, mc, nn, os, eaf, mj, il, nkr, ah, sg, sh, df, sho, ct, ca]
    #patterns = [ad, cn, jf, mm, ps, bk, tk, sk, pr, tkr, mc, nn, os, eaf, mj]



    series_list = []
    for index, pattern in enumerate(list_of_patterns):
        name = '|'.join(pattern)
        series = df["Location"].str.contains(name)
        series = series.map({True: list_of_patterns[index][0], False: None})
        series_list.append(series)

    """"#for case independent search (German, Upper/lower case)
    for pattern in list_of_patterns:
        for index in pattern:
            patterns_caseless = index.casefold()

    for index, pattern in enumerate(patterns_caseless):
        name = '|'.join(pattern)
        series = df["Location"].str.contains(name)
        series = series.map({True: patterns_caseless[index][0], False: None})
        series_list.append(series)"""

    series_to_one = series_list[0].combine_first(series_list[1])

    for index in range(len(series_list) - 1):
        series_to_one = series_to_one.combine_first(series_list[index + 1])
    # print(series_to_one)

    list = series_to_one.to_list()
    df_with_performer = pd.DataFrame(list, columns=["Performer"])
    df = pd.concat([df, df_with_performer], axis=1)

    return df

def append_df_with_size(df: pd.DataFrame) -> pd.DataFrame:
    import os
    list = []
    for index, row in df.iterrows():
        size = os.path.getsize(row["Location"])*(1/1024)*(1/1024)*(1/1024)
        #size in Gb
        list.append(size)

    df_with_size = pd.DataFrame(list, columns=["Size"])
    df = pd.concat([df, df_with_size], axis=1)

    return df

def copy_files_with_conditions(df, path):
    import shutil
    import os
    df = df[df["Drug application"] == 'Bicuculline']
    df = df[df["Recording system"] == "MEA"]
    df = df[df["Format"] == ".dat"]
    df = df[df["Drug dose"] == "10 microM"]
    #df = df[df["Size"] < 1.4]
    df = df[df["Size"] > 1.3]

    for row in df.iterrows():
        original_file_path = row[1]["Location"]
        file_name = os.path.basename(original_file_path)
        path_to_copy = os.path.join(path, file_name)
        new_file_path = os.path.normpath(path_to_copy)
        shutil.copyfile(original_file_path, new_file_path)
        csv_file_path = os.path.join(path, "info.csv")
        df.to_csv(csv_file_path)


