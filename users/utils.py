import requests
from users.exceptions import GithubException
import json


def get_token_and_profile(client_id, client_secret, code):
    session = requests.Session()
    token_request = session.post(
        f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
        headers={"Accept": "application/json"},
    )
    token_json = json.loads(token_request.text)
    error = token_json.get("error", None)
    if error is not None:
        raise GithubException("Can't get access token")
    else:
        access_token = token_json.get("access_token")
        profile_request = session.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json",
            },
        )
        profile_json = json.loads(profile_request.text)
        return token_json, profile_json
