import requests
import csv
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_TOKEN = os.environ.get('API_KEY')
URL = "https://api.football-data.org/v4/competitions/{id}/teams"
CSV_FILE_NAME = "competition_{competition_name}.csv"

def fetch_competition_data(competition_id):
    if competition_id is None:
        print("Please input competition_id.")
        return []

    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(URL.format(id=competition_id), headers=headers)
    if response.status_code == 200:
        competition = response.json()
        print("debug competition:", competition) #デバッグ用
        return competition
    else:
        print("Failed to fetch_competition_data. status code:", response.status_code)
        return []

def write_csv(competition, filename=CSV_FILE_NAME):
    competition_name = competition.get('competition').get('name')

    # CSVファイルへ書き込み　(UTF-8エンコーディング)
    with open(filename.format(competition_name=competition_name), mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # ヘッダー行を書き込む
        writer.writerow(["ID", "Name", "Tla", "Crest"])
        # 各コンペティションの情報を書き込む
        for team in competition.get('teams'):
            team_id = team.get("id")
            name = team.get("name")
            tla = team.get("tla")
            crest = team.get("crest")
            writer.writerow([team_id, name, tla, crest])
    print(f"CSV file '{filename}' has been created.")

def main():
    # いったんプレミアリーグのIDをセット
    competition = fetch_competition_data(2021)
    if competition:
        write_csv(competition)
    else:
        print("No competition data available.")

if __name__ == "__main__":
    main()