#!/bin/bash

docker run -it \
    -e BOT_API_TOKEN="{{ cookiecutter.bot_api_token }}" \
    -e DB_NAME="{{ cookiecutter.database_name }}.db" \
    -e ALLOWED_GROUPS="{{ cookiecutter.allowed_groups }}"\
    -e THRESHOLD={{ cookiecutter.threshold }} \
    -v {{ cookiecutter.database_persistance_location }}:/bot/db \
    ghcr.io/nachichuri/striker-bot:latest \
    python /bot/main.py