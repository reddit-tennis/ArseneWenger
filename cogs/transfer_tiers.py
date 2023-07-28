#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A simple cog that adds certain reactions to messages
"""
from itertools import zip_longest

from discord.ext import commands


class TransferReactionsCog(commands.Cog):
    """
    Reacts to transfer news based on the tier of the source
    """
    def __init__(self, bot):
        self.bot = bot
        self.tiers = {
            'Tier 1': {
                'names': [
                    'David Ornstein',
                    'Fabrizio Romano',
                    'Charles Watts',
                    'BBC Sport',
                ],
                'sources': [
                    'https://twitter.com/David_Ornstein',
                    'https://twitter.com/FabrizioRomano',
                    'https://twitter.com/charles_watts',
                    'https://twitter.com/BBCSport',
                    'https://www.bbc.co.uk/sport'
                    ],
                'reaction': '🟢'
            },
            'Tier 2': {
                'names': [
                    'Gianluca Di Marzio',
                    'Amy Lawrence',
                    'Mohamed Bouhafsi',
                    'James MacNicholas',
                    'The Guardian',
                    'The Athletic',
                ],
                'sources': [
                    'https://twitter.com/DiMarzio',
                    'https://twitter.com/amylawrence71',
                    'https://twitter.com/mohamedbouhafsi',
                    'https://twitter.com/JamesMcNicholas',
                    'https://www.theguardian.com/',
                    'https://theathletic.com/',
                ],
                'reaction': '🟡'
            },
            'Tier 3': {
                'names': [
                    'James Olley',
                    'Mark Ogden',
                    'Alexis Bernard',
                    'Mark Irwin',
                    'Sam Dean',
                    'Simon Collings',
                    'Manu Lonjon',
                    'Jeremy Wilson',
                    'Guillem Balague',
                    'James Benge',
                    'Andy Burton',
                    'Raphael Honigstein',
                    'Sami Mokbel',
                    "L'Equipe",
                    'The Times',
                    'BILD',
                    'The Independent',
                    'The Telegraph',
                    'El Confidencial',
                    'Gianluca Di Marzio',
                ],
                'sources': [
                    'https://twitter.com/JamesOlley',
                    'https://twitter.com/MarkOgden_',
                    'https://twitter.com/alexisbernard10',
                    'https://twitter.com/MarkIrwin_',
                    'https://twitter.com/SamJDean',
                    'https://twitter.com/SimonCollings',
                    'https://twitter.com/ManuLonjon',
                    'https://twitter.com/JWTelegraph',
                    'https://twitter.com/GuillemBalague',
                    'https://twitter.com/jamesbenge',
                    'https://twitter.com/burtonad',
                    'https://twitter.com/honigstein',
                    'https://twitter.com/SamiMokbel81_DM',
                    'https://twitter.com/lequipe',
                    'https://www.thetimes.co.uk/',
                    'https://www.bild.de/',
                    'https://www.independent.co.uk/',
                    'https://www.telegraph.co.uk/',
                    'https://www.elconfidencial.com/',
                    'https://gianlucadimarzio.com/en/',
                ],
                'reaction': '🟠'
            },
            'Tier 4': {
                'names': [
                    'MARCA',
                    'Sky Sports',
                    'AS',
                    'Mundo Deportivo',
                    'SPORT',
                    'SportBild',
                    'Kaveh Solhekol',
                    'Dharmesh Seth',
                    'John Cross',
                    'football.london',
                    'Cadena SER',
                ],
                'sources': [
                    'https://www.marca.com/',
                    'https://www.skysports.com/',
                    'https://as.com/',
                    'https://www.mundodeportivo.com/',
                    'https://www.sport.es/',
                    'https://www.sportbild.de/',
                    'https://twitter.com/solhekol',
                    'https://twitter.com/dharmeshseth',
                    'https://twitter.com/johncrossmirror',
                    'https://www.football.london/',
                    'https://cadenaser.com/',
                ],
                'reaction': '🔴'
            }
        }
    @commands.Cog.listener()
    async def on_message(self, message):
        for tier, info in self.tiers.items():
            names = [x for x in info['names']]
            sources = [x for x in info['sources']]
            reaction = info['reaction']
            zippy = list(zip_longest(names, sources, reaction, fillvalue=reaction))

            for name, source, reactions in zippy:
                if name in message.content:
                    await message.add_reaction(reaction)
                    return
                elif source in message.content:
                    await message.add_reaction(reaction)
                    return
                await self.check_embeds(message, name, reaction, source)


    async def check_embeds(self, message, name, reaction, source):
        for embed in message.embeds:
            if name in embed.author.name:
                await message.add_reaction(reaction)
                pass
            if source in embed.author.name:
                await message.add_reaction(reaction)
                pass


async def setup(bot):
    """
    Add the cog we have made to our bot.

    This function is necessary for every cog file, multiple classes in the
    same file all need adding and each file must have their own setup function.
    """
    await bot.add_cog(TransferReactionsCog(bot))
