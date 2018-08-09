import discord
from discord.ext import commands


class General:
    @commands.command(name='todo')
    async def test_todo(self, ctx):
        remaining = {
            'Complete': [],
            'In progress': [
                'Website'
            ],
            'Not implemented': [
                'PyDoc'
                'Python code sandbox',
                'CPython bug/branch tracker',
                'Forward PSF tweets?',
            ],
        }

        await ctx.send('\n\n'.join(f'**{key}:**\n' + '\n'.join(f'• {_}' for _ in value) for key, value in remaining.items() if value))

    @commands.command(name='source')
    async def test_source(self, ctx):
        await ctx.send('https://github.com/mental32/ep_bot')

    @commands.command(name='profile')
    async def test_profile(self, ctx, member: discord.Member):
        pass

def setup(bot):
    bot.add_cog(General())
