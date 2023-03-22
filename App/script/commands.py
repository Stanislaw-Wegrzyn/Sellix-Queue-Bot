import discord

from imports import *
from objects import *


# ADD TO QUEUE
@slash.slash(
    name="add_to_queue",
    description="Buy claims and queue position with yours credits!",
    guild_ids=[Config().guild_id()],
    options=[
        create_option(
            name="token",
            description="Token for nitro sniper.",
            option_type=3,
            required=True
        ),
        create_option(
            name="amount",
            description="How much nitro should be claimed for this token?",
            option_type=4,
            required=True
        )
    ]
)
async def add_to_queue(ctx: SlashContext, token: str, amount: int):
    token_obj = Token(token)
    token = token.replace('"', '')

    if amount <= 0:
        await ctx.reply(hidden=True, embed=discord.Embed(
            description='Nice try, amount needs to be higher then 0!',
            colour=discord.Colour.red()))
        return

    if token_obj.token_correctness_code != 0:
        await ctx.reply(hidden=True, embed=token_obj.token_correctness_embed)
        return

    if ctx.author_id == Config().config_gn['admin_id']:
        correct = True
    else:
        bank_obj = Bank()

        del_code = bank_obj.delete_amount_from_user(ctx.author_id, amount)
        if del_code == 1:
            await ctx.reply(hidden=True, embed=discord.Embed(
                description='You do not have any credits!!!',
                colour=discord.Colour.red()))
            return
        elif del_code == 2:
            await ctx.reply(hidden=True, embed=discord.Embed(
                description='You do not have enough credits!',
                colour=discord.Colour.red()))
            return
        correct = True
    if correct:
        order_id = Queue().add(token, amount, ctx.author_id)
        await ctx.reply(hidden=True, embed=discord.Embed(title='Successfully added to queue!',
                                            description=f'Your token has been added to queue (``{amount}`` claims)!\n'
                                                        f'Order id: ``{order_id}``.',
                                            colour=discord.Colour.green()))


# REMOVE FROM QUEUE
@slash.slash(
    name="remove_from_queue",
    description="Removing specified order from queue [admin only]",
    guild_ids=[Config().guild_id()],
    options=[
        create_option(
            name="order_id",
            description="What order should be removed?",
            option_type=3,
            required=True
        )
    ]
)
async def change_token(ctx: SlashContext, order_id: str):
    if ctx.author_id != Config().config_gn['admin_id']: return
    code = Queue().remove(order_id)

    if code == 0:
        await ctx.reply(hidden=True, embed=discord.Embed(title=f'Order ``{order_id}`` has been removed successfully!',
                                                         colour=discord.Colour.green()))
    elif code == 1:
        await ctx.reply(hidden=True, embed=discord.Embed(title=f'Order ``{order_id}`` does not exist!',
                                                         colour=discord.Colour.red()))


# CHANGE TOKEN
@slash.slash(
    name="change_token",
    description="Add user to sniper queue [admin only]",
    guild_ids=[Config().guild_id()],
    options=[
        create_option(
            name="order_id",
            description="In what order token should be changed?",
            option_type=3,
            required=True
        ),
        create_option(
            name="token",
            description="Token for nitro sniper.",
            option_type=3,
            required=True
        ),
        create_option(
            name="sudo",
            description="Change token without checking it?",
            option_type=5,
            required=True
        )
    ]
)
async def change_token(ctx: SlashContext, order_id: str, token: str, sudo: bool):
    if ctx.author_id != Config().config_gn['admin_id']: return
    if not sudo:
        token_obj = Token(token)
        token = token.replace('"', '')

        if token_obj.token_correctness_code != 0:
            await ctx.reply(hidden=True, embed=token_obj.token_correctness_embed)
            return

    code = Queue().change_token(order_id, token)
    if code == 1:
        await ctx.reply(hidden=True, embed=discord.Embed(
            description=f'Order id ``{order_id}`` does not exist!!',
            colour=discord.Colour.red()))
    else:
        await ctx.reply(hidden=True, embed=discord.Embed(
            description=f'Token in order ``{order_id}`` has been change to ``{token[-5:]}`` (last 5)!',
            colour=discord.Colour.green()))


# RERUN SNIPERS
@slash.slash(
    name="rerun_snipers",
    description="Rerun all velocitysnipers. [admin only]",
    guild_ids=[Config().guild_id()]
)
async def rerun_snipers(ctx: SlashContext):
    if ctx.author_id != Config().config_gn['admin_id']: return
    await ctx.reply(hidden=True, embed=discord.Embed(title='Rerunning in process...',
                                                        colour=discord.Colour.gold()))
    await Queue().safe_rerun_velocity(claimed=False)
    await ctx.reply(hidden=True, embed=discord.Embed(title='Velocitysnipers has been reruned successfully!',
                                                 colour=discord.Colour.green()))


# BUY CREDITS
@slash.slash(
    name="buy",
    description="Purchase credits to used them for buying nitro claims!",
    guild_ids=[Config().guild_id()],
    options=[
        create_option(
            name="amount",
            description="How much credits you want to buy?",
            option_type=4,
            required=True
        )
    ]
)
async def buy(ctx: SlashContext, amount: int):
    sellix_client = Sellix(Config().config_se['api_key'], Config().config_se['merchant_name'])
    config = Config().config_se
    if amount <= 0:
        await ctx.reply(hidden=True, embed=discord.Embed(
            description='Nice try, amount needs to be higher then 0!',
            colour=discord.Colour.red()))
        return
    reply_mess = await ctx.reply(hidden=True, embed=discord.Embed(
        title='In process...', colour=discord.Colour.gold()))
    try:
        payment = sellix_client.create_payment(
            title="Nitro Claims",
            value=float(config['price_per_credit']),
            currency="USD",
            quantity=amount,
            white_label=False,
            email="there_is_no@mail.XD",
            return_url=config["return_url"]
        )
        uniqid = Payment().creat_payment(ctx.author_id, dict(payment)['uniqid'])
        await ctx.reply(hidden=True, embed=discord.Embed(
            description='Click link below to pay with sellix api!\n'
                        f'{dict(payment)["url"]}\n'
                        f'Your payment id: ``{uniqid}``\n'
                        f'When payment will be approved you will get dm message from me!',
            colour=Config().embed_color()
        ))
    except Sellix.SellixException as e:
        print(e)
        await reply_mess.edit(
            embed=discord.Embed(title='!Sellix ERROR!', description=str(e), colour=discord.Colour.red()))
        return


# TEST VS EMBED
@slash.slash(
    name="test_vs_emebd",
    description="[admin only]",
    guild_ids=[Config().guild_id()],
    options=[
        create_option(
            name="classic",
            description="If true Classic nitro will be claimed.",
            option_type=5,
            required=True
        )
    ]
)
async def test_vs_emebd(ctx: SlashContext, classic: bool):
    if ctx.author_id != Config().config_gn['admin_id']: return
    embed = discord.Embed(title='Sniped Nitro!')
    embed.set_author(name='Velocity')
    if classic:
        embed.add_field(name='type', value='`Nitro Classic Monthly`')
    else:
        embed.add_field(name='type', value='`Nitro Monthly`')
    embed.add_field(name='delay', value='`0.245829s`')
    embed.add_field(name='Guild', value='`0.୫ /dhc`')
    embed.add_field(name='Author', value='`linz#0007`')
    embed.add_field(name='Code', value='`BKJuANe3MKWG74hu`')
    embed.add_field(name='Token Ending', value='`bOJZ0`')
    embed.add_field(name='Sniper', value='`AFFICIATE#6168`')
    embed.set_footer(text='Velocity • Dziś o 16:30')

    await ctx.send(embed=embed)


# ORDER INFO
@slash.slash(
    name="order_info",
    description="Shows everything about order with specified id.",
    guild_ids=[Config().guild_id()],
    options=[
        create_option(
            name="order_id",
            description="About what order you want to get info?",
            option_type=3,
            required=True
        )
    ]
)
async def rerun_snipers(ctx: SlashContext, order_id: str):
    try:
        queue = Queue().data()
        order = queue[order_id]
        position = list(queue.keys()).index(order_id) + 1
        embed = discord.Embed(
            title=f'Order ``{order_id}``:',
            description= \
                f'> position: ``{position}``\n'
                f'> user: ``{client.get_user(order["id"])}``  (``{order["id"]}``)\n'
                f'> token (last 5): ``{order["token"][-5:]}``\n'
                f'> nitro claimed: ``{order["nitro_claimed"]}``\n'
                f'> nitro bought: ``{order["nitro_bought"]}``',
            colour=Config().embed_color())
    except KeyError:
        embed = discord.Embed(title='This order id do not exist!', colour=discord.Colour.red())

    await ctx.reply(hidden=True, embed=embed)


# GIVE CREDITS
@slash.slash(
    name="give_credits",
    description="Gives someone custom amount of credits [admin only]",
    guild_ids=[Config().guild_id()],
    options=[
        create_option(
            name="user",
            description="To how you want to give credits?",
            option_type=6,
            required=True
        ),
        create_option(
            name="amount",
            description="How much amount you want to give?",
            option_type=4,
            required=True
        )
    ]
)
async def give_credits(ctx: SlashContext, user, amount: int):
    if ctx.author_id != Config().config_gn['admin_id']: return
    if amount <= 0:
        await ctx.reply(hidden=True, embed=discord.Embed(
            description='Nice try, amount needs to be higher then 0!',
            colour=discord.Colour.red()))
        return
    user = user.id
    Bank().add_to_bank(user_id=user, amount=amount)

    await ctx.reply(hidden=True, embed=discord.Embed(
        description=f'Successfully added ``{amount}`` credit(s) to user <@{user}>',
        colour=discord.Colour.green()))


# DELETE CREDITS
@slash.slash(
    name="delete_credits",
    description="Delete from someone custom amount of credits [admin only]",
    guild_ids=[Config().guild_id()],
    options=[
        create_option(
            name="user",
            description="From how you want to delete credits?",
            option_type=6,
            required=True
        ),
        create_option(
            name="amount",
            description="How much amount you want to delete?",
            option_type=4,
            required=True
        )
    ]
)
async def delete_credits(ctx: SlashContext, user: discord.Member, amount: int):
    if ctx.author_id != Config().config_gn['admin_id']: return
    if amount <= 0:
        await ctx.reply(hidden=True, embed=discord.Embed(
            description='Nice try, amount needs to be higher then 0!',
            colour=discord.Colour.red()))
        return
    user = user.id
    bank_obj = Bank()

    del_code = bank_obj.delete_amount_from_user(user, amount)
    if del_code == 1:
        await ctx.reply(hidden=True, embed=discord.Embed(
            description=f'<@{user}> do not have any credits!',
            colour=discord.Colour.red()))
        return
    elif del_code == 2:
        amount = 'all'
        bank_obj.delete_user(user)

    await ctx.reply(hidden=True, embed=discord.Embed(
        description=f'Successfully deleted ``{amount}`` credit(s) from user <@{user}>',
        colour=discord.Colour.green()))


# GET YOUR TOKEN
@slash.slash(
    name="get_your_token",
    description="Get your token by discord qr code!",
    guild_ids=[Config().guild_id()]
)
async def get_your_token(ctx: SlashContext):
    c = RemoteAuthClient()

    @c.event("on_fingerprint")
    async def on_fingerprint(data):
        embed = discord.Embed(title='Scan me!', colour=Config().embed_color())
        embed.set_image(url=f'https://api.qrserver.com/v1/create-qr-code/?size=256x256&data={data}')
        await ctx.reply(hidden=True, embed=embed)

    @c.event("on_token")
    async def on_token(token):
        await ctx.reply(hidden=True, embed=discord.Embed(title='Your token:', description=f'```{token}```',
                                                        colour=Config().embed_color()))

    @c.event("on_userdata")
    async def on_userdata(user):
        None

    @c.event("on_cancel")
    async def on_cancel():
        await ctx.reply(hidden=True, embed=discord.Embed(title=f"Auth canceled!", colour=discord.Colour.red()))

    @c.event("on_timeout")
    async def on_timeout():
        await ctx.reply(hidden=True, embed=discord.Embed(title=f"Timeout", colour=discord.Colour.red()))

    await c.run()


# STATS
@slash.slash(
    name="stats",
    description="Shows velocitysniper stats",
    guild_ids=[Config().guild_id()]
)
async def change_token(ctx: SlashContext):
    config = Config().config_vs

    await ctx.reply(hidden=True, embed=discord.Embed(title="Collecting data...", colour=discord.Colour.gold()))

    stats = {"total_servers": 0, "alts": 0}

    for api in config['api_links']:
        with requests.request('GET', api, headers={'content-type': 'application/json'}) as response:
            stats["total_servers"] += response.json()["total_servers"]
            stats["alts"] += response.json()["alts"]

    embed = discord.Embed(title='Stats: ',
                          description=f'> Total servers: {stats["total_servers"]}\n\n'
                                      f'> Alts: {stats["alts"]}',
                          colour=Config().embed_color())

    await ctx.reply(hidden=True, embed=embed)


# QUEUE DETAILS
@slash.slash(
    name="queue_details",
    description="Shows queue embed with all details about order",
    guild_ids=[Config().guild_id()]
)
async def queue_details(ctx: SlashContext):
    await ctx.reply(hidden=True, embed=Queue().details_embed())


