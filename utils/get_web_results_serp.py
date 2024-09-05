from serpapi import GoogleSearch
from concurrent.futures import ThreadPoolExecutor
from utils.deep_search import fetch_text
from utils.extract_subs import filter_links


# for formatting the search results
def perform_shallow_search(search_results: dict) -> tuple:
    body = """"""
    markdown_placeholder = """"""
    for idx, search_result in enumerate(search_results["organic_results"]):
        try:
            body += f"<result {idx}>\n{search_result['snippet']}\n</result {idx}>\n"
            markdown_placeholder += (
                f"- [**{search_result['source']}**]({search_result['link']})\n"
            )
        except Exception as e:
            markdown_placeholder += (
                f"- {search_result['link']}\n"  # If the source is not available
            )
            print(e)
    return body, markdown_placeholder


# for formatting the search results
def perform_deep_search(search_results: list) -> str:
    body = """"""
    markdown_placeholder = """"""
    all_links = []
    search_result_snippets = []
    for _, search_result in enumerate(search_results["organic_results"]):
        all_links.append(search_result["link"])
        search_result_snippets.append(search_result["snippet"])
        markdown_placeholder += (
            f"- [**{search_result['source']}**]({search_result['link']})\n"
        )

    paragraph_texts = fetch_text(all_links)
    body += """<instructions>Refer these results from the web and respond to the user: </instructions>\n"""
    body += paragraph_texts
    return body, markdown_placeholder


def search_the_web(
    num=10,
    deep_search=False,
    api_key=None,
    engine="google",
    q=None,
    google_domain="google.com",
    hl="en",
    gl="in",
    location="Kolkata, West Bengal, India",
    safe="off",
) -> tuple:
    """
    Search the web using Google search engine and return the results.

    Args:
        num (int): The maximum number of results to return.
        api_key (str): The API key for SerpApi.
        engine (str): The search engine to use.
        q (str): The query to search the web.
        google_domain (str): The Google domain to search in.
        hl (str): The language to search in.
        gl (str): The country to search in.
        location (str): The location to search in.
        safe (str): The safe search mode.
        deep_search (bool): Whether to perform a deep search or not.

    Returns:
        body (str): The body containing information from the search results.
        markdown_placeholder (str): The placeholder containing the references to the search results.
        related_questions (dict): The dict of related questions from the search results.
    """

    body_text = """"""
    markdown_placeholder = """"""
    related_questions = None

    if not api_key and q:
        body_text += f"Please provide an API key to search the web for {q}\n"
        return body_text, markdown_placeholder

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

        if "related_questions" in search_results.keys():
            related_questions = search_results["related_questions"]

        body_text += """<instructions>Refer these results from the web and respond to the user appropriately: </instructions>\n"""

        if "answer_box" in search_results.keys():
            body_text += (
                f"<major_info>{search_results['answer_box']['snippet']}</major_info>\n"
            )

        # if not deep_search:
        #     body, markdown_placeholder = perform_shallow_search(search_results)
        #     body_text += body
        #     return body_text, markdown_placeholder
        # else:
        try:  # ? Perform deep search by default; If an error occurs, perform a shallow search
            body, markdown_placeholder = perform_deep_search(search_results)
            if body:
                # If there are not enough words in the body, we perform a shallow search
                if len(body.split()) < 100:
                    body, markdown_placeholder = perform_shallow_search(search_results)
                    body_text += body
                    return (
                        body_text,
                        markdown_placeholder,
                        related_questions,
                    )  # ? Return the shallow search results
                print("Performed deep search!")
                body_text += body
                if (
                    len(body_text.split(" ")) > 4500
                ):  # ? Setting a hard limit of 4500 words, might need to adjust
                    # ! There is a potential to summarize the text here instead of truncating
                    # ! Use LLM for summarization
                    body_text = " ".join(body_text.split(" ")[:4500])
                    body_text += """\n<instructions>The above results might contain irrelevant information. Determine the relevance of the information and respond to the user accordingly.
                    Do not include the text within tags in your response. </instructions>"""
                return (
                    body_text,
                    markdown_placeholder,
                    related_questions,
                )  # ? Return the deep search results
            else:  # ? If the body is empty, perform a shallow search
                body, markdown_placeholder = perform_shallow_search(search_results)
                body_text += body
                body_text += """\n<instructions>The above results might contain irrelevant information. Determine the relevance of the information and respond to the user accordingly.
                    Do not include the text within tags in your response. </instructions>"""
                return body_text, markdown_placeholder, related_questions
        except Exception as e:
            print(e)
            print("Error in deep search. Performing shallow search.")
            body, markdown_placeholder = perform_shallow_search(search_results)
            body_text += """\n<instructions>The above results might contain irrelevant information. Determine the relevance of the information and respond to the user accordingly.
                    Do not include the text within tags in your response. </instructions>"""
            return body, markdown_placeholder, related_questions

    except Exception as e:
        body_text += f"An error occurred: {e}\n"
        print(e)
        return body_text, markdown_placeholder, related_questions


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
) -> list:
    """
    Search images using Google search engine and return the image links.

    Args:
        api_key (str): The API key for SerpApi.
        engine (str): The search engine to use.
        q (str): The query to search the web.
        google_domain (str): The Google domain to search in.
        hl (str): The language to search in.
        gl (str): The country to search in.
        location (str): The location to search in.
        safe (str): The safe search mode.
        tbm (str): The type of search (images).

    Returns:
        img_links (list): The list of image links.
    """
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
) -> list:
    """
    Search videos using Google search engine and return the video links.

    [extended_summary]

    Args:
        num (int): The maximum number of results to return.
        api_key (str): The API key for SerpApi.
        engine (str): The search engine to use.
        q (str): The query to search the web.
        google_domain (str): The Google domain to search in.
        hl (str): The language to search in.
        gl (str): The country to search in.
        location (str): The location to search in.
        safe (str): The safe search mode.
        tbm (str): The type of search (videos).
    Returns:
        video_links (list): The list of video links.
    """
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
    deep_search=False,
    max_results=10,
) -> tuple:
    """
    Search the web using Google search engine and return the results.

    This is the main function that orchestrates the search of the web using Google search engine.
    It uses the `search_the_web`, `search_images`, and `search_videos` functions to get the search results.

    Args:
        api_key (str): The API key for SerpApi.
        query (str): The query to search the web.
        location (str): The location to search in.
        max_results (int): The maximum number of results to return.

    Returns:
        body (str): The body containing information from the search results.
        img_links (list): The list of image links from the search results.
        video_links (list): The list of video links from the search results.
        MARKDOWN_PLACEHOLDER (str): The placeholder containing the references to the search results.
    """

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
        body, markdown_placeholder, related_questions = executor.submit(
            search_the_web,
            num=max_results,
            deep_search=deep_search,
            **params,
        ).result()
        print("Got the body and markdown_placeholder")
        img_links = executor.submit(search_images, tbm="isch", **params).result()
        print("Got the img_links")
        video_links = executor.submit(
            search_videos, num=max_results, tbm="vid", **params
        ).result()
        print("Got the video_links")
        if video_links:
            yt_links = filter_links(" ".join(video_links))

    return body, img_links, yt_links, markdown_placeholder, related_questions
