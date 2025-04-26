import requests
import csv
import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

API_TOKEN = os.environ.get("API_KEY")
URL = "https://api.football-data.org/v4/teams/{id}/matches"
CSV_FILE_NAME = "matches_{team_id}.csv"


def fetch_matches_data(team_id):
    if team_id is None:
        print("Please input team_id.")
        return []

    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(URL.format(id=team_id), headers=headers)
    if response.status_code == 200:
        matches = response.json()
        # print("debug matches:", matches) #デバッグ用
        return matches
    else:
        print("Failed to fetch_matches_data. status code:", response.status_code)
        return []


def filter_matches_upcoming(matches):
    all_matches = matches.get("matches", [])

    # 試合日時が過去（実際に行われた）ものに限定してフィルタ
    future_matches = [
        match
        for match in all_matches
        if "utcDate" in match
        and datetime.fromisoformat(match["utcDate"][:-1]) > datetime.now()
    ]

    # 日付順にソート（新しい順）
    future_matches.sort(key=lambda x: x["utcDate"], reverse=False)

    # 直近10試合を取得
    future_matches_10 = future_matches[:10]

    # debug
    for match in future_matches_10:
        utc_time = datetime.fromisoformat(match["utcDate"][:-1])
        home_team = match["homeTeam"]["name"]
        away_team = match["awayTeam"]["name"]
        score = match["score"]["fullTime"]
        print(
            f"{utc_time.strftime('%Y-%m-%d')} | {home_team} {score['home']} - {score['away']} {away_team}/n"
        )

    return future_matches_10


def write_csv(matches, team_id, filename=CSV_FILE_NAME):
    # CSVファイルへ書き込み　(UTF-8エンコーディング)
    with open(
        filename.format(team_id=team_id), mode="w", newline="", encoding="utf-8"
    ) as csvfile:
        writer = csv.writer(csvfile)
        # ヘッダー行を書き込む
        writer.writerow(["Date", "HomeTeam", "Score", "AwayTeam"])
        # 各試合の情報を書き込む
        for match in matches:
            utc_time = datetime.fromisoformat(match["utcDate"][:-1])
            home_team = match["homeTeam"]["name"]
            away_team = match["awayTeam"]["name"]
            score = match["score"]["fullTime"]
            writer.writerow(
                [
                    utc_time.strftime("%Y-%m-%d"),
                    home_team,
                    f"{score['home']} - {score['away']}",
                    away_team,
                ]
            )

    print(f"CSV file '{filename}' has been created.")


def main():
    # いったんチェルシーのIDをセット
    team_id = 61
    matches = fetch_matches_data(team_id)
    if matches:
        future_matches = filter_matches_upcoming(matches)
        write_csv(future_matches, team_id)
    else:
        print("No matches data available.")


if __name__ == "__main__":
    main()
