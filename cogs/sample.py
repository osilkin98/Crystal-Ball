import json

from discord.ext import commands
from discord.ext.commands.context import Context

from nanoleafapi import Nanoleaf

class Sample(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nanoip = self.bot.nano_config['ipAddress']
        self.nanoauth = self.bot.nano_config['authToken']

        self.nanopanels = Nanoleaf(
            ip=self.bot.nano_config['ipAddress'],
            auth_token=self.bot.nano_config['authToken'],
            print_errors=True
        )


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        This event receives the the guild when the bot joins.
        """
        print(f'Joined {guild.name} with {guild.member_count} users!')

    @commands.command()
    async def test(self, ctx):
        """
        A test command, Mainly used to show how commands and cogs should be laid out.
        """
        await ctx.send('Tested!')

    @commands.group(invoke_without_command=True)
    async def foo(self, ctx: Context):
        """
        A sub command group, Showing how sub command groups can be made.
        """
        await ctx.send('try my subcommand')

    @foo.command(aliases=['an_alias'])
    async def bar(self, ctx: Context):
        """
        I have an alias!, I also belong to command 'foo'
        """
        await ctx.send('foo bar!')


    @commands.group(invoke_without_command=True)
    async def nano(self, ctx: Context):
        # print(type(ctx))
        await ctx.send('Nanopanels command')
    
    @nano.command()
    async def toggle(self, ctx: Context):
        """
        Toggles nanopanels on/off
        """
        self.nanopanels.toggle_power()    
        status = "panels turned on" if self.nanopanels.get_power() else "panels turned off" 
        await ctx.send(status, delete_after=20)

    @nano.command()
    async def effects(self, ctx: Context):
        """
        Displays available scenes
        """
        await ctx.send(f'```json\n{json.dumps(self.nanopanels.get_info()["effects"], indent=2)}```')
    

    @nano.command()
    async def set_effect(self, ctx: Context):
        print('test etststseterwersrse')
        print('hi')
        await ctx.send('hello')
        



def setup(bot):
    bot.add_cog(Sample(bot))
