import logging
import re
import urllib.parse

import aiohttp
from bs4 import BeautifulSoup

torlog = logging.getLogger(__name__)


async def generate_directs(url):
    # blocklinks
    if (
        "mega.nz" in url
        or "drive.google.com" in url
        or "uptobox.com" in url
        or "1fiecher.com" in url
        or "googleusercontent.com" in url
    ):
        return "**ERROR:** Unsupported URL!"

    # mediafire.com
    elif "mediafire.com" in url:
        try:
            link = re.findall(r"\bhttps?://.*mediafire\.com\S+", url)[0]
            async with aiohttp.ClientSession() as ttksess:
                resp = await ttksess.get(link)
                restext = await resp.text()

            page = BeautifulSoup(restext, "lxml")
            info = page.find("a", {"aria-label": "Download file"})
            ourl = info.get("href")
            return ourl
        except:
            return "**ᴇʀʀᴏʀ:** 𝙲𝚊𝚗𝚝'𝚝 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍, 𝚍𝚘𝚞𝚋𝚕𝚎 𝚌𝚑𝚎𝚌𝚔 𝚢𝚘𝚞𝚛 𝚖𝚎𝚍𝚒𝚊𝚏𝚒𝚛𝚎 𝚕𝚒𝚗𝚔!"

    # disk.yandex.com
    elif "yadi.sk" in url or "disk.yandex.com" in url:
        try:
            link = re.findall(
                r"\b(https?://.*(yadi|disk)\.(sk|yandex)*(|com)\S+)", url
            )[0][0]
            print(link)
        except:
            return "**ᴇʀʀᴏʀ:** 𝙲𝚊𝚗𝚝'𝚝 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍, 𝚍𝚘𝚞𝚋𝚕𝚎 𝚌𝚑𝚎𝚌𝚔 𝚢𝚘𝚞𝚛 𝚢𝚊𝚍𝚒𝚜𝚔 𝚕𝚒𝚗𝚔!"

        api = "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}"
        try:
            async with aiohttp.ClientSession() as ttksess:
                resp = await ttksess.get(api.format(link))
                restext = await resp.json()
                ourl = restext["href"]
                return ourl
        except:
            torlog.exception("Ayee jooo")
            return "**ᴇʀʀᴏʀ:** 𝙲𝚊𝚗𝚝'𝚝 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍, 𝚝𝚑𝚎 𝚢𝚊𝚍𝚒𝚜𝚔 𝚏𝚒𝚕𝚎 𝚗𝚘𝚝 𝚏𝚘𝚞𝚗𝚍 𝚘𝚛 𝚍𝚘𝚠𝚖𝚕𝚘𝚊𝚍 𝚕𝚒𝚖𝚒𝚝 𝚛𝚎𝚊𝚌𝚑𝚎𝚍!"

    # zippyshare.com
    elif "zippyshare.com" in url:
        try:
            link = re.findall(r"\bhttps?://.*zippyshare\.com\S+", url)[0]
            async with aiohttp.ClientSession() as ttksess:
                resp = await ttksess.get(link)
                restext = await resp.text()
            base_url = re.search("http.+.com", restext).group()
            page_soup = BeautifulSoup(restext, "lxml")
            scripts = page_soup.find_all("script", {"type": "text/javascript"})
            for script in scripts:
                if "getElementById('dlbutton')" in script.text:
                    url_raw = re.search(
                        r"= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);", script.text
                    ).group("url")
                    math = re.search(
                        r"= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);", script.text
                    ).group("math")
                    url = url_raw.replace(math, '"' + str(eval(math)) + '"')
                    break
            ourl = base_url + eval(url)
            urllib.parse.unquote(url.split("/")[-1])
            return ourl
        except:
            return "**ᴇʀʀᴏʀ:** 𝙲𝚊𝚗𝚝'𝚝 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍, 𝚍𝚘𝚞𝚋𝚕𝚎 𝚌𝚑𝚎𝚌𝚔 𝚢𝚘𝚞𝚛 𝚣𝚒𝚙𝚙𝚢𝚜𝚑𝚊𝚛𝚎 𝚕𝚒𝚗𝚔!"

    # racaty.net
    elif "racaty.net" in url:
        try:
            link = re.findall(r"\bhttps?://.*racaty\.net\S+", url)[0]
            async with aiohttp.ClientSession() as ttksess:
                resp = await ttksess.get(link)
                restext = await resp.text()
            bss = BeautifulSoup(restext, "html.parser")
            op = bss.find("input", {"name": "op"})["value"]
            id = bss.find("input", {"name": "id"})["value"]

            async with aiohttp.ClientSession() as ttksess:
                rep = await ttksess.post(link, data={"op": op, "id": id})
                reptext = await rep.text()
            bss2 = BeautifulSoup(reptext, "html.parser")
            ourl = bss2.find("a", {"id": "uniqueExpirylink"})["href"]
            return ourl
        except:
            return "**ᴇʀʀᴏʀ:** 𝙲𝚊𝚗𝚝'𝚝 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍, 𝚍𝚘𝚞𝚋𝚕𝚎 𝚌𝚑𝚎𝚌𝚔 𝚢𝚘𝚞𝚛 𝚛𝚊𝚌𝚊𝚝𝚢 𝚕𝚒𝚗𝚔!"

    elif "pixeldrain.com" in url:
        url = url.strip("/ ")
        file_id = url.split("/")[-1]

        info_link = f"https://pixeldrain.com/api/file/{file_id}/info"
        dl_link = f"https://pixeldrain.com/api/file/{file_id}"

        async with aiohttp.ClientSession() as ttksess:
            resp = await ttksess.get(info_link)
            restext = await resp.json()

        if restext["success"]:
            return dl_link
        else:
            return "**ᴇʀʀᴏʀ:** 𝙲𝚊𝚗𝚝'𝚝 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍, {}.".format(restext["value"])
