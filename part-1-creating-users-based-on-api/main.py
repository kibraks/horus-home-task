"""
A script for creating Linux users based on data fetched from randomuser.me/api
"""

import json
import subprocess
from multiprocessing import Pool
from time import sleep

import requests


USER_API_URL = "https://randomuser.me/api/"

NUMBER_OF_USERS = 100


def fetch_user() -> tuple[str, str]:
    """Return full name and login of random user fetched from API"""
    try:
        res = requests.get(USER_API_URL)
        res.raise_for_status()
    except (requests.HTTPError, ConnectionError) as e:
        print(f"An error occured during fetching a user: {str(e)}")
        exit(1)
    try:
        res_data = json.loads(res.text)
        user_data = res_data["results"][0]
    except IndexError:
        # sometimes API randomly returns empty list of users. In this case we try again.
        sleep(2)
        return fetch_user()
    username = user_data["login"]["username"]
    full_name = f"{user_data["name"]["first"]} {user_data["name"]["last"]}"
    return username, full_name


def _fetch_user_wrapper(_) -> tuple[str, str]:
    """A wrapper making using fetch_user function as Pool.imap_unordered argument possible"""
    return fetch_user()


def create_user(username: str, full_name: str) -> None:
    """Create Linux user based on provided username and full name"""
    try:
        subprocess.run(["useradd", "-c", full_name, username])
    except subprocess.SubprocessError as e:
        print(f"Error during creating user {username}: {str(e)}")


if __name__ == "__main__":
    with Pool(5) as pool:
        users = []
        while len(users) < NUMBER_OF_USERS:
            new_users = pool.imap_unordered(_fetch_user_wrapper, range(5))
            users.extend(new_users)
            sleep(2)
        for username, full_name in users:
            create_user(username, full_name)

    subprocess.run(
        ["tail", f"-{NUMBER_OF_USERS}", "/etc/passwd"]
    )  # this line is added solely for testing purposes, so you can immediately see created users
