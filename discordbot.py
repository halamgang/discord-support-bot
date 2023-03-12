# sup.py

import discord

intents = discord.Intents.all()
client = discord.Client(intents=intents)

SUPPORT_CATEGORY_NAME = "support"  # 변경 가능

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content.startswith('!지원'):
        support_role_name = "Support"  # 변경 가능
        support_category = discord.utils.get(message.guild.categories, name=SUPPORT_CATEGORY_NAME)

        if support_category is None:
            await message.channel.send(f"카테고리 '{SUPPORT_CATEGORY_NAME}'을(를) 찾을 수 없습니다.")
            return

        support_role = discord.utils.get(message.guild.roles, name=support_role_name)

        if support_role is None:
            await message.channel.send(f"역할 '{support_role_name}'을(를) 찾을 수 없습니다.")
            return

        overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.guild.me: discord.PermissionOverwrite(read_messages=True),
            support_role: discord.PermissionOverwrite(read_messages=True),
            message.author: discord.PermissionOverwrite(read_messages=True)
        }

        support_channel_name = f"{message.author.display_name}-지원"

        try:
            support_channel = await message.guild.create_text_channel(support_channel_name, category=support_category, overwrites=overwrites)
            await support_channel.send(f"{message.author.mention}님, 지원 채널이 생성되었습니다. 문의사항을 적어주세요.")
            await message.delete()
        except discord.errors.Forbidden:
            await message.channel.send("Bot에 권한이 없어 채널을 만들 수 없습니다.")
    
    elif message.channel.category.name == SUPPORT_CATEGORY_NAME and message.author != client.user:
        support_role_name = "Support"  # 변경 가능
        support_role = discord.utils.get(message.guild.roles, name=support_role_name)

        if support_role is None:
            await message.channel.send(f"역할 '{support_role_name}'을(를) 찾을 수 없습니다.")
            return

        if message.author == support_role or support_role in message.author.roles:
            if message.content.startswith("!삭제"):
                await message.channel.delete()
            else:
                await message.add_reaction('✅')
        else:
            await message.add_reaction('❌')

def run():
    client.run("MTA4NDMxNDQxNjQzNjIzNjMzOQ.G0M0o5._nSAP6KLWx1Fxph9cz5E4bVBl8R13q_uoEfQQY")
