# PlaytimeStalkerBot
PlaytimeStalkerBot is a Discord bot that stalks the total playtime and the average daily time that someone spent in a video game. This bot gather data from [Exophase's](https://exophase.com) API, which may be inaccurate.

![Imgur](https://imgur.com/Aex0ITD.jpg)

# Installing
Clone this repository, replace your bot token in the file `src/.TOKEN` and run the `main.py`. For tutorials on how to integrate a discord bot to a server, [Google](https://google.com) or follow [Discord's documentation](https://discord.com/developers/docs/intro).

# Usage
* `!hello` - displays a `Hello World!` message.
* `!commands` - displays the list of commands of the bot.
* `!find gamename` - searches for the name of a game in exophase's database.
* `!set gamename` - sets the current game that the bot will be using to stalk.
* `!stalk player alt alt2 ...` - stalks the player's playtime and his alt accounts. Alt accounts are optinal.
