"""
Basic cog to show next F1 race
"""
from datetime import datetime

import discord
import fastf1
import requests
from discord.ext import commands
import re


class F1Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session_re = re.compile(r"Session(\d)(.*)")

    @commands.command(name="f1", help="Show info about the next F1 Race.")
    async def next_race(self, ctx):
        next_race = requests.get("https://ergast.com/api/f1/current/next.json").json()
        round = next_race["MRData"]["RaceTable"]["Races"][0]["round"]
        event = fastf1.get_event(2023, int(round))

        race = F1Race()
        race.round_number = event["RoundNumber"]
        race.country = event["Country"]
        race.location = event["Location"]
        race.event_name = event["EventName"]
        race.datetime = event["EventDate"]

        for index, value in event.items():
            session_data = self.session_re.findall(index)
            if len(session_data) > 0:
                session_number = int(session_data[0][0])
                if session_data[0][1] == "":
                    race.sessions[session_number].name = value
                else:
                    race.sessions[session_number].date = value

        await ctx.send(embed=race.to_embed())


class F1Race:
    def __init__(self):
        self.round_number = 0
        self.country = ""
        self.location = ""
        self.event_name = ""
        self.sessions = [F1RaceSession() for _ in range(10)]

    def countdown(target, datetime):
        """
        Calculate time to `target` datetime object from current time when invoked.
        Returns a list containing the string output and tuple of (days, hrs, mins, sec).
        """
        delta = target - datetime.now()
        d = delta.days if delta.days > 0 else 0
        # timedelta only stores seconds so calculate mins and hours by dividing remainder
        h, rem = divmod(delta.seconds, 3600)
        m, s = divmod(rem, 60)
        stringify = (
            f"{int(d)} {'days' if d is not 1 else 'day'}, "
            f"{int(h)} {'hours' if h is not 1 else 'hour'}, "
            f"{int(m)} {'minutes' if m is not 1 else 'minute'}, "
            f"{int(s)} {'seconds' if s is not 1 else 'second'} "
        )
        return [stringify, (d, h, m, s)]

    def to_embed(self):
        embed = discord.Embed(
            color=0x9C824A, title=f"Next Race - Round {self.round_number}"
        )

        embed.set_author(
            name="F1 Races",
            icon_url="https://purepng.com/public/uploads/large/purepng.com-formula-1-logoformula-1logonew2018-21529676510t61kq.png",  # noqa
        )

        embed.add_field(name="Country", value=self.country, inline=True)
        embed.add_field(name="Location", value=self.location, inline=True)
        embed.add_field(name="Event Name", value=self.event_name, inline=True)

        date = datetime.strptime(f"{self.datetime}", "%Y-%m-%d %H:%M:%S")
        # cd = self.countdown(self.date)
        #     f'{date.year}-{date.month}-{date.day}{date.hour}-{date.minute}-{date.second}'
        # )
        #
        # embed.add_field(name='Countdown', value=self.cd, inline=True)

        for session in self.sessions:
            if session.has_value():
                embed.add_field(name=session.name, value=session.date, inline=False)
        return embed


class F1RaceSession:
    def __init__(self):
        self.name = ""
        self.date = ""

    def has_value(self):
        return self.name != "" and self.date != ""


async def setup(bot):
    await bot.add_cog(F1Cog(bot))
