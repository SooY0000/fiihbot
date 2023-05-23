import random
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

# Inventory dictionary to store the user's caught fish
inventory = {}

# Fish lists
common_fish = ['숭어', '붕어', '우럭', '참돔', '연어', '송어', '청어', '넙', '고등어', '멸치', '새우', '가물치', '가멸치', '송사리', '가을치', '가멸치', '참비늘 숭어']
rare_fish = ['장어', '복어', '참치치', '쏠베감펭', '곰치', '무지게 송어', '핑거 쉬림프', '레드테일 캣피쉬']
super_rare_fish = ['가오', 'dolphins', 'anglerfish', 'sturgeon', 'vampire squid', 'oarfish', 'Napoleon fish']
epic_fish = ['giant sea bass', 'barracuda', 'dorado', 'dumbo octopus', 'snakehead', 'sea turtle']
legendary_fish = ['mackerel', 'tiger shark', 'tarpon', 'sailfish', 'marlin', 'arowana']
mythic_fish = ['sunfish', 'whale shark', 'great white shark', 'killer whale', 'giant squid']
JunCho_fish = ['블롭피쉬', '메갈로돈', '모사 사우루스', '크라켄', '삼엽충']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def fish(ctx):
    common_chance = 0.89
    rare_chance = 0.23
    super_rare_chance = 0.101
    epic_chance = 0.032
    legendary_chance = 0.009
    mythic_chance = 0.0014

    catch_count = 1
    message = f'{ctx.author.mention} You caught: '

    if random.random() <= 0.12:
        catch_count = 2
        message += '2 fish! '
    elif random.random() <= 0.07:
        catch_count = 3
        message += '3 fish! '
    elif random.random() <= 0.01:
        catch_count = 4
        message += '4 fish! '

    for _ in range(catch_count):
        fish_type = 'common'
        fish_roll = random.random()

        if fish_roll <= mythic_chance:
            fish_type = 'mythic'
            fish = random.choice(mythic_fish)
        elif fish_roll <= legendary_chance:
            fish_type = 'legendary'
            fish = random.choice(legendary_fish)
        elif fish_roll <= epic_chance:
            fish_type = 'epic'
            fish = random.choice(epic_fish)
        elif fish_roll <= super_rare_chance:
            fish_type = 'super rare'
            fish = random.choice(super_rare_fish)
        elif fish_roll <= rare_chance:
            fish_type = 'rare'
            fish = random.choice(rare_fish)
        else:
            fish = random.choice(common_fish)

        # Add fish to the user's inventory
        if ctx.author.id not in inventory:
            inventory[ctx.author.id] = {}

        if fish in inventory[ctx.author.id]:
            inventory[ctx.author.id][fish] += 1
        else:
            inventory[ctx.author.id][fish] = 1

        message += f'{fish} ({fish_type} class), '

    await ctx.send(message[:-2])  # Remove the trailing comma and space

@bot.command()
async def view_inventory(ctx):
    if ctx.author.id in inventory and inventory[ctx.author.id]:
        inventory_stack = {
            'common': [],
            'rare': [],
            'super rare': [],
            'epic': [],
            'legendary': [],
            'mythic': []
        }

        for fish, count in inventory[ctx.author.id].items():
            if fish in common_fish:
                inventory_stack['common'].append((fish, count))
            elif fish in rare_fish:
                inventory_stack['rare'].append((fish, count))
            elif fish in super_rare_fish:
                inventory_stack['super rare'].append((fish, count))
            elif fish in epic_fish:
                inventory_stack['epic'].append((fish, count))
            elif fish in legendary_fish:
                inventory_stack['legendary'].append((fish, count))
            else:
                inventory_stack['mythic'].append((fish, count))

        embed = discord.Embed(title=f"{ctx.author.name}'s Inventory", color=discord.Color.blurple())
        for rarity, fish_list in inventory_stack.items():
            if fish_list:
                value = '\n'.join([f'{fish}: {count}' for fish, count in fish_list])
                embed.add_field(name=rarity.capitalize(), value=value, inline=False)

        embed.set_footer(text="Fish Inventory")

        await ctx.send(embed=embed)
    else:
        await ctx.send(f'{ctx.author.mention} Your inventory is empty.')


# Replace 'TOKEN' with your actual bot token
bot.run('MTEwNTA4NDI4MDk3NzI0NDIyMQ.G-c2Ku.D0aUqRmpTDIx8qRpeOq9lZimnZ-A5xRBN6MdN8')
