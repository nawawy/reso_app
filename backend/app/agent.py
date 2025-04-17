import httpx
from config import SERPER_API_KEY, OPENAI_API_KEY
import nltk
import re
import json
import spacy
from utils import chunk_text
from newspaper import Article
from io import StringIO
import csv

from openai import OpenAI

nltk.download('punkt')

# Set OpenAI API key
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=OPENAI_API_KEY,
)

# Load the spaCy model
# Ensure you have the model installed: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

# Define the schema for the fields we want to extract
rule_fields = {"title", "authors", "date_of_birth"}



def scrape_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()

        return {
            "title": article.title,
            "text": article.text,
            "authors": article.authors,
            "publish_date": article.publish_date,
            "url": url
        }

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

def classic_extract(field, text):
    doc = nlp(text)

    if field == "title":
        return doc.ents[0].text if doc.ents else "Unknown Title"

    elif field == "authors":
        return list({ent.text for ent in doc.ents if ent.label_ == "PERSON"})

    elif field == "date_of_birth":
        for ent in doc.ents:
            if ent.label_ == "DATE" and re.search(r"\d{4}", ent.text):
                return ent.text
    return None

def openai_extract(text, field):
    if field == "summary":
        prompt = f"""
        You are a helpful data extractor.

        summarize the following text.
        Text:
        {text}
        """
    else:
        prompt = f"""
            You are a helpful data extractor.

            summarize the following text and extract the {field}.
            If the {field} is not present, return "Unknown".
            Text:
            {text}
            """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt[:5000]}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()

def hybrid_extract(text, schema):
    result = {}        
    for field in schema:
        print (f"Extracting field: {field}")
        try:
            if field in rule_fields:
                value = classic_extract(field, text)
                if not value:
                    value = openai_extract(text, field)
            else:
                value = openai_extract(text, field)
            result[field] = value
        except Exception as e:
            result[field] = f"Error: {str(e)}"
    return result
    
async def fetch_serper_results(prompt: str):
    """
    Asynchronous function to fetch search results from the Serper API
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://google.serper.dev/search",
                json={"q": prompt},
                headers={"X-API-KEY": SERPER_API_KEY},
            )
            response.raise_for_status()  # Raises an exception for HTTP errors
            return response.json().get("organic", [])
        except httpx.HTTPStatusError as http_error:
            print(f"HTTP error occurred: {http_error}")
        except httpx.RequestError as req_error:
            print(f"Request error occurred: {req_error}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return []  # Return an empty list in case of an error

async def run_agent(prompt: str, schema: str):
    # 1. Fetch search results from Serper API
    schema_obj = json.loads(schema)

    results = await fetch_serper_results(prompt)
    
    if not results:
        return {"error": "No results found or API request failed."}

    urls = [r["link"] for r in results[:5]]  # Take top 5 for now

    result_articles = []
    for url in urls:
        article_data = scrape_article(url)
        if article_data and article_data["text"]:

            data = hybrid_extract(article_data["text"], schema_obj)

            result_articles.append({
                "source_url": url,
                "title": article_data["title"],
                "extracted_schema": data
            })

    # Generate CSV content
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Source URL", "Title"] + schema_obj)  # Header row
    for article in result_articles:
        row = [article["source_url"], article["title"]]
        row.extend([article["extracted_schema"].get(field, "N/A") for field in schema_obj])
        writer.writerow(row)
    csv_content = output.getvalue()
    output.close()

    # Format text result
    text_result = "\n".join(
        [f"Source URL: {article['source_url']}\nTitle: {article['title']}\n" +
         "\n".join([f"{field}: {article['extracted_schema'].get(field, 'N/A')}" for field in schema_obj])
         for article in result_articles]
    ) or "No results available."

    return {"text_result": text_result, "csv_content": csv_content}

