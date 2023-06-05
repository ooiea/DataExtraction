import re
import pandas as pd



def append_df_with_recording_sys(df: pd.DataFrame) -> pd.DataFrame:
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
            list.append("HDMEA")
        elif row == ".dat":
            list.append("MEA")
        else:
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

    cardio = ["Cardio", "cardio", "Kardio", "myocytes", "HMZ", "hmz"]

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
    hesc = ["Human embryonic stem cells", "hESC", "hES", "human"]
    ipsc = ["Induced pluripotent stem cells", "iPSC", "iPS", "induced"]
    chicken = ["Chicken embryo cardiomyocytes", "Chicken", "chicken", "Hühn", "hühn"]

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

def append_df_with_div(df: pd.DataFrame) -> pd.DataFrame:
    """
    Appends a column called "DIV" to a given DataFrame
    Parameters
    ----------
    df : pd.DataFrame
        Data Frame with information about the given Directory.
    Returns
    -------
    df_with_div : pd.DataFrame
        Returns a Pandas DataFrame with a new column "DIV".
    """

    div = []

    # Defining the regular expression pattern to match DIV or div in different formats
    pattern = re.compile(
        r'(\d+)[^\d]*\b(?:DIV|div)[^\d]*(\d+)?|\b(?:DIV|div)[^\d]*(\d+)\b|(\d+)[^\d]*\b(?:DIV|div)\b|(\d+)[^\d]*(?:DIV|div)[^\d]*\b')

    for location in df["Location"]:
        closest_num = None
        match = pattern.search(str(location))
        if match:
            # Finding the closest number to "DIV" or "div"
            groups = match.groups()
            num1 = next((group for group in groups if group is not None), None)
            num2 = next((group for group in groups[1:] if group is not None), None)
            if num1 and num2:
                num1_index = groups.index(num1)
                num2_index = groups.index(num2)
                closest_num = num2 if abs(match.start(num2_index) - match.start(num1_index)) < abs(
                    match.start(0) - match.end(0)) else num1
            elif num1:
                closest_num = num1
        div.append(int(closest_num) if closest_num is not None else None)

    df["DIV"] = div

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
    lev = ["Levetiracetam", "levetiracetam", "lev"]

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

    dose1 = ["10 µM", "10 microM", "10 muM", "-10muM"]
    dose2 = ["5 µM", "5 microM", "5 muM", "-5muM"]
    dose3 = ["2 µM", "2 microM", "2 muM", "-2muM"]
    dose4 = ["1 µM", "1 microM", "1 muM", "-1muM"]
    dose5 = ["0,5 µM", "0,5 microM", "0,5 muM", "-05muM"]
    dose6 = ["0,2 µM", "0,2 microM", "0,2 muM", "-02muM"]
    dose7 = ["0,1 µM", "0,1 microM", "0,1 muM", "-01muM"]

    list_of_patterns = [dose1, dose2, dose3, dose4, dose5, dose6, dose7]
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

    rad = ["Radiation", "radiation", "Irradiation", "irradiation", "aR", "a.R.", "Gy", "Strahlung", "Strahl", "strahl"]
    ionizing = ["Ionizing, X-Ray", "X-Ray", "X-ray", "Xray"]
    nonionizing1 = ["Non-ionizing, TETRA", "TETRA"]
    nonionizing2 = ["Non-ionizing, GSM", "Mobile", "mobile", "GSM"]

    list_of_patterns = [rad, ionizing, nonionizing1, nonionizing2]

    series_list = []
    for index, pattern in enumerate(list_of_patterns):
        patterns = '|'.join(pattern)
        series = df["Location"].str.contains(patterns)
        series = series.map({True: list_of_patterns[index][0], False: None})
        series_list.append(series)

    series_to_one = series_list[0].combine_first(series_list[1])

    for index in range(len(series_list) - 1):
        series_to_one = series_to_one.combine_first(series_list[index + 1])
    # print(series_to_one)

    list = series_to_one.to_list()
    df_with_radiation = pd.DataFrame(list, columns=["Radiation"])
    df = pd.concat([df, df_with_radiation], axis=1)

    return df

def append_df_with_rad_dose(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Radiation dose, Gy" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_rad_dose : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Radiation dose, Gy".
        """

    pattern = re.compile(r'(\d*\.?\d+)\s*(Gy)')
    rad_dose = []


    for index in df["Location"]:
        if isinstance(index, str):
            matches = pattern.findall(index)
            if matches:
                # Calculating the distance between "Gy" and each match
                distances = [abs(index.find("Gy") - index.find(m[1])) for m in matches]
                # Finding the index of the match with the smallest distance
                min_idx = distances.index(min(distances))
                # Extracting the number from the matching string and convert to float
                closest_num_dose = float(matches[min_idx][0])
                rad_dose.append(closest_num_dose)
            else:
                rad_dose.append(None)
        else:
            rad_dose.append(None)

    df["Radiation dose, Gy"] = rad_dose

    return df


def append_df_with_ar_time(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Time after radiation, h" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_ar_time : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Time after radiation, h".
        """
    import re

    ar_times = []

    # Define the regular expression pattern
    pattern = re.compile(r'(\d+)\s*[_ ]*[hH]\b')

    # Loop through the "Location" column and extract the time value in hours
    for location in df['Location']:
        match = pattern.search(str(location))
        if match:
            ar_time = int(match.group(1))
        else:
            ar_time = None
        ar_times.append(ar_time)

    df['Time after radiation, h'] = ar_times

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
    japan = ["Japan", "japan", "Tokyo", "tokyo", "Tokio", "tokio"]
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

    list = series_to_one.to_list()
    df_with_labor = pd.DataFrame(list, columns=["Labor"])
    df = pd.concat([df, df_with_labor], axis=1)

    performer_names = [
        "Andreas Daus", "Christoph Nick", "Margot Mayer", "Berit Körbitzer", "Tim Köhler",
        "Steffen Künzinger", "Pascal Rüdel", "Tobias Kraus", "Nahid Nafez", "Ismael Losano",
        "Nico Kück", "Sebastian Gutsfeld", "Simone Hufgard", "Dennis Flachs",
        "Christiane Thielemann", "Sebastian Allig", "Hitesh Kanoia", "Karin Schiling",
        "Wenus Nafez", "Diana Khropost"
    ]


    mask = df["Performer"].isin(performer_names)
    series_to_one = series_to_one.where(series_to_one.isnull() | mask, "BioMEMS")

    df["Labor"] = series_to_one.combine_first(df["Labor"]).combine_first(df["Labor"].shift())

    return df

def append_df_with_date_and_time(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a columns called "Date" and "Time" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_date_and_time : pd.DataFrame
            Returns a Pandas DataFrame with a new columns "Date" and "Time".
        """

    import re

    pattern = r'Messung(\d{1,2}\.\d{1,2}\.\d{4})_(\d{2}\-\d{2}\-\d{2})'

    df["Date"] = ""
    df["Time"] = ""

    for index, row in df.iterrows():
        string = row["Location"]
        match = re.search(pattern, string)
        if match:
            date = match.group(1)
            time = match.group(2)
            df.at[index, "Date"] = date
            df.at[index, "Time"] = time

    return df


def append_df_with_stimulation(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Stimulation" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_stimulation : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Stimulation".
        """

    stim = ["Stimulation", "Stim", "stim", "Slice Stim"]

    pattern_stim = '|'.join(stim)
    df["Stimulation"] = df["Location"].str.contains(pattern_stim)
    df["Stimulation"] = df["Stimulation"].map({True: "Slice stimulation", False: None})

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
    jf = ["Johannes Frieß", "Frieß", "frieß"] #b and GSI and Darmstadt
    mm = ["Margot Mayer", "Mayer", "mayer"]
    ps = ["Philipp Steigerwald", "steigerwald"] #?
    bk = ["Berit Körbitzer", "Körbitzer", "körbitzer"]
    tk = ["Tim Köhler", "Köhler", "köhler"]
    sk = ["Steffen Künzinger", "Künzinger", "künzinger"]
    pr = ["Pascal Rüdel", "Pascal", "Rüdel"]
    tkr = ["Tobias Kraus", "Tobias", "Kraus", "kraus"]
    mc = ["Manuel Ciba", "Ciba", "ciba"] #b and Tokio and Fr
    nn = ["Nahid Nafez"]
    os = ["Oliver Smolin", "Smolin", "smolin"] #b and GSI
    eaf = ["Enes Aydin Furkan", "Furkan", "furkan"] # b and Wurzburg
    mj = ["Melanie Jungblut", "Jungblut", "jungblut"] # ?
    il = ["Ismael Losano", "Losano", "losano"]
    nkr = ["Nico Kück", "Kück", "kück"]
    ah = ["Anja Heselich", "Heselich", "heselich"] #b and GSI and Darmstadt
    sg = ["Sebastian Gutsfeld", "Gutsfeld", "gutsfeld"]
    sh = ["Simone Hufgard", "Hufgard", "hufgard"]
    dfl = ["Dennis Flachs", "Flachs", "flachs"]
    sho = ["Stefan Homes", "Homes", "homes"] #?
    ct = ["Christiane Thielemann", "Thielemann", "thielemann"]
    ca = ["Sebastian Allig", "Allig", "allig"]
    hka = ["Hitesh Kanoia", "Hitesh", "Kanoia", "kanoia"]
    ksc = ["Karin Schiling", "Karin", "Schiling", "schiling"]
    wn = ["Wenus Nafez"]
    dkh = ["Diana Khropost"]



    list_of_patterns = [ad, cn, jf, mm, ps, bk, tk, sk, pr, tkr, mc, nn, os, eaf, mj, il, nkr, ah, sg, sh, dfl, sho,
                        ct, ca, hka, ksc, wn, dkh]

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

def append_cleaning_function(df: pd.DataFrame) -> pd.DataFrame:
    """
        Removes trash files from a given DataFrame.
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df : pd.DataFrame
            Returns a Pandas DataFrame without trash files.
        """

    trash = ["Trash", "trash", "Error", "error", "Fehler", "fehler", "müll",
                        "LFP", "GlukZ", "DrCell", "Drcell", "drcell", "software"]
    df = df[~df.Location.str.contains('|'.join(trash))]
    df = df.reset_index(drop=True)

    #If size = 0
    for index, row in df.iterrows():
        if row["Size"] == 0:
            df = df.drop(index=index)
    df = df.reset_index(drop=True)

    #If recording system was not identified
    for index, row in df.iterrows():
        if row["Recording system"] is None:
            df = df.drop(index=index)
    df = df.reset_index(drop=True)

    return df

def append_df_with_control(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Control" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_culture_type : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Control".
        """

    control = ["Control", "Kontrol"]
    sham = ["Sham", "sham"]

    list_of_patterns = [control, sham]
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
    df_with_control = pd.DataFrame(list, columns=["Control"])
    df = pd.concat([df, df_with_control], axis=1)

    return df

def append_df_with_pitch(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Pitch, µm" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_pitch : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Pitch, µm".
        """

    pattern = re.compile(r'(\d*\.?\d+)\s*(um)')
    pitch = []


    for index in df["Location"]:
        if isinstance(index, str):
            matches = pattern.findall(index)
            if matches:
                # Calculating the distance between "Gy" and each match
                distances = [abs(index.find("um") - index.find(m[1])) for m in matches]
                # Finding the index of the match with the smallest distance
                min_idx = distances.index(min(distances))
                # Extracting the number from the matching string and convert to float
                closest_num_pitch = float(matches[min_idx][0])
                pitch.append(closest_num_pitch)
            else:
                pitch.append(None)
        else:
            pitch.append(None)

    df["Pitch, µm"] = pitch

    return df

def append_df_with_sampling_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Appends a column called "Sampling rate" to a given DataFrame
    Parameters
    ----------
    df : pd.DataFrame
        Data Frame with information about the given Directory.
    Returns
    -------
    df_with_sampling_rate : pd.DataFrame
        Returns a Pandas DataFrame with a new column "Sampling rate".
    """

    rate = []

    # Defining the regular expression pattern to match kHz, kH or Hz in different formats
    pattern = re.compile(
        r'(\d+)[^\d]*\b(?:kH|kHz|Hz)[^\d]*(\d+)?|\b(?:kH|kHz|Hz)[^\d]*(\d+)\b|(\d+)[^\d]*\b(?:kH|kHz|Hz)\b|(\d+)[^\d]*(?:kH|kHz|Hz)[^\d]*\b')

    for location in df["Location"]:
        closest_num = None
        match = pattern.search(str(location))
        if match:
            # Finding the closest number to kHz, kH or Hz
            groups = match.groups()
            num1 = next((group for group in groups if group is not None), None)
            num2 = next((group for group in groups[1:] if group is not None), None)
            if num1 and num2:
                num1_index = groups.index(num1)
                num2_index = groups.index(num2)
                closest_num = num2 if abs(match.start(num2_index) - match.start(num1_index)) < abs(
                    match.start(0) - match.end(0)) else num1
            elif num1:
                closest_num = num1
        rate.append(int(closest_num) if closest_num is not None else None)

    df["Sampling rate"] = rate

    return df

def append_df_with_electrode(df: pd.DataFrame) -> pd.DataFrame:
    """
    Appends a column called "Electrode" to a given DataFrame
    Parameters
    ----------
    df : pd.DataFrame
        Data Frame with information about the given Directory.
    Returns
    -------
    df_with_electrode : pd.DataFrame
        Returns a Pandas DataFrame with a new column "Electrode".
    """

    electrode = []

    pattern = re.compile(
        r'(\d+)[^\d]*\b(?:Electrode|electrode)[^\d]*(\d+)?|\b(?:Electrode|electrode)[^\d]*(\d+)\b|(\d+)[^\d]*\b(?:Electrode|electrode)\b|(\d+)[^\d]*(?:Electrode|electrode)[^\d]*\b')

    for location in df["Location"]:
        closest_num = None
        match = pattern.search(str(location))
        if match:
            groups = match.groups()
            num1 = next((group for group in groups if group is not None), None)
            num2 = next((group for group in groups[1:] if group is not None), None)
            if num1 and num2:
                num1_index = groups.index(num1)
                num2_index = groups.index(num2)
                closest_num = num2 if abs(match.start(num2_index) - match.start(num1_index)) < abs(
                    match.start(0) - match.end(0)) else num1
            elif num1:
                closest_num = num1
        electrode.append(int(closest_num) if closest_num is not None else None)

    df["Electrode"] = electrode

    return df



def copy_files_with_conditions(df, path):
    import shutil
    import os
    df = df[df["Drug application"] == 'Bicuculline']
    df = df[df["Recording system"] == "MEA"]
    df = df[df["Format"] == ".dat"]
    #df = df[df["Drug dose"] == "10 microM"]
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
