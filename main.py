import random
import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='!')

# Inventory dictionary to store the user's caught fish
inventory = {}

# Fish lists
common_fish = ['숭어', '붕어', '우럭', '참돔', '연어', '송어', '청어', '넙치', '고등어', '멸치', '새우', '가물치', '가멸치', '송사리', '가을치', '가멸치', '참비늘 숭어']
rare_fish = ['장어', '복어', '참치', '쏠베감펭', '곰치', '무지개 송어', '핑거 쉬림프', '레드테일 캣피쉬']
super_rare_fish = ['가오리', '돌고래', '아귀', '주걱 철갑상어', '뱀파이어 오징어', '산갈치', '나폴레옹 피쉬']
epic_fish = ['자이언트 씨배스', '바라쿠다', '도라도', '덤보 문어', '가물치', '바다 거북']
legendary_fish = ['만새기', '범 상어', '뱀 상어', '타폰', '돛새치', '아로와나']
mythic_fish = ['개복치', '고래 상어', '백상아리', '범고래', '대왕오징어']
JunCho_fish = ['블롭피쉬', '메갈로돈', '모사사우루스', '크라켄', '삼엽충']

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
    message = f'{ctx.author.mention} 물고기를 잡았습니다! '

    if random.random() <= 0.12:
        catch_count = 2
        message += '2마리! '
    elif random.random() <= 0.07:
        catch_count = 3
        message += '3마리! '
    elif random.random() <= 0.01:
        catch_count = 4
        message += '4마리!! '

    for _ in range(catch_count):
        fish_type = '커먼'
        fish_roll = random.random()

        if fish_roll <= mythic_chance:
            fish_type = '신화'
            fish = random.choice(mythic_fish)
        elif fish_roll <= legendary_chance:
            fish_type = '레전더리'
            fish = random.choice(legendary_fish)
        elif fish_roll <= epic_chance:
            fish_type = '에픽'
            fish = random.choice(epic_fish)
        elif fish_roll <= super_rare_chance:
            fish_type = '슈퍼 레어'
            fish = random.choice(super_rare_fish)
        elif fish_roll <= rare_chance:
            fish_type = '레어'
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

        message += f'{fish} ({fish_type} 등급), '

    await ctx.send(message[:-2])  # Remove the trailing comma and space


@bot.command()
async def view_inventory(ctx):
    if ctx.author.id in inventory and inventory[ctx.author.id]:
        inventory_stack = {
            '커먼': [],
            '레어': [],
            '슈퍼 레어': [],
            '에픽': [],
            '레전더리': [],
            '신화': []
        }

        for fish, count in inventory[ctx.author.id].items():
            if fish in common_fish:
                inventory_stack['커먼'].append((fish, count))
            elif fish in rare_fish:
                inventory_stack['레어'].append((fish, count))
            elif fish in super_rare_fish:
                inventory_stack['슈퍼 레어'].append((fish, count))
            elif fish in epic_fish:
                inventory_stack['에픽'].append((fish, count))
            elif fish in legendary_fish:
                inventory_stack['레전더리'].append((fish, count))
            else:
                inventory_stack['미틱'].append((fish, count))

        embed = discord.Embed(title=f"{ctx.author.name}님의 인벤토리", color=discord.Color.blurple())
        for rarity, fish_list in inventory_stack.items():
            if fish_list:
                value = '\n'.join([f'{fish}: {count}' for fish, count in fish_list])
                embed.add_field(name=rarity.capitalize(), value=value, inline=False)

        embed.set_footer(text="물고기 창고")

        await ctx.send(embed=embed)
    else:
        await ctx.send(f'{ctx.author.mention} 인벤토리가 비었습니다.')

@bot.command()
async def stop(ctx):
    await ctx.send("봇을 종료합니다...")
    await bot.logout()  # Gracefully logout and stop the bot


# Replace 'TOKEN' with your actual bot token
bot.run('MTEwNTA4NDI4MDk3NzI0NDIyMQ.GdWUeY.XEZUVqLTf0V-RMNrNVBkBjCCimR-IF_G0xDmDQ')
