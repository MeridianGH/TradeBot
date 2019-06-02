from steam.client import SteamClient
client = SteamClient()


@client.on(client.EVENT_DISCONNECTED)
def handle_disconnect():
    if client.relogin_available:
        client.relogin()


@client.on(client.EVENT_CHAT_MESSAGE)
def handle_direct_message(user, text):
    user.send_message(text)


client.cli_login()

try:
    client.run_forever()
except KeyboardInterrupt:
    client.disconnect()
