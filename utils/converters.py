import discord
import re
from discord.ext import commands


class SafeMember(commands.Converter):
    # A re-implementation of https://github.com/Rapptz/discord.py/blob/1863a1c6636f53592519320a173ec9573c090c0b/discord/ext/commands/converter.py
    async def convert(self, ctx, argument) -> discord.Member:
        match = re.match(r'([0-9]{15,21})$', argument) or re.match(r'<@!?([0-9]+)>$', argument)
        guild = ctx.guild
        if match is None:
            # not a mention...
            if guild and "#" in argument:
                result = guild.get_member_named(argument)
                if result is None:
                    raise commands.errors.BadArgument(f'Member "{argument}" not found. Search terms are case sensitive.')
            else:
                raise commands.errors.BadArgument('Matches by only nick/username are not allowed.')
        else:
            user_id = int(match.group(1))
            result = guild.get_member(user_id)
            if result is None:
                raise commands.errors.BadArgument(f'Member "{user_id}" not found.')
        return result


class FetchMember(commands.IDConverter):
    # Based on MemberConverter to fetch userid in case the userid cant be found in the guild
    async def convert(self, ctx, argument) -> discord.User:
        bot = ctx.bot
        match = self._get_id_match(argument) or re.match(r'<@!?([0-9]+)>$', argument)
        guild = ctx.guild
        if match is None and guild:
            result = guild.get_member_named(argument)
        else:
            user_id = int(match.group(1))
            result = guild.get_member(user_id) or await bot.fetch_user(user_id) if guild else await bot.fetch_user(user_id)
        if result is None:
            raise commands.errors.BadArgument('User "{}" not found'.format(argument))
        return result
