import praw

import requests
import datetime

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    username="",
    password="",
    user_agent="",
)


# Define the JSON data
def json_data(bu, du, mod, br, pfp):
    future_timestamp = ""

    # just some stuff to show time
    if du != "permanent":
        current_datetime = datetime.datetime.now()
        future_datetime = current_datetime + datetime.timedelta(days=int(du))
        future_timestamp = f"<t:{int(future_datetime.timestamp())}:R>"
    else:
        future_timestamp = "Forever"

    # json variables
    banned_user = f"[{bu}](https://www.reddit.com/u/{bu})"
    time_until = f"Time: {du}days\nUntil: {future_timestamp}"
    mod_who_banned = f"[{mod}](https://www.reddit.com/u/{mod})"
    ban_res = f"{br}"

    # json return val
    json_data1 = {
        "content": None,
        "embeds": [
            {
                "title": f"{bu} was banned",
                "color": 5814783,
                "fields": [
                    {
                        "name": "User Profile:",
                        "value": banned_user,
                    },
                    {
                        "name": "Duration:",
                        "value": time_until,
                    },
                    {
                        "name": "Responsible Moderator:",
                        "value": mod_who_banned,
                    },
                    {"name": "Ban Reason:", "value": ban_res},
                ],
                "thumbnail": {
                    "url": f"{pfp}",
                    "height": 0,
                    "width": 0,
                },
            }
        ],
        "attachments": [],
    }

    return json_data1


webhook_url = ""  # Webhook that sends data over to discord

for item in reddit.subreddit("sipstea").mod.stream.log(
    skip_existing=True
):  # skip_existing=True):

    if item.action == "banuser" and "chat" in item.description.lower():
        response = requests.post(
            webhook_url,
            json=json_data(
                item.target_author,
                (
                    item.details.split("days")[0]
                    if "days" in item.details
                    else "permanent"
                ),
                item._mod,
                item.description,
                reddit.redditor(item.target_author).icon_img,
            ),
        )
