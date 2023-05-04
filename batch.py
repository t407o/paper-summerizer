import datetime
import os
import textwrap
from time import sleep

import openai

from modules.messenger import DiscordMessenger, Messenger
from modules.model import Paper
from modules.paper_search import GoogleScholerSearch, PaperSearch

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

DISCORD_NOTIFIEE = os.getenv("DISCORD_NOTIFIEE")

SEARCH_LIMIT = 10
BATCH_SIZE = 10

search_keywords = []

messenger: Messenger = DiscordMessenger(
    DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID, DISCORD_NOTIFIEE
)
paper_search: PaperSearch = GoogleScholerSearch()

# list of (keyword, paper)
summarize_queue = []
post_histories = set()
post_count = 0

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def main():
    print("Batch start!")

    init()
    run()

    print("Batch completed successfully!")


def init():
    openai.api_key = OPENAI_API_KEY

    load_search_keywords_from("search_keywords.txt")
    load_search_histories_from("search_histories.txt")

    if not search_keywords:
        print("No search keywords found! Check the search_keywords.txt")
        exit(1)


def run():
    timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
    sendMessage(f"[Batch Start🚀] timestamp = {timestamp}")

    print("start searching...")
    for keyword in search_keywords:
        new_papers = search(keyword)

        enqueue(keyword, new_papers)

        print("waiting for 10 seconds... (to avoid rate limit)")
        sleep(10)

    print("start posting...")
    while summarize_queue:
        keyword, paper = dequeue()

        summarize_and_post(keyword, paper)
        append_to_post_histories(paper)

        print("waiting for 20 seconds... (to avoid rate limit)")
        sleep(20)

    if post_count > 0:
        sendWithMension(f"New {post_count} paper(s) are found!🎊")
    else:
        sendMessage(f"No new paper found...😇")

    sendMessage(f"[Batch End🏁] timestamp = {timestamp}")


def search(keyword: str):
    print(f"searching... keyword={keyword}")

    papers = paper_search.execute(keyword, SEARCH_LIMIT)

    print(f"total - {len(papers)} hits")

    new_papers = list(filter(is_new_paper, papers))

    print(f"new papers - {len(new_papers)} hits")
    print(f"returns {BATCH_SIZE} papers of {len(new_papers)} new papers")

    return new_papers[:BATCH_SIZE]


def summarize_and_post(keyword: str, paper: Paper):
    print("Trying to summarise abstract...")
    summarized_paper = summarize_abstract(paper)
    print("Summarization success!")

    message = toMessage(keyword, summarized_paper)

    print(f"Sending message... title={paper.title}")
    sendMessage(message)

    print("Successfully sent!")


def is_new_paper(paper: Paper):
    return paper.title not in post_histories


def summarize_abstract(paper: Paper):
    paper.abstract = ask_gpt_to_summarize(paper.abstract)
    return paper


def ask_gpt_to_summarize(abstract: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": abstract},
            {
                "role": "user",
                "content": "この文章を400字以内の日本語で要約してください。",
            },
        ],
    )
    return response.choices[0].message.content


def toMessage(keyword: str, paper: Paper):
    message = f"""
        🎺New Arrival🎺 {f'- {paper.submitted_at}' if paper.submitted_at else ""}
        **Keyword**: {keyword}
        **Title**: {paper.title}
        **Abstract**: {paper.abstract}
        **Author**: {", ".join(paper.authors)}
        **Url**: {blankIfNone(paper.url)}
    """
    return textwrap.dedent(message)[1:-1]


def blankIfNone(value: str):
    return value if value else "(not available)"


def sendMessage(message: str):
    messenger.send(message)


def sendWithMension(message: str):
    messenger.sendWithMention(message)


def enqueue(keyword: str, papers: list[Paper]):
    for i, paper in enumerate(papers):
        print(f"{i+1}. {paper.title}")
        summarize_queue.append((keyword, paper))


def dequeue():
    return summarize_queue.pop(0)


def append_to_post_histories(paper: Paper):
    print(f"recording search history... title={paper.title}")
    post_histories.add(paper.title)
    save_search_history_to("search_histories.txt", paper)

    global post_count
    post_count += 1


def save_search_history_to(file: str, paper: Paper):
    with open(os.path.join(__location__, file), "a+", encoding="utf-8") as f:
        f.write(f"{paper.title}\n")


def load_search_histories_from(file: str):
    if not os.path.exists(os.path.join(__location__, file)):
        print("No search history found...")
        return

    with open(os.path.join(__location__, file), "r", encoding="utf-8") as f:
        for line in f:
            post_histories.add(line.strip())


def load_search_keywords_from(file: str):
    with open(os.path.join(__location__, file), "r", encoding="utf-8") as f:
        for line in f:
            search_keywords.append(line.strip()) if line.strip() else None


main()
