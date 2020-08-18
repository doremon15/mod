from utils.database import DatabaseCog
from discord.ext import commands
import discord

staff_ranks = {"Owner": 0, "SuperOP": 1, "OP": 2, "HalfOP": 3, "Helper": 4}


def is_staff(role):
    async def predicate(ctx):
        if isinstance(ctx.channel, discord.abc.GuildChannel):
            return await check_staff(ctx, role) if not ctx.author == ctx.guild.owner else True
        else:
            return await check_staff(ctx, role)
    return commands.check(predicate)


async def check_staff(ctx, role):
    if role == "Helper":
        if await DatabaseCog.get_console(ctx, ctx.author.id):
            return True
    rank = await DatabaseCog.get_stafftrole(ctx, ctx.author.id)
    if rank:
        return staff_ranks[rank] <= staff_ranks[role]
    return False


async def check_staff_id(ctx, role, id):
    if role == "Helper":
        if await DatabaseCog.get_console(ctx, id):
            return True
    rank = await DatabaseCog.get_stafftrole(ctx, id)
    if rank:
        return staff_ranks[rank] <= staff_ranks[role]
    return False


async def check_bot_or_staff(ctx, target: discord.user, action: str):
    if target.bot:
        who = "a bot"
    elif await check_staff_id(ctx, "Helper", target.id):
        who = "another staffer"
    else:
        return False

    return await ctx.send(f"You can't {action} {who} with this command!")

def check_if_user_can_sr():
    async def predicate(ctx):
        author = ctx.author
        if not await check_staff_id(ctx, 'Helper', author.id) and (ctx.bot.roles['Verified'] not in author.roles) and (ctx.bot.roles['Trusted'] not in author.roles) and (ctx.bot.roles['Retired Staff'] not in author.roles):
            return False
        return True
    return commands.check(predicate)

def check_if_user_can_ready():
    async def predicate(ctx):
        channel = ctx.channel
        if channel != ctx.bot.channels['newcomers']:
            return False
        return True
    return commands.check(predicate)

