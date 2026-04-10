from openai import OpenAI
import os
import dotenv

# langchain的llm.with_structured_output其实是利用了大模型厂商API中对于结构化数据输出的支持，也就是以下代码当中传递的response_format参数
# 以下代码可以看到，对于不同的模型，传递response_format可能会报错
# 例如，OpenAI的闭源模型中，gpt-4o-mini支持response_format参数，但是早期模型gpt-3.5-turbo不支持。具体可以通过查看官方文档获取支持结构化输出的列表
# deepseek模型，暂不支持传递response_format参数
response_format_json_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "math_response",
        "schema": {
            "type": "object",
            "properties": {
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "explanation": {"type": "string"},
                            "output": {"type": "string"}
                        },

                    }
                },
                "final_answer": {"type": "string"}
            },
            "required": ["steps", "final_answer"]
        }
    }
}
dotenv.load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)
res = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "帮我算一下2x+12=38，x等于多少"}
    ],
    response_format=response_format_json_schema
)
print(res.choices[0].message.content)
