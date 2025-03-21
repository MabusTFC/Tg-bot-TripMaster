from config_g.config_google import *
from config_g import *
from google_auth_oauthlib.flow import Flow
import json
def authenticate_user():
    with open('credentials.json', 'r') as f:
        client_config = json.load(f)
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    print(f'Пожалуйста, авторизуйтесь через Google: {auth_url}')
    auth_code = input('Введите код авторизации: ').strip()
    flow.fetch_token(code=auth_code)
    creds = flow.credentials
    return creds