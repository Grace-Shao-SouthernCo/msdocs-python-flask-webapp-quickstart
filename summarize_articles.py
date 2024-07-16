import openai
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")



# headers for requests
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)

#split article text into chunks
def split_text(text):
    max_chunk_size = 2048
    chunks = []
    current_chunk = ""
    for sentence in text.split("."):
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def summarize_article(url):
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("summarizing")
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the main content of the article
        article = soup.find(class_='article-body') or soup.find('article') or soup.find('article-body') or soup.find('main')
        if article is None:
            return "No summary generated. Read more about the article at the provided URL."
        
        text = article.get_text()
        chunks = split_text(text)
        summaries = []
        for chunk in chunks:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Please summarize this text in five bullet points: {chunk}"}
                ]
            )
            summary = response.choices[0].message.content
            if summary.strip():  
                bullet_points = summary.split('\n')[:5]
                summaries.extend(bullet_points)
        return "\n".join(summaries[:5])
    else:
        return "URL error." # NOTE: some urls may not be printed
    