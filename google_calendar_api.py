import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError


from googleapiclient.discovery import build


class GoogleCalendarApi:
    KEYWORD_FROM_API = "fromAPI"

    def __init__(self):
        self.service = None
        self.SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def create_event(self, event):
        try:
            # Googleカレンダーにイベントを追加
            event_result = (
                self.service.events().insert(calendarId="primary", body=event).execute()
            )
            print(f"イベント作成完了: {event_result.get('htmlLink')}")

        except HttpError as error:
            print(f"An error occurred: {error}")

    # 近い10予定を表示
    def print_event_upcoming_10(self):
        try:
            # Call the Calendar API
            # 現在時刻を正しいRFC 3339形式で生成（UTC時刻）
            now = (
                datetime.datetime.now(datetime.timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            )
            print("Getting the upcoming 10 events")
            events_result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])

        except HttpError as error:
            print(f"An error occurred: {error}")

    # apiで登録した予定を削除
    def delete_all_events(self):
        try:
            # Call the Calendar API
            # 現在時刻を正しいRFC 3339形式で生成（UTC時刻）
            now = (
                datetime.datetime.now(datetime.timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            )
            print("Getting the upcoming 10 events")
            events_result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=100,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            events = events_result.get("items", [])

            # 条件：descriptionにキーワードを含む
            matched_events = [
                event
                for event in events
                if self.KEYWORD_FROM_API in event.get("description", "")
            ]

            if not matched_events:
                print("No upcoming matched events found.")
                return

            delete_count = 0
            for event in matched_events:
                print(
                    f"削除:{event['summary']} ({event['start'].get('dateTime', event['start'].get('date'))})"
                )
                self.service.events().delete(
                    calendarId="primary", eventId=event["id"]
                ).execute()
                delete_count += 1

            print(f"{delete_count} 件のイベントを削除しました。")

        except HttpError as error:
            print(f"An error occurred: {error}")

    # 認証初期化
    def authorize(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        service = build("calendar", "v3", credentials=creds)
        self.service = service
        return service
