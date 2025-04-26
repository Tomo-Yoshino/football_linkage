
def main():
    # 画面orCLIからチーム選択
    selected_team = select_team()
    team_id = selected_team['id']

    # Football-data　APIから試合情報を取得
    football_client = FootballDataClient()
    matches = football_client.get_matches_for_team(team_id)

    # Googleカレンダーのクライアント初期化
    calender_client = GoogleCalenderClient()

    # 取得した試合情報をカレンダーに登録
    for match in matches:
        event = transform_match_to_event(match)
        calendat_client.create_event

if __name__ == "__main__":
    main()