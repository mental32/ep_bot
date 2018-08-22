import asyncio


class GuildCog:
    def __init__(self, bot):
        self.bot = bot

        if self.bot.is_ready():
            self.bot.loop.create_task(self.__cog_init())

    def __repr__(self):
        return f'<Cog: {type(self).__name__}>'

    async def on_ready(self):
        self.bot.loop.create_task(self.__cog_init())

    @property
    def _roles(self):
        return {role.name: role for role in self._guild.roles}

    async def __cog_init(self):
        while not hasattr(self.bot, '_guild'):
            await asyncio.sleep(0)

        self._guild = _guild = self.bot._guild
        self._general = _guild.get_channel(455072636075245590)

        _roles = self._roles
        self._member_role = _roles['Member']
        self._bot_role = _roles['Bot']

        self.bot.dispatch('cog_init', self)
