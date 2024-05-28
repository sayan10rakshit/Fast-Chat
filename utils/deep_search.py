import asyncio
import aiohttp
import re
import random
from bs4 import BeautifulSoup
import chardet  # For detecting the encoding of the HTML content


async def fetch_html(session, url, timeout):
    """
    Asynchronously fetches the HTML content of the given URL within a specified timeout.

    Parameters:
        session (aiohttp.ClientSession): The client session to use for the request.
        url (str): The URL to fetch.
        timeout (aiohttp.ClientTimeout): The timeout setting for the request.

    Returns:
        str: The HTML content of the page if the request is successful, None otherwise.
    """
    try:
        async with session.get(url, timeout=timeout) as response:
            if response.status == 200:
                raw_content = await response.read()
                detected_encoding = chardet.detect(raw_content)["encoding"]
                return raw_content.decode(detected_encoding, errors="ignore")
            else:
                print(f"Failed to fetch {url}: HTTP {response.status}")
                return None
    except asyncio.TimeoutError:
        print(f"Timeout error for {url}")
        return None
    except aiohttp.ClientError as e:
        print(f"Client error for {url}: {e}")
        return None


async def fetch_all_html(urls):
    """
    Asynchronously fetches the HTML content for a list of URLs.

    Parameters:
        urls (list of str): The list of URLs to fetch.

    Returns:
        list of str: The list of HTML contents for each URL.
    """
    timeout = aiohttp.ClientTimeout(
        total=5
    )  # Set the total timeout for each request to 5 seconds
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_html(session, url, timeout) for url in urls]
        return await asyncio.gather(*tasks)


def extract_paragraph_texts(html):
    """
    Extracts the text content of all <p> tags from the given HTML.

    Parameters:
        html (str): The HTML content to parse.

    Returns:
        list of str: The list of text contents from all <p> tags.
    """
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = []
    for p in soup.find_all("p"):
        text = p.get_text().strip()
        basic_cleaned_text = re.sub(
            "^\s+?", "", re.sub("\n", "", re.sub(r"\s+", " ", text))
        )
        if len(basic_cleaned_text.split()) > 10:
            paragraphs.append(basic_cleaned_text)

    # If there are many paragraphs, we randomly select 5 paragraphs
    if len(paragraphs) > 5:
        paragraphs = [random.choice(paragraphs) for _ in range(5)]
        return paragraphs
    return paragraphs


async def main(urls):
    """
    The main coroutine that fetches HTML content from a list of URLs and extracts
    text from <p> tags.

    Parameters:
        urls (list of str): The list of URLs to process.

    Returns:
        list of str: The aggregated list of paragraph texts from all URLs.
    """
    html_contents = await fetch_all_html(urls)
    all_paragraph_texts = []
    for html in html_contents:
        if html:
            paragraphs = extract_paragraph_texts(html)
            all_paragraph_texts.extend(paragraphs)
    return all_paragraph_texts


def fetch_text(urls: list) -> str:
    """
    Does a deep search on the given URLs and returns the refined paragraph texts.

    Args:
        urls (list): The list of URLs to search.

    Returns:
        list: The list of refined paragraph texts.
    """
    urls = [
        url
        for url in urls
        if "amazon." not in url
        and "flipkart." not in url
        and "youtube." not in url
        and "zomato." not in url
        and ".pdf" not in url
    ]  # Exclude Amazon and Flipkart URLs since they don't allow scraping
    for url in urls:
        print(f"Fetching text from {url}")
    paragraph_texts = asyncio.run(main(urls))
    text_body = " ".join(text for text in paragraph_texts)
    return text_body
