from imports import *
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(client, sync_commands=True)