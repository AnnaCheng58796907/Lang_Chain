# 2. 多變數的複雜模板
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

model = OllamaLLM(model="gemma3:4b")

# 建立多變數的翻譯模板
complex_template = """
你是一位專業的{target_language}翻譯家，專精於{domain}領域。
請將以下{source_language}文本翻譯成{target_language}，並確保：
1. 保持原文的語氣和風格
2. 使用專業術語
3. 符合{target_language}的語言習慣

{source_language}文本：{text}
{target_language}翻譯：
"""

# 建立 ChatPromptTemplate
chat_prompt_template = ChatPromptTemplate.from_template(complex_template)

# 使用多個變數
formatted_prompt = chat_prompt_template.format(
    source_language="英文",
    target_language="繁體中文", 
    domain="商業",
    text="The quarterly revenue increased by 15% compared to last year."
)

response = model.invoke(formatted_prompt)

print("=== 多變數複雜模板範例 ===")
print(formatted_prompt)
print("\n" + "="*50)
print("Ollama gemma3:4b 模型回應:")
print(response)
