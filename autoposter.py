import datetime
import os.path
import pickle
import subprocess
import time
from urllib.parse import urlparse

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from urlextract import URLExtract
import tempfile

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
RANGE_NAME = 'A3:H'

WEEKDAYS = {0: 'понедельник',
            1: 'вторник',
            2: 'среда',
            3: 'четверг',
            4: 'пятница',
            5: 'суббота',
            6: 'воскресенье'
            }


def get_post_image(id, image_file_name, drive):
    post_image_file = drive.CreateFile({'id': id})
    post_image_file.FetchMetadata(fields='title, downloadUrl')
    post_image_file.GetContentFile(image_file_name)


def get_post_text(id, text_file_name, drive):
    post_text_file = drive.CreateFile({'id': id})
    post_text_file.FetchMetadata(fields='title, exportLinks')
    post_text_file.GetContentFile(text_file_name, mimetype='text/plain')


def authorize_in_drive_application():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive


def authorize_in_sheets_application():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    return sheet


def check_spreadsheet(schedule_sheet, spreadsheet_id, drive):
    today_weekday = datetime.date.today().weekday()
    current_hour = datetime.datetime.now().hour

    url_extractor = URLExtract()

    sheets_document = schedule_sheet.values().get(spreadsheetId=spreadsheet_id,
                                                  range=RANGE_NAME, valueRenderOption='FORMULA').execute()

    posting_schedule = sheets_document.get('values', [])

    for index, posting_day_schedule in enumerate(posting_schedule):

        post_vk, post_tg, post_fb, publish_day, publish_time, \
        post_text_link, post_image_link, is_published = posting_day_schedule

        is_today = publish_day == WEEKDAYS[today_weekday]
        is_now = publish_time == current_hour
        is_already_published = is_published.lower().strip() == 'нет'

        if not (is_today and is_now and is_already_published):
            continue

        text_url = url_extractor.find_urls(post_text_link)[0]
        text_file_id = urlparse(text_url).query[3:]

        image_url = url_extractor.find_urls(post_image_link)[0]
        image_file_id = urlparse(image_url).query[3:]


        with tempfile.NamedTemporaryFile() as image_tempfile, tempfile.NamedTemporaryFile() as text_tempfile:
            get_post_text(text_file_id, text_tempfile.name, drive)
            get_post_image(image_file_id, image_tempfile.name, drive)

            terminal_commands = ['python3', 'vk_tg_fb_posting.py', image_tempfile.name, text_tempfile.name]

            if post_vk.lower().strip() == 'да':
                terminal_commands.append('-pv')
            elif post_fb.lower().strip() == 'да':
                terminal_commands.append('-pf')
            elif post_tg.lower().strip() == 'да':
                terminal_commands.append('-pt')

            exit_code = subprocess.call(terminal_commands)

            if exit_code:
                print('Program "vk_tg_fb_posting.py" finished with exit code', exit_code)

            schedule_sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range="'Лист1'!H{}".format(index + 3),
                body={'values': [['да'], ]},
                valueInputOption='RAW').execute()
            print('Post was published successfully!')


if __name__ == '__main__':
    load_dotenv()
    spreadsheet_id = os.getenv('SPREADSHEET_ID')

    schedule_sheet = authorize_in_sheets_application()
    drive = authorize_in_drive_application()


    while True:
        check_spreadsheet(schedule_sheet, spreadsheet_id, drive)
        time.sleep(60)
