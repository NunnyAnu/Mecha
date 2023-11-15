from googleapiclient.http import MediaFileUpload
from Google import Create_Service

CLIENT_SECRET_FILE = 'client-secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# Upload a file
file_metadata = {
    'name': 'bolt2.fbx',
    'parents': ['1QlFw3dR1iYkuW86B8YEBYduxaJIX4iIQ']
}

media_content = MediaFileUpload('/Users/nunny/Desktop/Mecha/3DModel/bolt.fbx', mimetype='model/fbx')

file = service.files().create(
    body=file_metadata,

    media_body=media_content
).execute()

print(file)



