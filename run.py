import argparse
import json
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from src.model_langchain import HTPModel

TEXT_MODEL = "claude-3-5-sonnet-20240620"
MULTIMODAL_MODEL = "gpt-4o-2024-08-06"

def get_args():
    parser = argparse.ArgumentParser(description="HTP Model")
    parser.add_argument("--image_file", type=str, required=True , help="Path to the image")
    parser.add_argument("--save_path", type=str,required=True , help="Path to save the result")
    parser.add_argument("--language", type=str,required=True , default="zh", help="Language of the analysis report")
    
    return parser.parse_args()

load_dotenv()
config = get_args()

assert config.language in ["zh", "en"], "Language should be either 'zh' or 'en'."

text_model = ChatOpenAI(
    api_key='sk-zk24b495cde4d68ae134f94d6ae08964f3067d2e05279d61',
    base_url='https://api.zhizengzeng.com/v1',
    model = TEXT_MODEL,
    temperature=0.2,
    top_p = 0.75,
    seed=42,
)
multimodal_model = ChatOpenAI(
    api_key='sk-zk24b495cde4d68ae134f94d6ae08964f3067d2e05279d61',
    base_url='https://api.zhizengzeng.com/v1',
    model = MULTIMODAL_MODEL,
    temperature=0.2,
    top_p = 0.75,
    seed=42,
)

model = HTPModel(
    text_model=text_model,
    multimodal_model=multimodal_model,
    language=config.language,
    use_cache=True
)

result = model.workflow(
    image_path=config.image_file,
    language=config.language
)

# save the result to a file
with open(config.save_path, "w", encoding="utf-8") as f:
    f.write(json.dumps(result, indent=4, ensure_ascii=False))