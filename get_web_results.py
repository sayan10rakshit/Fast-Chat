# import streamlit as st
from duckduckgo_search import DDGS
from extract_subs import filter_links

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
# MAX_RESULTS = 3

# query = "give me info about peter cat kolkata"

# query = st.text_area(
#     "Enter your query:",
#     placeholder="give me info about peter cat kolkata",
# )


def search_the_web(query, max_results=3, region="ie-en"):
    if query:
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
        MARKDOWN_PLACEHOLDER = """"""
        BODY = """<instructions>Refer these results from the web and respond to the user: </instructions>\n"""

        for idx in range(max_results):

            BODY += f"<result{idx}>\n{results[idx]['body']}\n</result{idx}>\n"

            link_from_search = filter_links(results[idx]["href"])
            link_from_img_search = filter_links(img_results[idx]["url"])

            if not link_from_search:
                MARKDOWN_PLACEHOLDER += f"- {results[idx]['href']}\n"
            else:
                video_links.extend(link_from_search)

            if not link_from_img_search:
                MARKDOWN_PLACEHOLDER += f"- {img_results[idx]['url']}\n"
            else:
                video_links.extend(link_from_img_search)

            img_links.append(img_results[idx]["image"])

        BODY += """\n<instructions>The above results might contain irrelevant information. Determine the relevance of the information and respond to the user accordingly.
                Do not include the text within brackets in your response. </instructions>"""

        return BODY, img_links, video_links, MARKDOWN_PLACEHOLDER


# BODY, img_links, video_links, MARKDOWN_PLACEHOLDER = search_the_web(
#     "give me info about peter cat kolkata", max_results=3, region="ie-en"
# )
