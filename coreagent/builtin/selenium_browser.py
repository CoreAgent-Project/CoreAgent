from openai import Client as OpenAIClient
from selenium.webdriver.common.by import By
from seleniumbase import SB

def web_to_markdown(client: OpenAIClient, model: str, url: str):
  with SB(uc=True, incognito=True) as sb:
    sb.get(url)
    elem = sb.find_element(By.TAG_NAME, "body")
    text = elem.text
  resp = client.chat.completions.create(
    model=model,
    messages=[
      {"role": "system",
       "content": "You are a text-to-markdown converter, your input will be scraped Internet web page in plain text, your task is to convert them into organised markdown form. Your output should be directly a markdown file without putting them into a code block of markdown, but you can have code blocks inside your markdown file if the original web page has them. "},
      {"role": "user", "content": text},
    ],
    temperature=0.6,
    top_p=0.9,
    max_tokens=8192,
    # extra_body={"chat_template_kwargs": {"enable_thinking": False}},
  )
  return resp.choices[0].message.content

class SeleniumBrowser:
  def __init__(self, client: OpenAIClient, llm_model: str):
    self.client = client
    self.llm_model = llm_model
  def browse_web_get_markdown(self, url: str):
    """
    # Open a browser and convert the web page to structured markdown format.
    url: "The URL to read. "
    """
    return {'url': url, 'markdown': web_to_markdown(self.client, self.llm_model, url)}