from fetch_football_data.fetch_matches_data import fetch_matches_data
from fetch_football_data.fetch_matches_data import filter_matches_upcoming
from datetime import datetime, timedelta, timezone

# フォーマット
event = {
    "summary": "打ち合わせ",
    "location": "オンライン",
    "description": "fromAPI プロジェクト進捗確認ミーティング",
    "start": {
        "dateTime": "2025-04-13T15:00:00+09:00",
        "timeZone": "Asia/Tokyo",
    },
    "end": {
        "dateTime": "2025-04-13T16:00:00+09:00",
        "timeZone": "Asia/Tokyo",
    },
    "reminders": {
        "useDefault": False,
        "overrides": [
            {"method": "email", "minutes": 60},
            {"method": "popup", "minutes": 10},
        ],
    },
}


class MatchEventHandler:
    def __init__(self, team_id):
        self.team_id = team_id

    def get_match_event(self):
        result = []
        matches = fetch_matches_data(self.team_id)

        if matches:
            # 直近の試合データを取得
            future_matches = filter_matches_upcoming(matches)

            for event in future_matches:
                # debug
                # print(f'{event["homeTeam"]["name"]} - {event["awayTeam"]["name"]}')

                # 標準的なISO 8601の形式（タイムゾーンなし）に変換（最後のZを除去)
                start_dt = datetime.fromisoformat(event["utcDate"][:-1])
                # 日本時間に変換
                start_dt_jst = start_dt + timedelta(hours=9)

                match_json = self.create_calendar_json(
                    event["homeTeam"]["name"],
                    event["awayTeam"]["name"],
                    start_dt_jst,
                )

                # debug
                print(start_dt_jst)

                result.append(match_json)

        else:
            print("No matches data available.")

        return result

    def create_calendar_json(self, home_team_name, away_team_name, start_dt):
        return {
            "summary": home_team_name + " - " + away_team_name,
            "location": "",
            "description": "fromAPI",
            "start": {
                "dateTime": start_dt.isoformat(timespec="seconds"),
                "timeZone": "Asia/Tokyo",
            },
            "end": {
                "dateTime": (start_dt + timedelta(hours=2)).isoformat(
                    timespec="seconds"
                ),
                "timeZone": "Asia/Tokyo",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }
