import json

import requests


class Messenger:
    def __init__(self):
        pass

    def send(self, message):
        raise NotImplementedError

    def sendWithMention(self, message):
        raise NotImplementedError


class DiscordMessenger(Messenger):
    def __init__(self, bot_token, channel_id, discord_notifiee_name=None):
        self.client = DiscordApiClient(bot_token)
        self.channel_id = int(channel_id)
        self.user_id = (
            self.getUserIdBy(discord_notifiee_name) if discord_notifiee_name else None
        )

    def send(self, message):
        self.client.post(f"/channels/{self.channel_id}/messages", message)

    def sendWithMention(self, message):
        message = (f"<@{self.user_id}> " + message) if self.user_id else message
        self.send(message)

    def getUserIdBy(self, userName):
        if not userName:
            return None

        channel = self.client.get(f"/channels/{self.channel_id}")
        members = self.client.get(f"/guilds/{channel['guild_id']}/members")

        target_user = None
        for member in members:
            user = member["user"]
            if user["username"] == userName:
                target_user = member["user"]
                break

        if not target_user:
            return None

        return target_user["id"]


class DiscordApiClient:
    __API_ROOT = "https://discord.com/api/v10"

    def __init__(self, bot_token):
        self.bot_token = bot_token

    def post(self, path, content):
        url = f"{DiscordApiClient.__API_ROOT}{path}"

        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json",
        }

        data = {"content": content}

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Request failed...: url = {url}, errorCode = {response.status_code}, message = {response.text}"
            )

    def get(self, path):
        url = f"{DiscordApiClient.__API_ROOT}{path}"

        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Request failed...: url = {url}, errorCode = {response.status_code}, message = {response.text}"
            )
