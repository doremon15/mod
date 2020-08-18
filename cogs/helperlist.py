import discord

from utils.database import DatabaseCog
from utils.converters import SafeMember
from utils.checks import is_staff
from discord.ext import commands


class HelperList(DatabaseCog):
    """
    Management of active helpers.
    """
    async def cog_check(self, ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        return True

    @is_staff(role='Owner')
    @commands.command()
    async def addhelper(self, ctx, member: SafeMember, position):
        """Add user as a helper. Owners only."""
        if position not in self.bot.helper_roles:
            await ctx.send(f"💢 That's not a valid position. You can use __{'__, __'.join(self.bot.helper_roles.keys())}__")
            return
        await self.add_helper(member.id, position)
        await member.add_roles(self.bot.roles['Helpers'])
        await ctx.send(f"{member.mention} is now a helper. Welcome to the party room!")

    @is_staff(role='Owner')                       
    @commands.command()
    async def delhelper(self, ctx, member: SafeMember):
        """Remove user from helpers. Owners only."""
        await ctx.send(member.name)
        await self.remove_helper(member.id)
        await member.remove_roles(self.bot.roles['Helpers'])
        await ctx.send(f"{member.mention} is no longer a helper. Stop by some time!")

    @commands.command()
    async def helpon(self, ctx):
        """Gain highlighted helping role. Only needed by Helpers."""
        author = ctx.author
        console = await self.get_console(ctx.author.id)
        if not console:
            await ctx.send("You are not listed as a helper, and can't use this.")
            return
        await author.add_roles(self.bot.helper_roles[console])
        await ctx.send(f"{author.mention} is now actively helping.")
        msg = f"🚑 **Elevated: +Help**: {author.mention} | {author}"
        await self.bot.channels['mod-logs'].send(msg)

    @commands.command()
    async def helpoff(self, ctx):
        """Remove highlighted helping role. Only needed by Helpers."""
        author = ctx.author
        console = await self.get_console(ctx.author.id)
        if not console:
            await ctx.send("You are not listed as a helper, and can't use this.")
            return
        await author.remove_roles(self.bot.helper_roles[console])
        await ctx.send(f"{author.mention} is no longer actively helping!")
        msg = f"👎🏻 **De-Elevated: -Help**: {author.mention} | {author}"
        await self.bot.channels['mod-logs'].send(msg)

    @commands.command()
    async def listhelpers(self, ctx):
        """List helpers per console."""
        helper_list = await self.get_helpers_role()
        consoles = dict.fromkeys(self.bot.helper_roles.keys())
        embed = discord.Embed()
        for console in consoles:
            consoles[console] = []
            for helper in helper_list:
                if console in helper:
                    consoles[console].append(helper[0])
            if consoles[console]:
                embed.add_field(name=console, value="".join([f"<@{x}>\n" for x in consoles[console]]), inline=False)
        await ctx.send("Here is a list of our helpers:", embed=embed)


def setup(bot):
    bot.add_cog(HelperList(bot))
