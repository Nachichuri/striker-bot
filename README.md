```
     _        _ _               _           _
    | |      (_) |             | |         | |
 ___| |_ _ __ _| | _____ _ __  | |__   ___ | |_
/ __| __| '__| | |/ / _ \ '__| | '_ \ / _ \| __|
\__ \ |_| |  | |   <  __/ |    | |_) | (_) | |_
|___/\__|_|  |_|_|\_\___|_|    |_.__/ \___/ \__|
```

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/nachichuri/striker-bot/Build?style=flat-square)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/Nachichuri/striker-bot?style=flat-square)
![GitHub](https://img.shields.io/github/license/Nachichuri/striker-bot?style=flat-square)

## What is striker?

A Telegram bot you can self-host and allows you to have a list of your friends or colleagues with two statuses: strikes ⚡ and pastries owed 🥐. If you've never heard of strikes, take a look in the [rules section](#so-what-are-the-rules-).

If you've never had some kind of strike system with your colleagues or friends, you might want to consider it since it's a lot of fun!

## So what are the rules? 📜

The rules are pretty straightforward.

1. Every time you screw up, you get a strike ⚡.
2. Once you reach a certain number of strikes (usually 3), your strike counter resets back to 0, and your pastries 🥐 counter increases by one.
3. Having a positive pastries counter means you'll have to live with a _veil of shame_ until you bring pastries\* for the team to the office.
4. If somebody thinks you deserve it, they can give you negative strikes, and you can have up to 5 negative strikes.
5. The only way to decrease your pastries counter is by bringing food to the office.

> `*` "_pastries_" stands for _edible things that can be shared with my colleagues at the office_, not only pastries, so you can cook your specialties too!

## Available commands:

- 🤓 `/rules`: what this is all about.
- 🔎 `/status`: see overall or user-specific status.
- ⚡ `/strike user n`: add n strikes to the user.
- 🥐 `/brought_pastries user`: substract an owed pastry when the user settles a pastry debt.
- 👶 `/create_user user`: adds a new user to the database.

## How can I use it? 🔧

To use `striker-bot`, you'll have to create your own Telegram bot first. If you've never created a bot, [here's Telegram's official documentation](https://core.telegram.org/bots), but the process is very straightforward (and when you start creating bots, there's no turning back).

Once the bot is created, there are a few things you'll need to have:

- **Telegram bot API token:** you'll get it from the Bot Father once you create the bot.
- **Allowed chat IDs:** you wouldn't want anyone being able to talk to your bot and see your teammates or friends' names, right? So you'll have to provide the chat IDs you want the bot to specifically answer to (every Telegram user and group have their own ID).

### Using Docker 🐳

The fastest way to get `striker-bot` up and running is to use Docker. There's a [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/) template you can use by opening your terminal and running:

```
cookiecutter --directory .cookiecutter https://github.com/Nachichuri/striker-bot/
```

Cookiecutter will ask you for couple of questions, the most important ones being:

- **bot_api_token:** the API token the Bot Father sent you.
- **database_name:** the name of the SQLite database you'll persist the strikes in (without file extension).
- **allowed_groups:** comma-separated values of user and/or group IDs that the bot will answer to.
- **threshold:** number of strikes required to add a new pastry to the pastries counter.
- **database_persistance_location:** location on the host computer where you want to save your database in.

After running cookiecutter, a new directory with the provided `bot_name` name will be created on your current directory, containing two files: `docker-compose.yaml`, so you can run `docker-compose up` from that directory; and `docker_command.sh`, which you can run using `bash docker_command.sh`, whichever you choose.

If you don't have python installed or you don't want to use cookiecutter, there is a [Docker image](https://github.com/Nachichuri/striker-bot/pkgs/container/striker-bot) you can pull and use however you want. Here's an example of how you could run it:

```bash
docker run -it \
	-e BOT_API_TOKEN="1234567890:ABCDeFGhIJKLMNOPQrSTuVwXyZ1234567890" \
	-e DB_NAME="strikes.db" \
	-e ALLOWED_GROUPS="12345,67890,246810" \
	-e THRESHOLD=3 \
	-v /opt/striker-bot:/bot/db \
	ghcr.io/nachichuri/striker-bot:latest \
	python /bot/main.py
```

### Using my computer 💻

If you have python installed, you can just clone this repo and run `python main.py` to start the bot.

There is a caveat though, the bot is going to look for some environment variables you're going to need to `export` or otherwise it won't work:

- `BOT_API_TOKEN`: the API token the Bot Father sent you.
- `DB_NAME`: the name of the SQLite database you'll persist the strikes in.
- `ALLOWED_GROUPS`: comma-separated values of user and/or group IDs that the bot will answer to.
- `THRESHOLD` (opt): number of strikes required to add a new pastry to the pastries counter (defaults to 3 if not set).

## How does it work? 🤔

`striker-bot` is built with `python` 🐍, uses the `python-telegram-bot` library, and `SQLite` 📙 to store the users and their status (strikes and pastries owed).

## I have a killer idea for `striker-bot`! 💡

You can either [open an issue](https://github.com/Nachichuri/striker-bot/issues/new) and we can chat there, or just [fork, branch and send your pull request](https://github.com/firstcontributions/first-contributions).
