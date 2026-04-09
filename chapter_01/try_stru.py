import os
from langchain.chat_models import init_chat_model
import dotenv

dotenv.load_dotenv()
# llm = init_chat_model(
#     model="openai/gpt-oss-20b:free",
#     model_provider="openai",
#     base_url="https://openrouter.ai/api/v1",
#     api_key="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",
# )
llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai",
    # base_url="https://openrouter.ai/api/v1",
    # api_key="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",
)

schema = {
    "name": "animal_list",
    "schema": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "animal": {"type": "string", "description": "动物名称"},
                "emoji": {"type": "string", "description": "动物的emoji表情"},
            },
            "required": ["animal", "emoji"],
        },
    },
}

messages = [{"role": "user", "content": "任意生成三种动物，以及他们的 emoji 表情"}]

llm_with_structured_output = llm.with_structured_output(
    schema, method="json_schema", include_raw=True
)
resp = llm_with_structured_output.invoke(messages)
print(resp)
print(resp["raw"])
print(resp["parsed"])
