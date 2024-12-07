<p align="center">
  <img src="https://github.com/user-attachments/assets/15700e71-2c25-4997-a500-8085af010375" />
  <br>
  <br>
  a fun little discord bot for a fun little discord server
</p>

---

Hobbit is a homemade multipurpose discord bot for a server me and my friends have. It has everything we need, and nothing we don't.

> [!WARNING]  
> Hobbit, first and foremost, is a discord bot for *our* server. Your are more than welcome to modify this bot for your own needs, but I will probably not be accepting feature requests or PRs.
>
> And yes, our discord server is invite only. 

## Features

- Currency system with TinyDB for tracking Merits, points earned for participating in community events
- Shop is dynamically generated from a JSON file
- Message scheduling, with attachments
- Various brainrot references

## Use

First you'll need a Discord bot token. There are plenty or tutorials online, but the gist is to create an app, then a bot, and give it all Privileged Gateway Intents. Then invite it using an OAuth2 link with the following permissions and scopes:

- `bot` and `applications.commands`
- permission integer `2416176128`

Copy your bot token for later.

This project is created with [uv](https://github.com/astral-sh/uv), an ultra fast Python package and project manager.

Clone this repo:

```
git clone github.com/Hex-4/hobbit && cd hobbit
```

Create a .env file and add your bot token:

```
TOKEN = your_discord_bot_token
```

Then run with uv:

```
uv run bot.py
```

Without uv, install dependencies and run:

```
pip install tinydb py-cord python-dotenv
python bot.py
```

To manage shop items, edit `market.json`. Make sure each item has a unique ID. For role rewards, set `"role"` to the role ID, accessible by enabling Developer Mode in Discord.

> [!IMPORTANT]  
> If you are not me from the future (if so, hi!) you will probably need to change the channel IDs to match your server.

## Demo Video

https://www.youtube.com/watch?v=F1STzwj9wrw


