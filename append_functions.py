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

    neuro = ["Neuro", "neuro", "NS", "Rat", "Ratneuronen"]

    cardio = ["Cardio", "cardio", "Kardio", "myocytes", "CD2", "HMZ", "hmz", "Chicken", "chicken", "Hühn", "hühn", "Huhn", "huhn"]

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

    rat = ["Rat neurons", "Ratneuronen", "Rat"]
    hesc = ["hESC", "Human embryonic stem cells", "hES"]
    ipsc = ["iPSC", "Induced pluripotent stem cells", "iPS", "induced", "iCell", "Smolin", "smolin", "Frieß", "frieß", "Friess", "friess"]
    hipsc = ["hiPSC", "Human induced pluripotent stem cells", "hiPS"]
    chicken = ["Chicken embryo cardiomyocytes", "Chicken", "chicken", "Hühn", "hühn", "Huhn", "huhn"]
    hek = ["HEK", "Human Embryonic Kidney"]

    list_of_patterns = [rat, hesc, ipsc, hipsc, chicken, hek]

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



def append_df_with_div_dap(df: pd.DataFrame) -> pd.DataFrame:
    """
    Appends a column called "DIV / DAP" to a given DataFrame
    Parameters
    ----------
    df : pd.DataFrame
        Data Frame with information about the given Directory.
    Returns
    -------
    df_with_div_dap : pd.DataFrame
        Returns a Pandas DataFrame with a new column "DIV / DAP".
    """

    div_dap = []

    div_pattern = re.compile(r'(\d+)\s*(?:div|DIV)\s*(\d+)?', re.IGNORECASE)
    dap_pattern = re.compile(r'(\d+)\s*(?:dap|DaP|DAP)\s*(\d+)?', re.IGNORECASE)

    for location in df["Location"]:
        closest_num_div = None
        closest_num_dap = None
        last_div_position = -1  # Initialize the position of the last found DIV pattern
        last_dap_position = -1  # Initialize the position of the last found DAP pattern

        # Finding the closest number for DIV pattern
        match_div = div_pattern.findall(str(location))
        if match_div:
            for num1, num2 in match_div:
                num1_position = location.find(num1)
                num2_position = location.find(num2) if num2 else -1

                # Check if the number is greater than zero, does not have leading zeros, and is less than or equal to 60
                if num1[0] != '0' and int(num1) > 0 and int(num1) <= 60:
                    num1_dist = abs(num1_position - last_div_position)
                    num2_dist = abs(num2_position - last_div_position) if num2_position >= 0 else num1_dist + 1

                    # Prioritize the left number
                    if num2_dist <= num1_dist:
                        if int(num2) > 0 and int(num2) <= 60:  # Check if num2 is valid
                            closest_num_div = num2
                            last_div_position = num2_position
                    elif int(num1) <= 60:
                        closest_num_div = num1
                        last_div_position = num1_position

        # Finding the closest number for DaP pattern
        match_dap = dap_pattern.findall(str(location))
        if match_dap:
            for num1, num2 in match_dap:
                num1_position = location.find(num1)
                num2_position = location.find(num2) if num2 else -1

                # Check if the number is greater than zero, does not have leading zeros, and is less than or equal to 60
                if num1[0] != '0' and int(num1) > 0 and int(num1) <= 60:
                    num1_dist = abs(num1_position - last_dap_position)
                    num2_dist = abs(num2_position - last_dap_position) if num2_position >= 0 else num1_dist + 1

                    # Prioritize the left number
                    if num2_dist <= num1_dist:
                        if int(num2) > 0 and int(num2) <= 60:  # Check if num2 is valid
                            closest_num_dap = num2
                            last_dap_position = num2_position
                    elif int(num1) <= 60:
                        closest_num_dap = num1
                        last_dap_position = num1_position

        if closest_num_div:
            div_dap.append(f"{closest_num_div} DIV")
        elif closest_num_dap:
            div_dap.append(f"{closest_num_dap} DAP")
        else:
            div_dap.append(None)

    df["DIV / DAP"] = div_dap

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
    bic = ["Bicuculline","bicuculline", "BIC", "Bic", "bic"]

    #Searching for experiments with "Carbamazepine"
    carba = ["Carbamazepine", "carbamazepine", "carba", "Carba"]

    # Searching for experiments with "LSD"
    lsd = ["LSD", "lsd"]

    # Searching for experiments with "Levetiracetam"
    lev = ["Levetiracetam", "levetiracetam", "lev"]

    # Searching for experiments with "Cisplatin"
    cisplatin = ["Cisplatin", "cisplatin"]

    # Searching for experiments with "Isoproterenol"
    isoprot = ["Isoproterenol", "isoproterenol"]

    # Searching for experiments with "Amitriptyline"
    amitript = ['Amitriptyline', "amitriptyline"]


    list_of_patterns = [bic, carba, lsd, lev, cisplatin, isoprot, amitript]
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

    # Initialize an empty "Drug dose" column
    df["Drug dose"] = None

    # Part of the function to search for patterns
    pattern1 = re.compile(r'(\d+(?:,\d+)?)\D*(?:µM|microM|muM)\D*(\d+)?', re.IGNORECASE)
    pattern2 = re.compile(r'(\d+(?:,\d+)?)\D*(?:µL|microL|muL)\D*(\d+)?', re.IGNORECASE)

    for index, row in df.iterrows():
        location = row["Location"]
        closest_num1 = None
        closest_num2 = None

        match1 = pattern1.search(str(location))
        match2 = pattern2.search(str(location))

        # Function to calculate the distance considering letters and digits
        def calculate_distance(match, text):
            if match:
                distance = 0
                for i, (a, b) in enumerate(zip(match.group(), text)):
                    if a != b:
                        distance += abs(ord(a) - ord(b))
                    distance += abs(i - len(match.group()))
                return distance
            return float('inf')

        if match1:
            num1 = match1.group(1).replace(',', '.')
            num2 = match1.group(2)
            dist1 = calculate_distance(match1, str(location))
            if num2 or (not closest_num1) or dist1 < calculate_distance(pattern1.search(str(closest_num1)), str(location)):
                closest_num1 = f"{float(num1):.1f} µM"

        if match2:
            num1 = match2.group(1).replace(',', '.')
            num2 = match2.group(2)
            dist2 = calculate_distance(match2, str(location))
            if num2 or (not closest_num2) or dist2 < calculate_distance(pattern2.search(str(closest_num2)), str(location)):
                closest_num2 = f"{float(num1):.1f} µL"

        # Handle cases where "01" should be treated as "0.1"
        if not closest_num1 and closest_num2:
            closest_num1 = closest_num2.replace("01", "0.1")

        # Assign the closest number to the "Drug dose" column
        if pd.isna(row["Drug dose"]):
            if closest_num1:
                df.at[index, "Drug dose"] = closest_num1
            elif closest_num2:
                df.at[index, "Drug dose"] = closest_num2

    # Continue with additional patterns from list_of_patterns
    for pattern_set in list_of_patterns:
        pattern = '|'.join(pattern_set)

        # Search for the pattern and assign if the "Drug dose" column is not filled
        mask = df["Location"].str.contains(pattern, case=False)
        df.loc[mask & pd.isna(df["Drug dose"]), "Drug dose"] = pattern_set[0]

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
    ionizing1 = ["Ionizing, X-Ray", "X-Ray", "X-ray", "Xray", "XRay"]
    ionizing2 = ["Ionizing, heavy ions", " Ti ", " C ", " Fe ", " Ca "]
    nonionizing1 = ["Non-ionizing, TETRA", "TETRA"]
    nonionizing2 = ["Non-ionizing, GSM", "Mobile", "mobile", "GSM"]

    list_of_patterns = [rad, ionizing1, ionizing2, nonionizing1, nonionizing2]

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
            Returns a Pandas DataFrame with a new column "Radiation dose".
        """

    pattern = re.compile(r'(\d*\.?\d+)\s*(Gy)')
    rad_dose = []

    for index in df["Location"]:
        if isinstance(index, str):
            matches = pattern.findall(index)
            if matches:
                # Extracting the number from the matching string and convert to float
                closest_num_dose = float(matches[0][0])
                rad_dose.append(f"{closest_num_dose} Gy")
            else:
                rad_dose.append(None)
        else:
            rad_dose.append(None)

    df["Radiation dose"] = rad_dose

    return df




def append_df_with_br_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Appends a column called "Time before radiation" to a given DataFrame
    Parameters
    ----------
    df : pd.DataFrame
        Data Frame with information about the given Directory.
    Returns
    -------
    df_with_br_time : pd.DataFrame
        Returns a Pandas DataFrame with a new column "Time before radiation".
    """

    time = []

    h_br_pattern = re.compile(r'(\d+)\D*(?:h bR|h b.R.|h vor Bestrahlung)\D*(\d+)?', re.IGNORECASE)
    d_br_pattern = re.compile(r'(\d+)\D*(?:d bR|d b.R.|d vor Bestrahlung)\D*(\d+)?', re.IGNORECASE)
    m_br_pattern = re.compile(r'(\d+)\D*(?:m bR|m b.R.|m vor Bestrahlung)\D*(\d+)?', re.IGNORECASE)

    for location in df["Location"]:
        closest_num_h_br = None
        closest_num_d_br = None
        closest_num_m_br = None

        # Finding the closest number for h_br_pattern
        match_h_br = h_br_pattern.search(str(location))
        if match_h_br:
            num1 = match_h_br.group(1)
            num2 = match_h_br.group(2)
            if num2 and abs(match_h_br.start(2) - match_h_br.start(1)) < abs(match_h_br.start(1) - match_h_br.end(1)):
                closest_num_h_br = num2
            else:
                closest_num_h_br = num1

        match_d_br = d_br_pattern.search(str(location))
        if match_d_br:
            num1 = match_d_br.group(1)
            num2 = match_d_br.group(2)
            if num2 and abs(match_d_br.start(2) - match_d_br.start(1)) < abs(match_d_br.start(1) - match_d_br.end(1)):
                closest_num_d_br = num2
            else:
                closest_num_d_br = num1

        match_m_br = m_br_pattern.search(str(location))
        if match_m_br:
            num1 = match_m_br.group(1)
            num2 = match_m_br.group(2)
            if num2 and abs(match_m_br.start(2) - match_m_br.start(1)) < abs(match_m_br.start(1) - match_m_br.end(1)):
                closest_num_m_br = num2
            else:
                closest_num_m_br = num1

        if closest_num_h_br:
            time.append(f"{closest_num_h_br} h b.R.")
        elif closest_num_d_br:
            time.append(f"{closest_num_d_br} d b.R.")
        elif closest_num_m_br:
            time.append(f"{closest_num_m_br} m b.R.")
        else:
            time.append(None)

    df['Time before radiation'] = time

    return df


def append_df_with_ar_time(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Time after radiation" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_br_or_ar_time : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Time after radiation".
    """

    time = []

    h_ar_pattern = re.compile(r'(\d+)\D*(?:h aR|h a.R.|h nach Bestrahlung)\D*(\d+)?', re.IGNORECASE)
    d_ar_pattern = re.compile(r'(\d+)\D*(?:d aR|d a.R.|d nach Bestrahlung)\D*(\d+)?', re.IGNORECASE)
    m_ar_pattern = re.compile(r'(\d+)\D*(?:m aR|m a.R.|m nach Bestrahlung)\D*(\d+)?', re.IGNORECASE)

    target_pattern = re.compile(r'(\d+d aR|d a.R.|d nach Bestrahlung)\s*a', re.IGNORECASE)

    for location in df["Location"]:
        closest_target = None

        # Finding the closest target pattern
        match_target = target_pattern.findall(str(location))
        if match_target:
            closest_target = match_target[-1]  # Take the last match

        if closest_target:
            time.append(closest_target)
        else:
            closest_num_h_ar = None
            closest_num_d_ar = None
            closest_num_m_ar = None



        match_h_ar = h_ar_pattern.search(str(location))
        if match_h_ar:
            num1 = match_h_ar.group(1)
            num2 = match_h_ar.group(2)
            if num2 and abs(match_h_ar.start(2) - match_h_ar.start(1)) < abs(match_h_ar.start(1) - match_h_ar.end(1)):
                closest_num_h_ar = num2
            else:
                closest_num_h_ar = num1

        match_d_ar = d_ar_pattern.search(str(location))
        if match_d_ar:
            num1 = match_d_ar.group(1)
            num2 = match_d_ar.group(2)
            if num2 and abs(match_d_ar.start(2) - match_d_ar.start(1)) < abs(match_d_ar.start(1) - match_d_ar.end(1)):
                closest_num_d_ar = num2
            else:
                closest_num_d_ar = num1

        match_m_ar = m_ar_pattern.search(str(location))
        if match_m_ar:
            num1 = match_m_ar.group(1)
            num2 = match_m_ar.group(2)
            if num2 and abs(match_m_ar.start(2) - match_m_ar.start(1)) < abs(match_m_ar.start(1) - match_m_ar.end(1)):
                closest_num_m_ar = num2
            else:
                closest_num_m_ar = num1


        if closest_num_h_ar:
            time.append(f"{closest_num_h_ar} h a.R.")
        elif closest_num_d_ar:
            time.append(f"{closest_num_d_ar} d a.R.")
        elif closest_num_m_ar:
            time.append(f"{closest_num_m_ar} m a.R.")
        else:
            time.append(None)

    df['Time after radiation'] = time

    return df





def append_df_with_lab(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Laboratory" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_drugs_application : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Laboratory".
        """


    biomems = ["BioMEMS Lab", "BioMEMS", "BIOMEMS", "biomems", "Biomems"]
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
    df_with_lab = pd.DataFrame(list, columns=["Laboratory"])
    df = pd.concat([df, df_with_lab], axis=1)

    performer_names = [
        "Andreas Daus", "Christoph Nick", "Margot Mayer", "Berit Körbitzer", "Tim Köhler",
        "Steffen Künzinger", "Pascal Rüdel", "Tobias Kraus", "Nahid Nafez", "Ismael Losano",
        "Nico Kück", "Sebastian Gutsfeld", "Simone Hufgard", "Dennis Flachs",
        "Christiane Thielemann", "Sebastian Allig", "Hitesh Kanoia", "Karin Schiling",
        "Wenus Nafez", "Diana Khropost"
    ]

    mask = df["Performer"].isin(performer_names)

    # Update the last part to save "BioMEMS Lab" where pattern from performer_names was found and the "Laboratory" is None
    df.loc[mask & df["Laboratory"].isnull(), "Laboratory"] = "BioMEMS Lab"

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
    jf = ["Johannes Frieß", "Frieß", "frieß", "Friess", "friess"] #b and GSI and Darmstadt
    mm = ["Margot Mayer", "MM", "Mayer", "mayer"]
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

    df_with_size = pd.DataFrame(list, columns=["Size, Gb"])
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
        if row["Size, Gb"] == 0:
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

    control = ["Control", "Kontrol", "DMSO"]
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

    # Defining the regular expression pattern to match kHz, Hz or MHz in different formats
    pattern1 = re.compile(r'(\d+)\D*(?:kHz|kH)\D*(\d+)?', re.IGNORECASE)
    pattern2 = re.compile(r'(\d+)\D*(?:Hz)\D*(\d+)?', re.IGNORECASE)
    pattern3 = re.compile(r'(\d+)\D*(?:MHz)\D*(\d+)?', re.IGNORECASE)

    for location in df["Location"]:
        closest_num1 = None
        closest_num2 = None
        closest_num3 = None

        match1 = pattern1.search(str(location))
        if match1:
            num1 = match1.group(1)
            num2 = match1.group(2)
            if num2 and abs(match1.start(2) - match1.start(1)) < abs(match1.start(1) - match1.end(1)):
                closest_num1 = num2
            else:
                closest_num1 = num1

        match2 = pattern2.search(str(location))
        if match2:
            num1 = match2.group(1)
            num2 = match2.group(2)
            if num2 and abs(match2.start(2) - match2.start(1)) < abs(match2.start(1) - match2.end(1)):
                closest_num2 = num2
            else:
                closest_num2 = num1

        match3 = pattern3.search(str(location))
        if match3:
            num1 = match3.group(1)
            num2 = match3.group(2)
            if num2 and abs(match3.start(2) - match3.start(1)) < abs(match3.start(1) - match3.end(1)):
                closest_num3 = num2
            else:
                closest_num3 = num1

        if closest_num1:
            rate.append(f"{closest_num1} kHz")
        elif closest_num2:
            rate.append(f"{closest_num2} Hz")
        elif closest_num3:
            rate.append(f"{closest_num3} MHz")
        else:
            rate.append(None)

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

def append_df_with_nano(df: pd.DataFrame) -> pd.DataFrame:
    """
    Appends a column called "Nanoparticles" to a given DataFrame
    Parameters
    ----------
    df : pd.DataFrame
        Data Frame with information about the given Directory.
    Returns
    -------
    df_with_nano : pd.DataFrame
        Returns a Pandas DataFrame with a new column "Nanoparticles".
    """

    gnr = ["GNR", "gnr", "NanoRods", "nanorods", "Nanorods"]
    gnp = ["GNP", "GnP", "nanoparticles"]

    list_of_patterns = [gnr, gnp]

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
    df_with_nano = pd.DataFrame(list, columns=["Nanoparticles"])
    df = pd.concat([df, df_with_nano], axis=1)

    return df

def append_df_with_laser(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Laser" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_laser : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Laser".
        """

    laser = ["Laser", "laser"]

    pattern_laser = '|'.join(laser)
    df["Laser"] = df["Location"].str.contains(pattern_laser)
    df["Laser"] = df["Laser"].map({True: "Laser", False: None})

    return df

def append_df_with_timeframe(df: pd.DataFrame) -> pd.DataFrame:
    """
        Appends a column called "Timeframe, s" to a given DataFrame
        Parameters
        ----------
        df : pd.DataFrame
            Data Frame with information about the given Directory.
        Returns
        -------
        df_with_timeframe : pd.DataFrame
            Returns a Pandas DataFrame with a new column "Timeframe, s".
        """

    timeframe = []

    pattern = re.compile(r'(\d+)\s*[_ ]*[s]\b')

    for location in df['Location']:
        match = pattern.search(str(location))
        if match:
            timefr = int(match.group(1))
        else:
            timefr = None
        timeframe.append(timefr)

    df["Timeframe, s"] = timeframe

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
