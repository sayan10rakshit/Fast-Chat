import os
import random
import time
import json
import logging

import groq
from groq import Groq
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import TimeoutException, DuckDuckGoSearchException

from utils.deep_search import fetch_text
from utils.extract_subs import filter_links

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

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


def summarize(
    content_from_links,
    model,
    max_tokens,
    api_key,
    objective="Summarize the following information crawled from several websites",
) -> str:
    """
    ## Summarize the information from the search results.

    ---

    **Args**
        - **content_from_links (str)**: The content extracted from the search results.
        - **model (str)**: The model to be used for summarization.
        - **max_tokens (int)**: The maximum number of tokens for the summarization.
        - **api_key (str)**: The API key for Groq API.
        - **objective (str)**: The objective for summarization.

    ---

    **Returns**
        - **distilled_info (str)**: The distilled information from the search results.
    """
    distilled_info = """"""

    client = Groq(api_key=api_key)

    try:
        messages = [
            {  #! Note that `Distillation` objective is the `Final` Objective
                "role": "user",
                "content": f"""
                #Distillation objective:
    `           {objective}

                #Additional instructions:
                - Retain all relevant descriptive information from the search content.
                - Include specific details such as numerical data, technical specifications, and feature comparisons.
                - Highlight any unique selling points or standout characteristics of the options being compared.
                - Present a balanced view, including both positive and negative aspects when available.
                - If certain important information is missing, note its absence.
                - Do not include any advertisements, sponsored content and disregard any irrelevant information that deviates from the distillation objective.
                - Distill the information as much as possible while maintaining clarity and coherence with respect to the distillation objective on the given search content.

                #Search content:
                {content_from_links}

                Based on the above objective and search content, provide a comprehensive distillation of the information, ensuring to include all relevant details and comparisons.
                """,
            }
        ]

        print("\n\n Waiting for 2 seconds before summarizing\n\n")
        time.sleep(2)

        #! Make this model constant by passing a parameter to the function
        print(f"\n\nModel selected for summarizing: {model}\n\n")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=1,
            max_tokens=max_tokens,
            top_p=0.9,
            stream=False,
            stop=None,
            seed=42,
        )
        distilled_info += response.choices[0].message.content

        return distilled_info

    except groq.RateLimitError:
        print("Rate limit error")
        return distilled_info

    except groq.AuthenticationError:
        print("Invalid API key")
        return distilled_info

    except groq.BadRequestError:
        print("Bad request error")
        return distilled_info

    except groq.InternalServerError:
        print("Internal server error")
        return distilled_info


def search_summary(
    search_queries,
    api_key,
    max_results=7,
    objective="summarize",
    region=REGIONS["India"],
) -> tuple:
    """
    ## Search the web using DuckDuckGo search engine and return the results.

    ---

    **Args**
        - **user_query (str)**: The query to search the web.
        - **max_results (int)**: The maximum number of results to return.
        - **region (str)**: The region to search in.
        - **api_key (str)**: The API key for Groq API.

    ---

    **Returns**
        - **body (str)**: The body containing information from the search results.
        - **img_links (list)**: The list of image links from the search results.
        - **video_links (list)**: The list of video links from the search results.
        - **markdown_placeholder (str)**: The placeholder containing the references to the search results.
    """
    if len(search_queries) > 0:
        all_info = """"""
        distilled_info = """"""
        all_img_links = []
        all_video_links = []
        all_markdown_placeholders = """"""

        for search_query in search_queries:
            try:
                video_links = []
                img_links = []
                url_list = []
                content_from_links = []
                markdown_placeholder = """"""

                logging.info(f"\n\nAttempting for query: {search_query}\n\n")

                text_results = DDGS().text(
                    search_query, region=region, max_results=max_results
                )

                img_results = DDGS().images(
                    keywords=search_query,
                    region=region,
                    # safesearch="on",
                    size=None,
                    type_image=None,
                    layout=None,
                    license_image=None,
                    max_results=max_results,
                )

                if text_results:
                    for _, search_result in enumerate(text_results):

                        if "href" in search_result.keys():
                            url_list.append(search_result["href"])
                            video_links_from_search = filter_links(
                                search_result["href"]
                            )

                            if not video_links_from_search:
                                markdown_placeholder += f"- [[**{search_result['title']}**]({search_result['href']})]\n"
                            else:
                                video_links.extend(video_links_from_search)

                if img_results:
                    for _, image_result in enumerate(img_results):
                        video_links_from_img_search = filter_links(image_result["url"])
                        if not video_links_from_img_search:
                            markdown_placeholder += f"- [[**{image_result['title']}**]({image_result['url']})]\n"
                        else:
                            video_links.extend(video_links_from_img_search)
                        img_links.append(image_result["image"])

                content_from_links = fetch_text(url_list)
                #! All the <p> text from each link fetched from a `search_query` among the `search_queries`
                all_info += (
                    f"""<info>Information from search query: {search_query}\n"""
                    + content_from_links
                    + "\n</info>"
                )

                img_links = list(set(img_links))
                all_img_links.extend(img_links)
                video_links = list(set(video_links))
                all_video_links.extend(video_links)
                all_markdown_placeholders += markdown_placeholder
                print("\n\n Waiting for 2 seconds before next search query\n\n")
                time.sleep(2)

            except DuckDuckGoSearchException as e:
                logging.error(f"Error occurred during DuckDuckGo search: {e}")
                return None, None, None, None
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
                return None, None, None, None

        model_list = [
            ("llama-3.2-90b-text-preview", 8192),
            ("llama-3.1-70b-versatile", 8000),
            ("llama-3.1-8b-instant", 8000),
            ("llama3-70b-8192", 8192),
            ("llama3-8b-8192", 8192),
            ("llama-3.2-11b-text-preview", 8192),
            ("mixtral-8x7b-32768", 32768),
        ]

        #! This is deliberately done to mitigate the rate limit errors faced for each model
        # * We can play around with the weights to see which model works best
        model, max_tokens = random.choices(
            model_list, weights=[1, 1, 1, 1, 1, 1, 1], k=1
        )[0]
        distilled_info += summarize(
            content_from_links=all_info,
            model=model,
            max_tokens=max_tokens,
            api_key=api_key,
            objective=objective,
        )

        return distilled_info, all_img_links, all_video_links, all_markdown_placeholders

    else:
        logging.error("No search query provided.")
        return None, None, None, None


def generate_search_strings(
    query: str,
    api_key,
) -> dict:
    """
    ## Generate search strings based on the user query

    ---

    **Args**
        - **query (str)**: The user query to be processed
        - **api_key (str)**: The API key for Groq API

    ---

    **Returns**
        - **json_response (dict)**: The JSON response containing the search strings
    """
    prompt = (
        """
        # Research LLM Prompt Template for JSON Output

        You are an advanced research assistant designed to break down user queries into structured search objectives and generate relevant search strings. Your task is to analyze the given prompt and create a plan for gathering information effectively, outputting the result in a specific JSON format.

        ## Instructions:

        1. Carefully read and understand the user's query.
        2. Break down the query into 1-3 main objectives. Each objective should represent a key aspect of the information needed to answer the query comprehensively. There should be no more than 3 objectives.
        3. For each objective, generate 1-3 search strings that would likely yield relevant information when used in a web search. There should not be more than 3 search strings per objective.
        4. Do not give duplicate search strings or objectives.
        5. Create a final objective that describes the main task to be applied to all search results (e.g., summarizing, comparing, analyzing).
        6. Format your response in JSON according to the structure provided below.

        ## JSON Output Structure:

        ```json
        {
        "objectives": [
            {
            "description": "Brief description of the first main information-gathering goal",
            "search_strings": [
                "First search string for Objective 1",
                "Second search string for Objective 1",
                "Third search string for Objective 1"
            ]
            },
            {
            "description": "Brief description of the second main information-gathering goal",
            "search_strings": [
                "First search string for Objective 2",
                "Second search string for Objective 2",
                "Third search string for Objective 3"
            ]
            }
        ],
        "final_objective": "Description of the main task to be applied to all search results"
        }
        ```

        ## Notes:

        - The number of objectives can range from 1 to 3, depending on the complexity of the query.
        - Each objective can have 1 to 3 search strings.
        - Ensure that each objective and search string is directly relevant to answering the user's query.
        - Use clear and concise language in your objectives and search strings.
        - Avoid redundancy in your search strings; each should focus on a different aspect or perspective of the objective.
        - The final objective should describe the overall task to be performed on the collected information (e.g., summarizing, comparing, analyzing).
        - Output only valid JSON without any additional text or explanations.

        Now, based on the user's query, generate the appropriate objectives, search strings, and final objective following this JSON structure.
            """
        + """\n The user prompt is: """
        + query
    )

    model_list = [
        ("llama-3.1-70b-versatile", 8000),
        ("llama3-groq-70b-8192-tool-use-preview", 8192),
        ("llama-3.2-90b-text-preview", 8192),
    ]

    #! This is deliberately done to mitigate the rate limit errors faced for each model
    model, max_tokens = random.choices(model_list, weights=[1, 1, 1], k=1)[0]
    print(f"\n\nModel selected for generating search strings: {model}\n\n")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=max_tokens,
        top_p=0.9,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
        seed=42,
    )

    try:
        json_response = json.loads(response.choices[0].message.content)
        print(f"\n\n{json.dumps(json_response, indent=5)}\n\n")
        return json_response
    except json.JSONDecodeError:
        logging.error("Error decoding JSON response.")
        return None


def agentic_search_crawler(objective_json: dict, api_key) -> tuple:
    """
    ## Perform an agentic search based on the user query.

    ---

    **Args**
        - **objective_json (dict)**: The JSON response containing the search strategy.
        - **api_key (str)**: The API key for Groq API.

    ---

    **Returns**
        - **total_distilled_info (str)**: The distilled information from the search results
        - **total_img_links (list)**: The list of image links from the search results
        - **total_video_links (list)**: The list of video links from the search results
        - **total_markdown_placeholders (str)**: The placeholder containing the references to the search results
    """

    total_distilled_info = (
        """<distilled_info>The following is the distilled information\n"""
    )
    total_img_links = []
    total_video_links = []
    total_markdown_placeholders = """"""

    if objective_json is not None:
        search_queries = None
        for objective in objective_json["objectives"]:
            distilled_info = """"""
            img_links = []
            video_links = []
            markdown_placeholders = """"""
            search_queries = objective["search_strings"]
            if len(search_queries) > 3:
                search_queries = search_queries[:3]  #! Limiting the search queries to 3

            distilled_info, img_links, video_links, markdown_placeholders = (
                search_summary(
                    search_queries,
                    objective=objective_json["final_objective"],
                    api_key=api_key,
                )
            )

            total_distilled_info += (
                f"""<objective>{objective["description"]}</objective>\n"""
                + distilled_info
            )
            total_distilled_info += """</distilled_info>"""

            total_img_links.extend(img_links)
            total_video_links.extend(video_links)
            total_markdown_placeholders += markdown_placeholders

    return (
        total_distilled_info,
        total_img_links,
        total_video_links,
        total_markdown_placeholders,
    )
