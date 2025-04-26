import requests
import csv
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_TOKEN = os.environ.get('API_KEY')
URL = "https://api.football-data.org/v4/competitions"
CSV_FILE_NAME = "competitions.csv"

def fetch_competitions_data():
    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        competitions = data.get("competitions", [])
        print("debug competitions:", competitions) #デバッグ用
        return competitions
    else:
        print("Failed to fetch_competitions_data. status code:", response.status_code)
        return []

def write_csv(competitions, filename=CSV_FILE_NAME):
    # CSVファイルへ書き込み　(UTF-8エンコーディング)
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # ヘッダー行を書き込む
        writer.writerow(["ID", "Name", "Code", "Area", "Plan"])
        # 各コンペティションの情報を書き込む
        for comp in competitions:
            comp_id = comp.get("id")
            name = comp.get("name")
            code = comp.get("code")
            area_name = comp.get("area", {}).get("name")
            plan = comp.get("plan")
            writer.writerow([comp_id, name, code, area_name, plan])
    print(f"CSV file '{filename}' has been created.")

def main():
    competitions = fetch_competitions_data()
    if competitions:
        write_csv(competitions)
    else:
        print("No competitions data available.")

if __name__ == "__main__":
    main()