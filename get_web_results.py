# import streamlit as st
from duckduckgo_search import DDGS
from extract_subs import filter_links
import time
from groq import Groq

REGIONS = {
    "Arabia": "xa-ar",
    "Arabia (en)": "xa-en",
    "Argentina": "ar-es",
    "Australia": "au-en",
    "Austria": "at-de",
    "Belgium (fr)": "be-fr",
    "Belgium (nl)": "be-nl",
    "Brazil": "br-pt",
    "Bulgaria": "bg-bg",
    "Canada": "ca-en",
    "Canada (fr)": "ca-fr",
    "Catalan": "ct-ca",
    "Chile": "cl-es",
    "China": "cn-zh",
    "Colombia": "co-es",
    "Croatia": "hr-hr",
    "Czech Republic": "cz-cs",
    "Denmark": "dk-da",
    "Estonia": "ee-et",
    "Finland": "fi-fi",
    "France": "fr-fr",
    "Germany": "de-de",
    "Greece": "gr-el",
    "Hong Kong": "hk-tzh",
    "Hungary": "hu-hu",
    "India": "in-en",
    "Indonesia": "id-id",
    "Indonesia (en)": "id-en",
    "Ireland": "ie-en",
    "Israel": "il-he",
    "Italy": "it-it",
    "Japan": "jp-jp",
    "Korea": "kr-kr",
    "Latvia": "lv-lv",
    "Lithuania": "lt-lt",
    "Latin America": "xl-es",
    "Malaysia": "my-ms",
    "Malaysia (en)": "my-en",
    "Mexico": "mx-es",
    "Netherlands": "nl-nl",
    "New Zealand": "nz-en",
    "Norway": "no-no",
    "Peru": "pe-es",
    "Philippines": "ph-en",
    "Philippines (tl)": "ph-tl",
    "Poland": "pl-pl",
    "Portugal": "pt-pt",
    "Romania": "ro-ro",
    "Russia": "ru-ru",
    "Singapore": "sg-en",
    "Slovak Republic": "sk-sk",
    "Slovenia": "sl-sl",
    "South Africa": "za-en",
    "Spain": "es-es",
    "Sweden": "se-sv",
    "Switzerland (de)": "ch-de",
    "Switzerland (fr)": "ch-fr",
    "Switzerland (it)": "ch-it",
    "Taiwan": "tw-tzh",
    "Thailand": "th-th",
    "Turkey": "tr-tr",
    "Ukraine": "ua-uk",
    "United Kingdom": "uk-en",
    "United States": "us-en",
    "United States (es)": "ue-es",
    "Venezuela": "ve-es",
    "Vietnam": "vn-vi",
    "No region": "wt-wt",
}

def search_the_web(user_query, max_results=3, region="ie-en", api_key=None):
    if user_query:
        # SEARCH_PROMPT = f"""
        # <instructions>Given the following search query, give me a good effective search text to search the web. Just respond with one brief text.</instructions>\n
        # <user_query>{user_query}</user_query>
        # """

        # messages = [
        #     {"role": "user", "content": SEARCH_PROMPT},
        # ]
        # try:
        #     client2 = Groq(
        #         api_key = # ! give a separate api key, then uncomment this line
        #     )
        #     chat_completion = client2.chat.completions.create(
        #         model="llama3-70b-8192",
        #         messages=messages,
        #         temperature=1,
        #         max_tokens=100,
        #         top_p=0.9,
        #     )

        #     query = chat_completion.choices[0].message.content or user_query
        #     print(query)

        # except Exception as e:
        #     print(e)
        #     print("Error")
        #     query = user_query

        query = user_query

        results = DDGS().text(query, region=region, max_results=max_results)

        img_results = DDGS().images(
            keywords=query,
            region="ie-en",
            safesearch="off",
            size=None,
            # color="Monochrome",
            type_image=None,
            layout=None,
            license_image=None,
            max_results=max_results,
        )

        video_links = []
        img_links = []
        markdown_placeholder = """"""
        body = """<instructions>Refer these results from the web and respond to the user: </instructions>\n"""

        if results:
            for idx, search_result in enumerate(results):

                body += f"<result {idx}>\n{search_result['body']}\n</result {idx}>\n"

                video_links_from_search = filter_links(search_result["href"])

                if not video_links_from_search:
                    markdown_placeholder += f"- {search_result['href']}\n"
                else:
                    video_links.extend(video_links_from_search)

        if img_results:
            for idx, image_result in enumerate(img_results):
                video_links_from_img_search = filter_links(image_result["url"])
                if not video_links_from_img_search:
                    markdown_placeholder += f"- {image_result['url']}\n"
                else:
                    video_links.extend(video_links_from_img_search)
                img_links.append(image_result["image"])

        body += """\n<instructions>The above results might contain irrelevant information. Determine the relevance of the information and respond to the user accordingly.
                Do not include the text within brackets in your response. </instructions>"""

        # Remove duplicates
        img_links = list(set(img_links))
        video_links = list(set(video_links))

        return body, img_links, video_links, markdown_placeholder
