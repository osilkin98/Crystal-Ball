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
    async def stop(self, ctx):
        """
        Kills the current server
        """
        await ctx.send('Bye!', delete_after=10)
        exit()

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
        await ctx.send('Nanopanels command', delete_after=20)
    
    @nano.command()
    async def on(self, ctx: Context):
        """
        Turns the nanopanels on if they are off, otherwise does nothing
        """
        if not self.nanopanels.get_power():
            self.nanopanels.toggle_power()

        await ctx.send('Nanopanels on', delete_after=20) 

    @nano.command()
    async def off(self, ctx: Context):
        """
        Turns the nanopanels off if they are on
        """
        if self.nanopanels.get_power():
            self.nanopanels.toggle_power()
        
        await ctx.send('Nanopanels off', delete_after=20)

    @nano.command()
    async def brightness(self, ctx: Context):
        """
        Set the nanopanels brightness, value must be between 0 and 100
        """
        args = ctx.message.content.split(' ')
        if len(args) < 3:
            await ctx.send('Error: must have a `brightness` value', delete_after=10)

        brightness = int(args[2])
        duration = abs(int(args[3])) if len(args) >= 4 else 0

        if 0 <= brightness <= 100:
            self.nanopanels.set_brightness(
                brightness=brightness, 
                duration=duration
            )
            await ctx.send(f'Set brightness to {brightness}', delete_after=10)
        else:
            await ctx.send('Invalid values', delete_after=10)

    @nano.command()
    async def effects(self, ctx: Context):
        """
        Displays available scenes
        """
        msg = ''
        for i, effect in enumerate(self.nanopanels.list_effects()):
            msg += f'{i+1}. {effect}\n'
        
        await ctx.send(f'```md\n{msg}```',delete_after=60)
    

    @nano.command()
    async def effect(self, ctx: Context):
        """
        Sets the provided effect
        """
        _, _, element_no = ctx.message.content.split(' ')
        element_no = int(element_no)
        effects = self.nanopanels.list_effects()

        # check for out of bounds
        if element_no > len(effects):
            return

        selected = effects[element_no - 1]
        if self.nanopanels.set_effect(selected):
            await ctx.send(f'Set effect `{selected}`', delete_after=20)
        else:
            await ctx.send(f'Error setting effect `{selected}`', delete_after=10) 


    @nano.command()
    async def info(self, ctx: Context):
        """
        Prints out information about the nanopanels in a readable format
        """
        # info to print: brightness, on/off state, current effect
        info = self.nanopanels.get_info()
        brightness = info['state']['brightness']['value']
        state = 'on' if info['state']['on']['value'] else 'off'
        effect = info['effects']['select']
        print(json.dumps(self.nanopanels.get_info(), indent=4))


        message = f'effect: `{effect}`\nbrightness: `{brightness}`\nstate: `{state}`'
        await ctx.send(message, delete_after=20)        




def setup(bot):
    bot.add_cog(Sample(bot))
