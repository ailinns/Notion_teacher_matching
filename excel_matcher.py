import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "CSIT_Database_Maching.xlsx")


def load_excel_data():
    df = pd.read_excel(FILE_PATH, skiprows=2)

    df.columns = [
        "No",
        "Name_TH",
        "Name_EN",
        "Email",
        "Expertise_TH",
        "Expertise_EN",
        "Keywords_TH",
        "Keywords_EN"
    ]

    return df


def normalize_text(text):
    return str(text).lower().strip()


def match_advisor_from_excel(keywords, top_k=3):

    if not keywords:
        return []

    df = load_excel_data()

    keywords = [normalize_text(k) for k in keywords]
    total_keywords = len(keywords)

    results = []

    for _, row in df.iterrows():

        advisor_name = row["Name_EN"]
        expertise_text = normalize_text(row["Keywords_EN"])
        expertise_th = normalize_text(row["Keywords_TH"])

        match_count = 0

        for k in keywords:
            if k in expertise_text or k in expertise_th:
                match_count += 1

        if match_count > 0:
            percentage = round((match_count / total_keywords) * 100, 2)

            results.append({
                "advisor": advisor_name,
                "match_count": match_count,
                "percentage": percentage
            })

    results = sorted(results, key=lambda x: x["percentage"], reverse=True)

    return results[:top_k]