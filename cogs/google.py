import requests
import requests.auth
from discord.ext import commands


SEARCH_API_URL = 'https://www.googleapis.com/customsearch/v1'
DEV_KEY = ""
CX_KEY = ""


class GoogleCog(commands.Cog):
    """
    Uses https://developers.google.com/custom-search/v1/using_rest to perform text and image searches.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def googlesync(self, ctx) -> None:
        try:
            await ctx.bot.tree.sync()
            await ctx.send("Owner synced Google commands.")
        except Exception:
            await ctx.send(f"Failed to sync command. Is the owner calling this?")

    @commands.hybrid_command(
        name="g", description="Returns first Google search result for given query."
    )
    async def search(self, ctx: commands.Context, text: str):
        parsed = requests.get(
            SEARCH_API_URL, params={"cx": CX_KEY, "q": text, "key": DEV_KEY}
        ).json()

        try:
            result = parsed["items"][0]
        except KeyError:
            return "No results found."

        title = result["title"]
        content = result["snippet"]
        if not content:
            content = "No description available."
        else:
            content = content.replace("\n", "")

        await ctx.send(f"{result['link']} {title} {content}")

    @commands.hybrid_command(
        name="gis", description="Returns first Google search result for given query."
    )
    async def google_images(self, ctx: commands.Context, text: str):
        response = requests.get(
            SEARCH_API_URL,
            params={
                "cx": CX_KEY,
                "q": text,
                "searchType": "image",
                "key": DEV_KEY,
            },
        ).json()

        try:
            result = response["items"][0]
        except KeyError:
            return "No results found."

        await ctx.send(result["link"])


async def setup(bot):
    await bot.add_cog(GoogleCog(bot))
