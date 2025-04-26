import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# 登録するイベント情報
event = {
    'summary': '打ち合わせ',
    'location': 'オンライン',
    'description': 'プロジェクト進捗確認ミーティング',
    'start': {
        'dateTime': '2025-04-08T15:00:00+09:00',
        'timeZone': 'Asia/Tokyo',
    },
    'end': {
        'dateTime': '2025-04-08T16:00:00+09:00',
        'timeZone': 'Asia/Tokyo',
    },
    'attendees': [
        {'email': 'example@example.com'},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': 60},
            {'method': 'popup', 'minutes': 10},
        ],
    },
}

def set_event(service):

  try:
    # Googleカレンダーにイベントを追加
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print(f"イベント作成完了: {event_result.get('htmlLink')}")

  except HttpError as error:
    print(f"An error occurred: {error}")

def print_event(service):
  try:
    # Call the Calendar API
    # 現在時刻を正しいRFC 3339形式で生成（UTC時刻）
    now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
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

def authorize():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  service = build("calendar", "v3", credentials=creds)
  return service


def main():

  service = authorize()
  # print_event(service)
  set_event(service)


if __name__ == "__main__":
  main()