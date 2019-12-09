import logging

import googleapiclient.discovery
from google.oauth2 import service_account

logger = logging.getLogger(__name__)

class MemberSheet(object):
    def __init__(self):
        pass

    def get_credentials(self):
        client_secret_file = 'client_secret.json'
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly'
        ]
        credentials = service_account.Credentials.from_service_account_file(client_secret_file, scopes=scopes)

        return credentials

    def get_my_combat_point(self):
        spreadsheet_id = '1HK96UyIEEiX3Q67yMzpA-bc5eLi0jHm3pgJSTXFnqkY'
        range_name = 'メンバー情報一覧!A1:P'

        credentials = self.get_credentials()
        service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range_name).execute()
        values = result.get('values', [])

        print()
        logger.info(values)
        return ['てｓｔ']


if __name__ == '__main__':
    member_sheet = MemberSheet()
    result = member_sheet.get_my_combat_point()
