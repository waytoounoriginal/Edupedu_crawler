import datetime

import requests
import json

import lxml
from bs4 import BeautifulSoup

import asyncio
from EdgeGPT import Chatbot, ConversationStyle

def parse_articles():

    # Get the articles
    url = "https://www.edupedu.ro/category/stiri/"
    response = requests.get(url)
    response.encoding = 'utf-8'
    print("Crawling articles...")
    print(response.status_code)

    text = response.text

    # print(text)
    soup = BeautifulSoup(text, 'lxml')
    articles = soup.find_all("article")
    article_links = [article.find('a', {"class": "cs-overlay-link"}).get("href") for article in articles]
    print(article_links)

    return article_links[0:3]


async def shorten_articles(site_links):
    print("Creating bot...")
    bot = await Chatbot.create()
    prompt = "Te rog rezuma urmatoarele articole in romana si ataseaza informatiile fiecaruia intr-o lista de bulletpoint-uri, atasand si titlul inainte, boldit. Ofera in finalul mesajului o analiza concreta si compacta asupra evolutiei grevei profesorilor, cu cele mai actuale date, cu subtitlul boldit, format h2, '🏫 Despre greva profesorilor'. Boldeaza cele mai importante date.  "

    for link in site_links:
        prompt += link + "\n"

    print("Asking bot...")
    response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative)

    text = response['item']['messages'][1]['text']
    # text_created_at = response['item']['messages'][1]['createdAt']

    print(text)

    await bot.close()

    # Get the time
    formatted_time_string = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Format the text
    # Get rid of the first paragraph
    text = text.split("\n")[1:]

    # Join the text with newlines
    text = "\n".join(text)

    # Add a h1 title at the beginning of the text
    text = "# 👩‍🏫 Totul despre greva\n" + f"<sub>Ultima actualizare: {formatted_time_string}</sub>\n\n" + text

    # Add a small disclaimer at the end of the text
    text += "\n\n\n<sub><sub>Acest text a fost generat automat de BingAI folosind ultimele informatii de pe Edupedu, precum si de pe alte site-uri de stiri. Deci, nu te baza pe el pentru a lua decizii importante :)</sub></sub>"

    return text


def write_in_markdown(text):
    print("Writing in markdown...")
    f = open("README.md", "w", encoding="utf-8")
    f.write(text)
    f.close()


async def main():
    site_links = parse_articles()

    try:
        text = await shorten_articles(site_links)
    except Exception as e:
        print("Error")
        # Log error
        with open("error.log", "w") as f:
            f.write(f"[ERROR] TIME: {datetime.datetime.now()}\n{str(e)}\n\n")
            return

    write_in_markdown(text)

if __name__ == "__main__":
    asyncio.run(main())
