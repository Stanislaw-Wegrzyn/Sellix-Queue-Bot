import discord
import discord_slash.context

from imports import *
from objects import *
from commands import *

decoded_data = open('../../config.json', 'r').read().encode().decode('utf-8-sig')
open('../../config.json', 'w').write(decoded_data)

DiscordComponents(client)


@tasks.loop(count=1)
async def wait_until_ready():
    if client.is_ready(): return
    await client.wait_until_ready()
    
    Logo()

@client.event
async def on_message(message):
    config_vs = Config().config_vs
    config_gn = Config().config_gn
    config_se = Config().config_se
    config_cp = Config().config_cp

    if message.channel.id == config_vs['velocity_logs_channel_id'] and message.author.id != config_gn['admin_id']:
        failed_claim_message_pattern = ":no: Attempted to claim code in `<DELAY>` | `<TYPE>`"
        success_claim_message_pattern = " <EMOJI> Successfully Claimed `<TYPE>` in `<DELAY>` <PING>!"
        time.sleep(0.5)
        embed = message.embeds[0]
        emb_dict = embed.to_dict()
        if emb_dict["title"] == "Failed Snipe!" or emb_dict["title"] == "Failed Snipe! (smart)":
            success = False
        elif emb_dict["title"] == "Sniped Nitro!" or emb_dict["title"] == "Sniped Nitro! (smart)":
            success = True
        else:
            return
        channel = client.get_channel(config_vs['claims_channel_id'])
        if success is False:
            None
        if success is True:
            delay = emb_dict["fields"][1]["value"]
            type = emb_dict["fields"][0]["value"]

            if 'Classic' in type:
                emoji = config_vs['classic_claim_emoji']
            else:
                emoji = config_vs['boost_claim_emoji']

            success_message = await channel.send(
                success_claim_message_pattern.replace("<DELAY>", delay).replace("<TYPE>", type).replace("<EMOJI>", emoji).replace("<PING>", f"<@&{config_cp['claims_ping_role_id']}>"))
            await success_message.add_reaction('🎉')

            await Queue().safe_rerun_velocity(claimed=True)

    elif message.channel.id == config_se['sellix_logs_channel_id']:
        event = message.content.split('event: ')[1].split('\n')[0]
        payment_obj = Payment()
        warnings_channel = client.get_channel(Config().config_gn['warnings_channel_id'])
        if event == 'order:paid':
            unigid = message.content.split('uniqid: ')[1].split('\n')[0]
            amount = message.content.split('amount: ')[1].split('\n')[0]
            try:
                user_id = payment_obj.data()[unigid]

                if client.get_user(user_id) is not None:
                    try:
                        invalid_token_dm = await client.get_user(user_id).create_dm()
                        await invalid_token_dm.send(embed=discord.Embed(
                            title='Your payment has been approved!',
                            description=f'Congratulations your payment ``{unigid}`` has been approved by sellix!\n'
                                        f'To your bank has been added ``{amount}`` credits! Have fun!',
                            colour=discord.Colour.green()
                        ))
                        customer_role = client.get_guild(Config().guild_id()).get_role(Config().config_gn['customer_role_id'])
                        await client.get_guild(Config().guild_id()).get_member(user_id).add_roles(customer_role)
                    except discord.errors.Forbidden:
                        await warnings_channel.send(embed=discord.Embed(colour=discord.Colour.gold(), description=
                            f"{client.get_user(user_id)}'s payment ``{unigid}`` has been approved by sellix but cannot send dm to user (error 401)."))
                else:
                    await warnings_channel.send(embed=discord.Embed(colour=discord.Colour.gold(), description=
                        f"Payment ``{unigid}`` belong to user with id: ``{user_id}`` has been approved by sellix but cannot send dm to user (user left from server)."))

                Leaderboard().add_to_leaderboard(user_id, int(amount))
                payment_obj.accept_payment(unigid, int(amount))
            except KeyError:
                None
        elif event == 'order:cancelled':
            unigid = message.content.split('uniqid: ')[1].split('\n')[0]
            amount = message.content.split('amount: ')[1].split('\n')[0]
            try:
                user_id = payment_obj.data()[unigid]

                if client.get_user(user_id) is not None:
                    try:
                        invalid_token_dm = await client.get_user(user_id).create_dm()
                        await invalid_token_dm.send(embed=discord.Embed(
                            title='Your payment has been canceled!',
                            description=f'Attention! Your payment ``{unigid}`` has been canceled by sellix!\n'
                                        f'Therefore, your ``{amount}`` credit(s) will not be added to your bank!',
                            colour=discord.Colour.red()
                        ))

                    except discord.errors.Forbidden:
                        await warnings_channel.send(
                            f"{client.get_user(user_id)}'s payment ``{unigid}`` has been canceled by sellix but cannot send dm to user (error 401).")
                else:
                    await warnings_channel.send(
                        f"Payment ``{unigid}`` belong to user with id: {user_id} has been canceled by sellix but cannot send dm to user (user left from server).")

                payment_obj.delete_payment(unigid)
            except KeyError:
                None


@tasks.loop(seconds=10)
async def _updating():
    if not client.is_ready(): return
    Queue()
    Bank()
    Leaderboard()
    ReactionRole()


@client.event
async def on_button_click(interaction):
    if interaction.custom_id == 'claim_ping_reaction_role':
        await interaction.respond(type=6)
        await ReactionRole().get_role(interaction.author.id)


# CLIENT RUNNING
wait_until_ready.start()
# SITE TASKS
_updating.start()

client.run(Config().token())
