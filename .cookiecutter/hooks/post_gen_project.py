import os

print(
    "\n     _        _ _               _           _   \n"
    "    | |      (_) |             | |         | |  \n"
    " ___| |_ _ __ _| | _____ _ __  | |__   ___ | |_ \n"
    "/ __| __| '__| | |/ / _ \ '__| | '_ \ / _ \| __|\n"
    "\__ \ |_| |  | |   <  __/ |    | |_) | (_) | |_ \n"
    "|___/\__|_|  |_|_|\_\___|_|    |_.__/ \___/ \__|\n\n"
    'A folder named "{{cookiecutter.bot_name}}" has been created in your current working directory.\n'
    "\nIt contains a docker-compose file to run compose from there, or you can also \n"
    'use the command provided in the "docker_command.sh" file too.\n'
    "\nIf you want to run it now, you can run:\n"
    "\ndocker run -it \\"
    '\n\t-e BOT_API_TOKEN="{{ cookiecutter.bot_api_token }}" \\'
    '\n\t-e DB_NAME="{{ cookiecutter.database_name }}.db" \\'
    '\n\t-e ALLOWED_GROUPS="{{ cookiecutter.allowed_groups }}" \\'
    "\n\t-e THRESHOLD={{ cookiecutter.threshold }} \\"
    "\n\t-v {{ cookiecutter.database_persistance_location }}:/app \\"
    "\n\tghcr.io/nachichuri/striker-bot:latest \\"
    "\n\tpython /bot/main.py"
)
