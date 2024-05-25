from serpapi import GoogleSearch
from concurrent.futures import ThreadPoolExecutor


def search_the_web(
    num=10,
    api_key=None,
    engine="google",
    q=None,
    google_domain="google.com",
    hl="en",
    gl="in",
    location="Kolkata, West Bengal, India",
    safe="off",
):
    body = """"""
    MARKDOWN_PLACEHOLDER = """"""

    if not api_key and q:
        body += f"Please provide an API key to search the web for {q}\n"
        return body, MARKDOWN_PLACEHOLDER

    try:
        search_results = GoogleSearch(
            {
                "api_key": api_key,
                "engine": engine,
                "q": q,
                "google_domain": google_domain,
                "hl": hl,
                "gl": gl,
                "location": location,
                "safe": safe,
                "num": num,
            }
        ).get_dict()

        body += """<instructions>Refer these results from the web and respond to the user: </instructions>\n"""

        for idx, search_result in enumerate(search_results["organic_results"]):
            body += f"<result {idx}>\n{search_result['snippet']}\n</result {idx}>\n"
            try:
                MARKDOWN_PLACEHOLDER += (
                    f"- [**{search_result['source']}**]({search_result['link']})\n"
                )
            except Exception as e:
                MARKDOWN_PLACEHOLDER += (
                    f"- **{search_result['source']}** : {search_result['link']}\n"
                )
                print(e)

        body += """\n<instructions>The above results might contain irrelevant information. Determine the relevance of the information and respond to the user accordingly.
                        Do not include the text within brackets in your response. </instructions>"""

        return body, MARKDOWN_PLACEHOLDER

    except Exception as e:
        body += f"An error occurred: {e}\n"
        print(e)
        return body, MARKDOWN_PLACEHOLDER


def search_images(
    api_key=None,
    engine="google",
    q=None,
    google_domain="google.com",
    hl="en",
    gl="in",
    location="Kolkata, West Bengal, India",
    safe="off",
    tbm="isch",
):
    img_links = []

    if not api_key and q:
        return img_links

    try:
        img_search_results = GoogleSearch(
            {
                "api_key": api_key,
                "engine": engine,
                "q": q,
                "google_domain": google_domain,
                "hl": hl,
                "gl": gl,
                "location": location,
                "safe": safe,
                "tbm": tbm,
            }
        ).get_dict()

        for _, image_result in enumerate(img_search_results["images_results"]):
            img_links.append(image_result["original"])

        return img_links
    except Exception as e:
        return img_links


def search_videos(
    num=10,
    api_key=None,
    engine="google",
    q=None,
    google_domain="google.com",
    hl="en",
    gl="in",
    location="Kolkata, West Bengal, India",
    safe="off",
    tbm="vid",
):
    video_links = []

    if not api_key and q:
        return video_links

    try:
        video_search_results = GoogleSearch(
            {
                "api_key": api_key,
                "engine": engine,
                "q": q,
                "google_domain": google_domain,
                "hl": hl,
                "gl": gl,
                "location": location,
                "safe": safe,
                "tbm": tbm,
                "num": num,
            }
        ).get_dict()

        for _, video_result in enumerate(video_search_results["video_results"]):
            video_links.append(video_result["link"])
        return video_links

    except Exception as e:
        print(e)
        return video_links


def get_web_results(
    api_key=None,
    query=None,
    location="Kolkata, West Bengal, India",
    max_results=10,
):

    params = {
        "api_key": api_key,
        "engine": "google",
        "q": query,
        "google_domain": "google.com",
        "hl": "en",
        "gl": "in",
        "location": location,
        "safe": "off",
    }

    with ThreadPoolExecutor() as executor:
        body, MARKDOWN_PLACEHOLDER = executor.submit(
            search_the_web, num=max_results, **params
        ).result()
        img_links = executor.submit(search_images, tbm="isch", **params).result()
        video_links = executor.submit(
            search_videos, num=max_results, tbm="vid", **params
        ).result()

    return body, img_links, video_links, MARKDOWN_PLACEHOLDER
