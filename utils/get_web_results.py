from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import TimeoutException, DuckDuckGoSearchException
from utils.extract_subs import filter_links
import time
import logging

# ! Experimental Section
# ? Uncomment the following code to use Groq API for generating search string
# import groq
# from groq import Groq

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

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def search_the_web(
    user_query,
    max_results=12,
    region="ie-en",
    # api_key=None,  # ? Can be used for an agent that returns appropriate search string
    retries=3,
    delay=2,
    backoff_factor=2,
) -> tuple:
    """
    Search the web using DuckDuckGo search engine and return the results.

    Args:
        user_query (str): The query to search the web.
        max_results (int): The maximum number of results to return.
        region (str): The region to search in.
        retries (int): The number of retries to attempt if an error occurs.
        delay (int): The delay between retries.
        backoff_factor (int): The factor to increase the delay between retries.
        api_key (str): The API key for Groq API.

    Returns:
        body (str): The body containing information from the search results.
        img_links (list): The list of image links from the search results.
        video_links (list): The list of video links from the search results.
        markdown_placeholder (str): The placeholder containing the references to the search results.
    """
    if user_query:
        query = user_query

        for attempt in range(retries):
            try:
                logging.info(f"Attempt {attempt + 1} for query: {query}")

                # ! Experimental Section
                # ? Uncomment the following code to use Groq API for generating search string
                # search_prompt = (
                #     "<instructions>Given the following query, return an appropriate search string: </instructions>\n"
                #     + query
                #     + "\n<instructions>Only return the search string, do not return any other information.</instructions>"
                # )

                # client = Groq(api_key=api_key)
                # messages = {"role": "user", "content": search_prompt}
                # chat_completion = client.chat.completions.create(
                #     model="llama3-70b-8192",
                #     messages=messages,
                #     max_tokens=50,
                # )
                # query = chat_completion.choices[0].message.content

                results = DDGS().text(query, region=region, max_results=max_results)
                img_results = DDGS().images(
                    keywords=query,
                    region=region,
                    safesearch="off",
                    size=None,
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

                # logging.info(f"Results: {results}")
                # logging.info(f"Image Results: {img_results}")

                return body, img_links, video_links, markdown_placeholder

            except TimeoutException as e:
                logging.error(
                    f"Timeout occurred: {e}. Retrying {attempt + 1}/{retries}..."
                )
                time.sleep(delay)
                delay *= backoff_factor  # Exponential backoff
            except DuckDuckGoSearchException as e:
                logging.error(f"Error occurred during DuckDuckGo search: {e}")
                return None, None, None, None
            # ! Experimental Section
            # ? Uncomment the following code to handle errors from Groq API
            # except groq.RateLimitError:
            #     logging.error("Rate limit error occurred. Retrying...")
            #     return None, None, None, None
            # except groq.AuthenticationError:
            #     logging.error("Authentication error occurred. Retrying...")
            #     return None, None, None, None
            # except groq.BadRequestError:
            #     logging.error("Bad request error occurred. Retrying...")
            #     return None, None, None, None
            # except groq.InternalServerError:
            #     logging.error("Internal server error occurred. Retrying...")
            #     return None, None, None, None
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
                return None, None, None, None

        logging.error("Failed to retrieve results after several attempts.")
        return None, None, None, None


# Example usage
# results = search_the_web("Tell me about apple")
# print(results)
