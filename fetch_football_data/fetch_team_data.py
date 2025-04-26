import requests
import csv
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_TOKEN = os.environ.get('API_KEY')
URL = "https://api.football-data.org/v4/teams/{id}"
CSV_FILE_NAME = "team_{team_name}.csv"

def fetch_team_data(team_id):
    if team_id is None:
        print("Please input team_id.")
        return []

    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(URL.format(id=team_id), headers=headers)
    if response.status_code == 200:
        team = response.json()
        print("debug team:", team) #デバッグ用
        return team
    else:
        print("Failed to fetch_team_data. status code:", response.status_code)
        return []

def write_csv(team, filename=CSV_FILE_NAME):
    team_name = team.get('name')

    # CSVファイルへ書き込み　(UTF-8エンコーディング)
    with open(filename.format(team_name=team_name), mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # ヘッダー行を書き込む
        writer.writerow(["ID", "Name", "Tla", "Crest", "Founded", "Venue", "Squads"])
        # 各コンペティションの情報を書き込む
        team_id = team.get("id")
        tla = team.get("tla")
        crest = team.get("crest")
        founded = team.get("founded")
        venue = team.get("venue")
        squads = len(team.get("squad")) # スカッド数
        writer.writerow([team_id, team_name, tla, crest, founded, venue, squads])
    print(f"CSV file '{filename}' has been created.")

def main():
    # いったんチェルシーのIDをセット
    team = fetch_team_data(61)
    if team:
        write_csv(team)
    else:
        print("No team data available.")

if __name__ == "__main__":
    main()