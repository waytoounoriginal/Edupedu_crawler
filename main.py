import requests
import json

import asyncio
from EdgeGPT import Chatbot, ConversationStyle


def parse_articles():
    url = "https://www.edupedu.ro/wp-json/csco/v1/menu-posts?cat=15&type=category&per_page=5"
    response = requests.get(url)
    print("Crawling articles...")
    print(response.status_code)

    text = response.text
    encoded = json.loads(text)

    html_text = encoded["content"]
    html_text.split(r"\t\t\t\t\t")

    site_links = [];
    # Find all the links within the html_text
    for i in range(len(html_text)):
        if html_text[i:i + 4] == "href":
            link = ""
            j = i + 6
            while html_text[j] != '"':
                link += html_text[j]
                j += 1
            site_links.append(link)

    # Delete duplicates
    site_links = list(dict.fromkeys(site_links))

    print("Finished crawling articles...\n" "Detected links: \n")
    print(site_links)

    return site_links


async def shorten_articles(site_links):
    print("Creating bot...")
    bot = await Chatbot.create()
    prompt = "Renunta la introducerea ta ca Bing. Ofera doar informatii.\nRezuma urmatoarele articole in romana si ataseaza informatiile fiecaruia intr-o lista de bulletpoint-uri, atasand si titlul inainte. Ofera in finalul mesajului o analiza asupra evolutiei grevei profesorilor."

    for link in site_links:
        prompt += link + "\n"

    print("Asking bot...")
    response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative)

    text = response['item']['messages'][1]['text']

    print(text)

    await bot.close()

    return text


def write_in_markdown(text):
    print("Writing in markdown...")
    f = open("README.md", "w", encoding="utf-8")
    f.write(text)
    f.close()


async def main():
    site_links = parse_articles()
    text = await shorten_articles(site_links)
    write_in_markdown(text)

if __name__ == "__main__":
    asyncio.run(main())
