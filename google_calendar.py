from google_calendar_api import GoogleCalendarApi
from match_event_handler import MatchEventHandler


def main():
    # 試合情報を取得
    match_event_handler = MatchEventHandler(61)
    events = match_event_handler.get_match_event()

    gcapi = GoogleCalendarApi()
    gcapi.authorize()

    # イベント作成
    for event in events:
        gcapi.create_event(event)

    # 今後10予定を表示
    gcapi.print_event_upcoming_10()

    # 本ツールで追加した予定を削除する
    # gcapi.delete_all_events()


if __name__ == "__main__":
    main()
