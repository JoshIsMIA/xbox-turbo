'''
This program here uses the refresh tokens that you would get when you authenticate your xbox accounts to the xbox live api services (access_token,refresh_token,id_token), You would get your refresh token one time from 
logging in to your account and you can keep refresh the tokens for 90 days and then you will have to re-authenticate with xbox live for all the accounts you have.
'''
import json
import requests


CLIENT_ID = 'ENTER CLIENT ID HERE'
TOKEN_URL = 'https://login.microsoftonline.com/consumers/oauth2/v2.0/token'
REDIRECT_URI = 'http://localhost'

def load_tokens(file_path):
    with open(file_path, 'r') as f:
        tokens = json.load(f)
    return tokens

def save_tokens(file_path, tokens):
    with open(file_path, 'w') as f:
        json.dump(tokens, f, indent=4)

def refresh_access_token(refresh_token):
    data = {
        'client_id': CLIENT_ID,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'redirect_uri': REDIRECT_URI,
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json()  
    else:
        print(f"Failed to refresh token. Response: {response.content}")
        return None

def update_tokens(tokens):
    for token_entry in tokens:
        email = token_entry.get('email')
        refresh_token = token_entry.get('refresh_token')

        print(f"Refreshing tokens for {email}...")
        new_token_data = refresh_access_token(refresh_token)

        if new_token_data:
            token_entry['access_token'] = new_token_data.get('access_token')
            token_entry['refresh_token'] = new_token_data.get('refresh_token')
            print(f"Tokens updated for {email}")
        else:
            print(f"Failed to update tokens for {email}")

    return tokens

def refresh_all_tokens(file_path):
    tokens = load_tokens(file_path)
    updated_tokens = update_tokens(tokens)
    save_tokens(file_path, updated_tokens)
    print("All tokens updated and saved.")

if __name__ == "__main__":
    FILE_PATH = "tokens.json"  
    refresh_all_tokens(FILE_PATH)
