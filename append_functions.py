
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

    rec_sys_dict = {".brw": "HDMEA", ".dat": "MEA", "": None}
    df_with_recording_system = pd.DataFrame(df["Format"].map(rec_sys_dict).values, columns=["Recording system"])
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

    neuro = ["Neuro", "neuro", "NS"]
    cardio = ["Cardio", "cardio", "Kardio", "myocytes", "HMZ", "hmz"]

    list_of_patterns = [neuro, cardio]
    series_list = []
    for index, pattern in enumerate(list_of_patterns):
        patterns = '|'.join(pattern)
        series = df["Location"].str.contains(patterns)
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
    chicken = ["Chicken embryo cardiomyocytes", "Chicken", "chicken", "Hühn", "hühn"]

    list_of_patterns = [rat, hesc, ipsc, chicken]

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
    import re
    div_patterns = []

    # Define the regular expression pattern
    pattern = re.compile(r'\d*\W*div\W*\d*', re.IGNORECASE)

    # Loop through the "Location" column and filter out the strings that match the pattern
    for index in df["Location"]:
        if pattern.match(str(index)):
            div_patterns.append(index)
        else:
            div_patterns.append(None)

    # Find the closest number to "div" or "DIV" in each matched string
    div = []
    for div_str in div_patterns:
        if div_str is not None:
            # Extract all numbers from the string using regular expressions
            numbers = re.findall(r'\d+\.?\d*', div_str)
            # Convert the numbers to floats
            numbers = [float(n) for n in numbers]
            # Find the index of "div" or "DIV" in the string
            div_index = div_str.lower().find("div")
            if div_index != -1:
                # Find the number closest to the "div" or "DIV" position
                closest_num = min(numbers, key=lambda x: abs(numbers.index(x) - div_index))
                div.append(closest_num)
            else:
                div.append(None)
        else:
            div.append(None)

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

        patterns = '|'.join(pattern)
        series = df["Location"].str.contains(patterns)
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

    dose1 = ["10 microM", "10 muM", "-10muM"]
    dose2 = ["5 microM", "5 muM", "-5muM"]
    dose3 = ["2 microM", "2 muM", "-2muM"]
    dose4 = ["1 microM", "1 muM", "-1muM"]
    dose5 = ["0,5 microM", "0,5 muM", "-05muM"]
    dose6 = ["0,2 microM", "0,2 muM", "-02muM"]
    dose7 = ["0,1 microM", "0,1 muM", "-01muM"]

    list_of_patterns = [dose1, dose2, dose3, dose4, dose5, dose6, dose7]
    series_list = []
    for index, pattern in enumerate(list_of_patterns):

        # Random sign except zero: ^0    OR  ca*t will match 'ct' (0 'a' characters) OR   \[0-9] except special classes(numbers in this case)
        #patterns = '0*'+'|'.join(pattern)

        patterns = '|'.join(pattern)
        series = df["Location"].str.contains(patterns)
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
    nonionizing2 = ["Non-ionizing, GSM", "mobile", "GSM"]

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
        Appends a column called "Radiation dose" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_rad_dose : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Drug dose".
        """
    import re
    def closest_num(dose_str):
        """
        Returns the number closest to "Gy" in the given string based on position
        """
        # Define the regular expression pattern
        pattern = re.compile(r'\d*\.?\d*\s*Gy')

        # Find all matches in the string
        matches = pattern.findall(dose_str)

        # Calculate the distance between "Gy" and each match
        distances = [abs(dose_str.find("Gy") - dose_str.find(m)) for m in matches]

        # Find the index of the match with the smallest distance
        min_idx = distances.index(min(distances))

        # Extract the number from the matching string and convert to float
        closest_num = float(re.findall(r'\d+\.?\d*', matches[min_idx])[0])

        return closest_num

    rad_dose = []
    # Define the regular expression pattern
    pattern = re.compile(r'\d*\W*Gy\W*\d*')

    # Loop through the "Location" column and find the closest number to "Gy" in each matched string
    for index in df["Location"]:
        if pattern.match(str(index)):
            closest_num_val = closest_num(index)
            rad_dose.append(closest_num_val)
        else:
            rad_dose.append(None)

    df["Radiation dose"] = rad_dose

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
    art_patterns = []

    # Define the regular expression pattern
    pattern = re.compile(r'\d*\W*h\W*\d*', re.IGNORECASE)

    # Loop through the "Location" column and filter out the strings that match the pattern
    for index in df["Location"]:
        if pattern.match(str(index)):
            art_patterns.append(index)
        else:
            art_patterns.append(None)

    # Find the closest number to "h" or "H" in each matched string
    art = []
    for art_str in art_patterns:
        if art_str is not None:
            # Extract all numbers from the string using regular expressions
            numbers = re.findall(r'\d+\.?\d*', art_str)
            # Convert the numbers to floats
            numbers = [float(n) for n in numbers]
            # Find the index of "h" or "H" in the string
            div_index = art_str.lower().find("h")
            if div_index != -1:
                # Find the number closest to the "h" or "H" position
                closest_num = min(numbers, key=lambda x: abs(numbers.index(x) - div_index))
                art.append(closest_num)
            else:
                art.append(None)
        else:
            art.append(None)

    df["Time after radiation, h"] = art

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
        patterns = '|'.join(pattern)
        series = df["Location"].str.contains(patterns)
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
    eaf = ["Enes Aydin Furkan", "Furkan", "furkan", "Enes"]
    mj = ["Melanie Jungblut", "Jungblut"]
    il = ["Ismael Losano", "Losano"]
    nkr = ["Nico Kück", "Kück"]
    ah = ["Anja Heselide", "Heselide"]
    sg = ["Sebastian Gutsfeld", "Gutsfeld"]
    sh = ["Simone Hufgard", "Hufgard"]
    dfl = ["Dennis Flachs", "Flachs"]
    sho = ["Stefan Homes", "Homes"]
    ct = ["Christiane Thielemann", "Thielemann"]
    ca = ["Sebastian Allig", "Allig"]


    list_of_patterns = [ad, cn, jf, mm, ps, bk, tk, sk, pr, tkr, mc,
                        nn, os, eaf, mj, il, nkr, ah, sg, sh, dfl, sho, ct, ca]

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
        #The size is in Gb
        list.append(size)

    df_with_size = pd.DataFrame(list, columns=["Size"])
    df = pd.concat([df, df_with_size], axis=1)

    return df


def append_df_with_date(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Date" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_stimulation : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Date".
        """

    import re
    from datetime import datetime

    date_patterns = []

    # Define regular expression patterns for different date formats
    patterns = [
        r'\d{1,2}/\d{1,2}/\d{4}',  # mm/dd/yyyy
        r'\d{4}/\d{1,2}/\d{1,2}',  # yyyy/mm/dd
        r'\d{4}-\d{1,2}-\d{1,2}',  # yyyy-mm-dd
        r'\d{1,2}\-\d{1,2}\-\d{4}',  # dd-mm-yyyy
    ]

    # Loop through the "Location" column and filter out the strings that match the pattern
    for index in df["Location"]:
        date_pattern = None
        for pattern in patterns:
            match = re.search(pattern, str(index))
            if match:
                date_pattern = pattern
                break
        date_patterns.append(date_pattern)

    # Convert date strings to datetime objects in the "yyyy-mm-dd" format
    dates = []
    for pattern, loc in zip(date_patterns, df["Location"]):
        if pattern:
            match = re.search(pattern, str(loc))
            date_str = match.group(0)
            date_obj = None
            if pattern == r'\d{1,2}/\d{1,2}/\d{4}':
                date_obj = datetime.strptime(date_str, '%m/%d/%Y')
            elif pattern == r'\d{4}/\d{1,2}/\d{1,2}':
                date_obj = datetime.strptime(date_str, '%Y/%m/%d')
            elif pattern == r'\d{4}-\d{1,2}-\d{1,2}':
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            elif pattern == r'\d{1,2}-\d{1,2}-\d{4}':
                date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            dates.append(date_obj.strftime('%Y-%m-%d'))
        else:
            dates.append(None)

    df["Date"] = dates
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
        if row["Recording system"] == None:
            df = df.drop(index=index)
            df = df.reset_index(drop=True)

    return df

def copy_files_with_conditions(df, path):
    import shutil
    df = df[df["Drug application"] == 'Bicuculline']
    df = df[df["Recording system"] == "MEA"]
    df = df[df["Format"] == ".dat"]
    df = df[df["Drug dose"] == "10 microM"]
    #df = df[df["Size"] < 1.4]
    #df = df[df["Size"] > 1.3]

    print('Number of bicuculline files with chosen parameters:', len(df.index))

    return df

    """for row in df.iterrows():
        original_file_path = row[1]["Location"]
        file_name = os.path.basename(original_file_path)
        path_to_copy = os.path.join(path, file_name)
        new_file_path = os.path.normpath(path_to_copy)
        shutil.copyfile(original_file_path, new_file_path)
        csv_file_path = os.path.join(path, "info.csv")
        df.to_csv(csv_file_path)"""


