from http import client
import discord

from imports import *
from client import *


class Logo:
    def __init__(self):
        print(
            "                                                                                                          \n"
            "                                                                                                          \n"
            "                                                                                                          \n"
            "                                                               .--.,                                      \n"
            "                               .--.         ,--,             ,--.'  \   ,---.    __  ,-.                  \n"
            "                             .--,`|       ,'_ /|   .--.--.   |  | /\/  '   ,'\ ,' ,'/ /|                  \n"
            "                             |  |.   .--. |  | :  /  /    '  :  : :   /   /   |'  | |' |                  \n"
            "                             '--`_ ,'_ /| :  . | |  :  /`./  :  | |-,.   ; ,. :|  |   ,'                  \n"
            "                             ,--,'||  ' | |  . . |  :  ;_    |  : :/|'   | |: :'  :  /                    \n"
            "                             |  | '|  | ' |  | |  \  \    `. |  |  .''   | .; :|  | '                     \n"
            "         ___         ___     :  | |:  | : ;  ; |   `----.   \\'  : '  |   :    |;  : |     ___         ___ \n"
            "      .'  .`|     .'  .`|  __|  : ''  :  `--'   \ /  /`--'  /|  | |   \   \  / |  , ;  .'  .`|     .'  .`|\n"
            "   .'  .'   :  .'  .'   :.'__/\_: |:  ,      .-./'--'.     / |  : \    `----'   ---'.'  .'   :  .'  .'   :\n"
            ",---, '   .',---, '   .' |   :    : `--`----'      `--'---'  |  |,'              ,---, '   .',---, '   .' \n"
            ";   |  .'   ;   |  .'     \   \  /                           `--'                ;   |  .'   ;   |  .'    \n"
            "`---'       `---'          `--`-'                                                `---'       `---'        \n"
        )

        print(
            f'{Fore.LIGHTRED_EX}'
            f'                              +----------------------------------------------+\n'
            f'                              |    {Fore.CYAN}Script has been written by: __jusfor__{Fore.LIGHTRED_EX}    |\n'
            f'                              +----------------------------------------------+\n'
            f'                              |  {Fore.CYAN}cracked.io: https://cracked.io/jusfor{Fore.LIGHTRED_EX}       |\n'
            f'                              |  {Fore.CYAN}telegram: https://t.me/jusfor5{Fore.LIGHTRED_EX}              |\n'
            f'                              +----------------------------------------------+\n\n\n{Style.RESET_ALL}'
            f'{Fore.RED}Bot logged in as: {Style.RESET_ALL}{client.user}'
        )


class Config:
    def __init__(self):
        self.config = json.load(open('../../config.json'))
        self.config_gn = self.config['general']
        self.config_vs = self.config['velocitysniper']
        self.config_q = self.config['queue']
        self.config_se = self.config['sellix']
        self.config_b = self.config['bank']
        self.config_cp = self.config['claim_ping_reaction_role']

    def data(self):
        return json.load(open('../../config.json'))

    def token(self):
        return self.config_gn['token']

    def guild_id(self):
        return self.config_gn['guild_id']

    def embed_color(self):
        color = self.config_gn['embeds_color']

        return discord.Colour.from_rgb(color['r'], color['g'], color['b'])


class Queue:
    def __init__(self):
        self.init_queue.start()

    @tasks.loop(count=1)
    async def init_queue(self):
        config = Config().config_q
        config_vs = Config().config_vs

        queue_channel_history = await client.get_channel(config['queue_channel_id']).history(limit=1).flatten()

        queue_embed = await self.embed_msg()

        if len(queue_channel_history) == 0:
            await client.get_channel(config['queue_channel_id']).send(embed=queue_embed)
        else:
            await queue_channel_history[0].edit(embed=queue_embed)

        total_claims_channel_history = await client.get_channel(config_vs['total_claims_stats_channel_id']).history(limit=1).flatten()

        total_claims_embed = self.total_claims_embed_msg()

        if len(total_claims_channel_history) == 0:
            await client.get_channel(config_vs['total_claims_stats_channel_id']).send(embed=total_claims_embed)
        else:
            await total_claims_channel_history[0].edit(embed=total_claims_embed)

    def data(self):
        return json.load(open('../config/queue.json'))

    def overwrite(self, queue: dict):
        with open('../config/queue.json', "w") as output_db:
            output_db.write(json.dumps(queue, indent=len(queue)))
            output_db.close()

    def current_order_id(self):
        current_orders = list()
        for order_id, order in self.data().items():
            if order['status'] == 'current':
                current_orders.append(order_id)

        return current_orders

    def get_orders_ids_choices(self):
        choices_list_orders_ids = list()
        for order_id_choice in self.data().keys():
            choices_list_orders_ids.append(create_choice(name=order_id_choice, value=order_id_choice))
        return choices_list_orders_ids

    def generate_order_id(self):
        queue = self.data()

        if len(list(queue.keys())) == 0:
            order_nr = '0'
        else:
            order_nr = str(int(list(queue.keys())[len(list(queue.keys())) - 1][5:9]) + 1)

        if len(order_nr) == 1:
            order_nr = '000' + order_nr
        elif len(order_nr) == 2:
            order_nr = '00' + order_nr
        elif len(order_nr) == 3:
            order_nr = '0' + order_nr

        random_nr0 = str(random.randint(1000, 10000))
        random_nr1 = str(random.randint(1000, 10000))

        order_id = f'{random_nr0}-{order_nr}-{random_nr1}'

        return order_id

    def add(self, token, amount, user_id):
        queue = self.data()
        order_id = self.generate_order_id()
        queue.update(
            {
                order_id:
                    {
                        'token': token,
                        'username': str(client.get_user(int(user_id))),
                        'id': int(user_id),
                        'nitro_bought': amount,
                        'nitro_claimed': 0,
                        'status': 'waiting'
                    }
            }
        )

        self.overwrite(queue)

        return order_id

    def remove(self, order_id):
        queue = self.data()
        try:
            del queue[order_id]
            self.overwrite(queue)
            return 0
        except KeyError:
            return 1

    def get_total_claims(self):
        total_claims = int(open('../config/total.claims').read())
        return total_claims

    def add_one_to_total_claims(self):
        total_claims = self.get_total_claims()

        f = open('../config/total.claims', 'w')
        f.write(str(total_claims + 1))
        f.close()

    def change_token(self, order_id, token):
        queue = self.data()
        try:
            queue[order_id]['token'] = token
            self.overwrite(queue)
            return 0
        except KeyError:
            return 1

    async def invalid_token_in_queue(self, order_id):
        invalid_usr_id = self.data()[order_id]['id']
        warnings_channel = client.get_channel(Config().config_gn['warnings_channel_id'])

        queue = self.data()
        queue[order_id]['status'] = 'suspended'
        self.overwrite(queue)

        embed = discord.Embed(
            title=f'Your token is invalid!',
            description=
            f'Hello there, your token in queue is invalid and needs replacement. \n'
            f'Please, send your token to this dm conversation to replace it!\n'
            f'Until you send your valid token your order will be suspended!',
            colour=discord.Colour.red())
        invalid_usr_id = int(invalid_usr_id)
        if client.get_user(invalid_usr_id) is not None:
            try:
                invalid_token_dm = await client.get_user(invalid_usr_id).create_dm()
                await invalid_token_dm.send(embed=embed)

                def _check_respond(m):
                    return m.channel.id == invalid_token_dm.id and m.author.id == invalid_usr_id

                @tasks.loop(count=1)
                async def typing_new_token():
                    not_correct = True

                    while not_correct:
                        new_token = await client.wait_for('message', check=_check_respond)
                        new_token = new_token.content.replace('"', '')

                        new_token_obj = Token(new_token)

                        if new_token_obj.token_correctness_code != 0:
                            embed = new_token_obj.token_correctness_embed
                            embed.description += '\nPlease try again!'
                            await invalid_token_dm.send(embed=embed)
                        else:
                            queue = self.data()
                            queue[order_id]['token'] = new_token
                            queue[order_id]['status'] = 'waiting'
                            self.overwrite(queue)
                            await invalid_token_dm.send(embed=discord.Embed(
                                title='Token approved!',
                                description='Your order has been actualized and resumed!',
                                colour=discord.Colour.green()))

                typing_new_token.start()
                await self.safe_rerun_velocity(False)

            except discord.errors.Forbidden:
                await warnings_channel.send(embed=discord.Embed(colour=discord.Colour.gold(), description=
                    f"{client.get_user(invalid_usr_id)}'s token is invalid but cannot send dm to user (error 401)."))
        else:
            await warnings_channel.send(embed=discord.Embed(colour=discord.Colour.gold(), description=
                f"Token belong to user with id: ``{invalid_usr_id}`` is invalid but cannot send dm to user (user left from server)."))

    def zero_in_queue(self):
        queue = self.data()

        for order_id in queue:
            if queue[order_id]['nitro_claimed'] == 0 and queue[order_id]['status'] != 'suspended':
                str_next_order = order_id
                next_order = queue[order_id]
                return str_next_order, next_order
        return None

    async def safe_rerun_velocity(self, claimed: bool):
        queue = self.data()
        config = Config().config_q
        warnings_channel = client.get_channel(Config().config_gn['warnings_channel_id'])

        if claimed:
            self.add_one_to_total_claims()
            id_done_order = self.current_order_id()[0]
            queue[id_done_order]['nitro_claimed'] += 1

            self.overwrite(queue)

            done_order = queue[id_done_order]

            if done_order['nitro_claimed'] != done_order['nitro_bought']:
                try:
                    queue[self.current_order_id()[0]]['status'] = 'waiting'
                except IndexError:
                    None
                try:
                    now_index = list(queue.keys()).index(id_done_order)
                    queue[list(queue.keys())[now_index + 1]]['status'] = 'current'
                except IndexError:
                    try:
                        queue[list(queue.keys())[0]]['status'] = 'current'
                    except IndexError:
                        await warnings_channel.send(content=f'<@${Config().guild_id()}>', embed=discord.Embed(
                            title='Queue is empty!!!',
                            colour=discord.Colour.red()
                        ))
                        for host in config['hosts']:
                            stop_sniper(host, config['hosts_username'], config['hosts_password'])
                        return

            elif done_order['nitro_claimed'] >= done_order['nitro_bought']:
                embed = discord.Embed(
                    title=f'Your order has been done!',
                    description=
                    f'Hello there, Your order with id: ``{id_done_order}`` has been fulfilled!\n'
                    f'Have fun with nitro and we hope you will come back to us!',
                    colour=discord.Colour.green())

                if client.get_user(done_order['id']) is not None:
                    try:
                        done_order_dm = await client.get_user(done_order['id']).create_dm()
                        await done_order_dm.send(embed=embed)
                    except discord.errors.Forbidden:
                        await warnings_channel.send(embed=discord.Embed(colour=discord.Colour.gold(), description=
                            f"{client.get_user(done_order['id'])}'s order has been completed but cannot send dm to user (error 401)."))
                else:
                    await warnings_channel.send(embed=discord.Embed(colour=discord.Colour.gold(), description=
                        f"Order belong to user with id: ``{done_order['id']}`` has been completed but cannot send dm to user (user left from server)."))

                if len(queue.keys()) == 0:
                    await warnings_channel.send(content=f'<@${Config().guild_id()}>', embed=discord.Embed(
                        title='Queue is empty!!!',
                        colour=discord.Colour.red()
                    ))
                    for host in config['hosts']:
                        stop_sniper(host, config['hosts_username'], config['hosts_password'])
                    return
                else:
                    try:
                        now_index = list(queue.keys()).index(id_done_order)
                        queue[list(queue.keys())[now_index + 1]]['status'] = 'current'
                    except IndexError:
                        queue[list(queue.keys())[0]]['status'] = 'current'
                del queue[id_done_order]
            self.overwrite(queue)
        else:
            for i in range(list(queue.keys()).index(self.current_order_id()[0]) + 1):
                if queue[list(queue.keys())[i]]['status'] != 'suspended':
                    try:
                        queue[self.current_order_id()[0]]['status'] = 'waiting'
                    except IndexError:
                        None
                    queue[list(queue.keys())[i]]['status'] = 'current'
                    break
            self.overwrite(queue)

        next_token = queue[self.current_order_id()[0]]['token']
        next_token_obj = Token(next_token)

        if next_token_obj.token_correctness_code != 0:
            await self.invalid_token_in_queue(self.current_order_id()[0])

        for host in config['hosts']:
            rerun_sniper(host, config['hosts_username'], config['hosts_password'], next_token)

    async def embed_msg(self):
        queue = self.data()

        config = Config().config_q

        suspended_orders_ids = []

        waiting_order_id = ""

        content = str()
        for order_id, order in queue.items():
            if order['status'] == 'current':
                content += f'> {order["username"]} ``{order["nitro_claimed"]}``**/**``{order["nitro_bought"]}`` '
                content += str(config['current_order_emoji']) + '\n'
                current_index = list(queue.keys()).index(order_id)
                try:
                    waiting_order_id = list(queue.keys())[current_index + 1]
                except IndexError:
                    content = content.split('\n')
                    content[0] += ' ' + str(config['waiting_order_emoji'])
                    content = '\n'.join(content)
            elif order_id == waiting_order_id:
                content += f'> {order["username"]} ``{order["nitro_claimed"]}``**/**``{order["nitro_bought"]}`` '
                content += str(config['waiting_order_emoji']) + '\n'
            elif order['status'] == 'suspended':
                suspended_orders_ids.append(order_id)
            else:
                content += f'> {order["username"]} ``{order["nitro_claimed"]}``**/**``{order["nitro_bought"]}``\n'

        content += '\n**Suspended Orders:**\n'
        for order_id in suspended_orders_ids:
            order = queue[order_id]
            content += f'> {order["username"]} ``{order["nitro_claimed"]}``**/**``{order["nitro_bought"]}`` \n'

        embed = discord.Embed(title='Queue: ', description=f'{content}', colour=Config().embed_color())

        return embed

    def details_embed(self):
        queue = self.data()

        config = Config().config_q

        suspended_orders_ids = []

        waiting_order_id = ""

        content = str()
        for order_id, order in queue.items():
            if order['status'] == 'current':
                content += f'> {order["username"]} **|** ``{order["nitro_claimed"]}``**/**``{order["nitro_bought"]}`` **|** token: ``{order["token"][-5:]}`` **|** order id: ``{order_id}`` '
                content += str(config['current_order_emoji']) + '\n'
                current_index = list(queue.keys()).index(order_id)
                try:
                    waiting_order_id = list(queue.keys())[current_index + 1]
                except IndexError:
                    content = content.split('\n')
                    content[0] += ' ' + str(config['waiting_order_emoji'])
                    content = '\n'.join(content)
            elif order_id == waiting_order_id:
                content += f'> {order["username"]} **|** ``{order["nitro_claimed"]}``**/**``{order["nitro_bought"]}`` **|** token: ``{order["token"][-5:]}`` **|** order id: ``{order_id}`` '
                content += str(config['waiting_order_emoji']) + '\n'
            elif order['status'] == 'suspended':
                suspended_orders_ids.append(order_id)
            else:
                content += f'> {order["username"]} **|** ``{order["nitro_claimed"]}``**/**``{order["nitro_bought"]}`` **|** token: ``{order["token"][-5:]}`` **|** order id: ``{order_id}`` \n'

        content += '\n**Suspended Orders:**\n'
        for order_id in suspended_orders_ids:
            order = queue[order_id]
            content += f'> {order["username"]} **|** ``{order["nitro_claimed"]}``**/**``{order["nitro_bought"]}`` **|** token: ``{order["token"][-5:]}`` **|** order id: ``{order_id}`` \n'

        embed = discord.Embed(title='Details queue: ', description=f'{content}', colour=Config().embed_color())

        return embed

    def total_claims_embed_msg(self):
        embed = discord.Embed(title='Total Snipes', description=f'In total **{Config().config_gn["your_service_name"]}** has sniped ``{self.get_total_claims()}`` nitros!',
                              colour=Config().embed_color())
        return embed


class Token:
    def __init__(self, token):
        self.token = token.replace('"', '')

        self.headers = {'Authorization': self.token, 'Content-type': 'application/json'}
        self.api = 'https://discord.com/api/v9/users/@me'

        if token[0:4] == 'mfa.':
            self.token_correctness_code = 3  # invalid token format (2fa)
            self.token_correctness_embed = discord.Embed(title='Invalid token!',
                                                         description='Token has enable 2fa!',
                                                         colour=discord.Colour.red())

        else:
            with requests.request('GET', self.api, headers=self.headers) as response:
                api_data = response.json()
                if str(api_data) == "{'message': '401: Unauthorized', 'code': 0}":
                    self.token_correctness_code = 2  # invalid token
                    self.token_correctness_embed = discord.Embed(title='Invalid Token!',
                                                                 description='Token does not exist!',
                                                                 colour=discord.Colour.red())
                elif api_data['phone'] is None:
                    self.token_correctness_code = 1  # no phone token
                    self.token_correctness_embed = discord.Embed(title='Invalid token!',
                                                                 description='Token is not verified by phone number!',
                                                                 colour=discord.Colour.red())
                else:
                    self.token_correctness_code = 0
                    self.token_correctness_embed = discord.Embed(title='Token correct!',
                                                             colour=discord.Colour.green())

    def get_info(self):
        with requests.request('GET', self.api, headers=self.headers) as response:
            api_data = response.json()
            return api_data


class Payment:
    def data(self):
        return json.load(open('../config/pending_payments.json'))

    def overwrite(self, data: dict):
        with open('../config/pending_payments.json', "w") as output_db:
            output_db.write(json.dumps(data, indent=len(data)))
            output_db.close()
        
    def creat_payment(self, user_id: int, uniqid: str):
        all_payments = self.data()
        
        all_payments.update(
            {
                uniqid: user_id
            }
        )
        
        self.overwrite(all_payments)
        return uniqid

    def delete_payment(self, uniqid: str):
        all_payments = self.data()

        try:
            del all_payments[uniqid]
        except KeyError:
            return 1

        self.overwrite(all_payments)
        return 0
    
    def accept_payment(self, uniqid: str, amount: int):
        user_id = self.data()[uniqid]
        self.delete_payment(uniqid)
        Bank().add_to_bank(user_id=user_id, amount=amount)


class Bank:
    def __init__(self):
        self.init_bank.start()

    @tasks.loop(count=1)
    async def init_bank(self):
        config = Config().config_b

        bank_channel_history = await client.get_channel(config['bank_channel_id']).history(limit=1).flatten()

        queue_embed = self.embed_msg()

        if len(bank_channel_history) == 0:
            await client.get_channel(config['bank_channel_id']).send(embed=queue_embed)
        else:
            await bank_channel_history[0].edit(embed=queue_embed)

    def data(self):
        return json.load(open('../config/bank.json'))

    def overwrite(self, bank: dict):
        with open('../config/bank.json', "w") as output_db:
            output_db.write(json.dumps(bank, indent=len(bank)))
            output_db.close()

    def add_to_bank(self, user_id: int, amount: int):
        bank = self.data()
        user_id = str(user_id)
        try:
            bank[user_id] += amount
        except KeyError:
            bank.update(
                {
                    user_id: amount
                }
            )
        self.overwrite(bank)

    def delete_user(self, user_id: int):
        bank = self.data()
        user_id = str(user_id)
        try:
            del bank[user_id]
        except KeyError:
            return 1
        self.overwrite(bank)
        return 0

    def delete_amount_from_user(self, user_id: int, amount: int):
        bank = self.data()
        user_id = str(user_id)
        try:
            bank[user_id] -= amount
            if bank[user_id] == 0:
                self.delete_user(user_id)
            elif bank[user_id] < 0:
                return 2
        except KeyError:
            return 1
        self.overwrite(bank)
        return 0

    def embed_msg(self):
        bank = self.data()

        content = str()
        for user_id, amount in bank.items():
            if amount == 0:
                None
            else:
                content += f'> **{client.get_user(int(user_id))}** ``{amount}``\n'

        embed = discord.Embed(title='Credits Bank:', description=content, colour=Config().embed_color())
        return embed


class Leaderboard:
    def __init__(self):
        self.init_leaderboard.start()

    @tasks.loop(count=1)
    async def init_leaderboard(self):
        config = Config().config_gn

        leaderboard_channel_history = await client.get_channel(config['leaderboard_channel_id']).history(limit=1).flatten()

        leaderboard_embed = self.embed_msg()

        if len(leaderboard_channel_history) == 0:
            await client.get_channel(config['leaderboard_channel_id']).send(embed=leaderboard_embed)
        else:
            await leaderboard_channel_history[0].edit(embed=leaderboard_embed)

    def data(self):
        return json.load(open('../config/leaderboard.json'))

    def overwrite(self, leaderboard: dict):
        with open('../config/leaderboard.json', "w") as output_db:
            output_db.write(json.dumps(leaderboard, indent=len(leaderboard)))
            output_db.close()

    def add_to_leaderboard(self, user_id, amount):
        leaderboard = self.data()
        user_id = str(user_id)
        try:
            leaderboard[str(user_id)]['amount'] += amount
        except KeyError:
            leaderboard.update({user_id: {"user_id": user_id, "amount": amount}})

        self.overwrite(leaderboard)

    def embed_msg(self):
        leaderboard = self.data()
        leaderboard_list = list()
        for dic in leaderboard.values():
            leaderboard_list.append(dic)

        if len(leaderboard) == 0:
            content = ''
        else:
            def sort_amount(e):
                return e['amount']

            leaderboard_list.sort(key=sort_amount)
            leaderboard_list.reverse()
            content = str()
            counter = 1
            for dic in leaderboard_list:
                if counter in [1, 2, 3]:
                    if counter == 1:
                        place = '🥇'
                    elif counter == 2:
                        place = '🥈'
                    elif counter == 3:
                        place = '🥉'
                else:
                    place = f'#{counter}'
                content += f'**{place}** {client.get_user(int(dic["user_id"]))} *({dic["amount"]})*\n'
                if counter == 10:
                    break
                counter += 1

        embed = discord.Embed(title='Leaderboard: ', description=content, colour=Config().embed_color())

        return embed


class ReactionRole:
    def __init__(self):
        self.init_reaction_role.start()

    @tasks.loop(count=1)
    async def init_reaction_role(self):
        config = Config().config_cp

        reaction_role_channel_history = await client.get_channel(config['reaction_role_channel_id']).history(limit=1).flatten()

        reaction_role_embed = self.embed_msg()

        button_cp = create_button(
                    label='Claim Ping',
                    emoji='📢',
                    custom_id='claim_ping_reaction_role',
                    style=1
                )

        if len(reaction_role_channel_history) == 0:
            await client.get_channel(config['reaction_role_channel_id']).send(
                embed=reaction_role_embed,
                components=[
                    {
                        "type": 1,
                        "components": [button_cp]
                    }
                ]
            )

        else:
            await reaction_role_channel_history[0].edit(embed=reaction_role_embed)

    async def get_role(self, user_id):
        config = Config().config_cp
        await client.get_guild(Config().guild_id()).get_member(user_id).add_roles(
            client.get_guild(Config().guild_id()).get_role(config['claims_ping_role_id'])
        )

    def embed_msg(self):
        embed = discord.Embed(
            title='Claim Ping:',
            description=f'Click button below to get pinged on <#{Config().config_vs["claims_channel_id"]}> every time a claim is detected!',
            colour=Config().embed_color())

        return embed
