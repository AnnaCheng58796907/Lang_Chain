import gradio as gr
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

# 初始化模型
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


def translate_text(source_language, target_language, domain, text):
    """
    翻譯文本的函數
    """
    try:
        # 格式化提示詞
        formatted_prompt = chat_prompt_template.format(
            source_language=source_language,
            target_language=target_language,
            domain=domain,
            text=text
        )

        # 調用模型
        response = model.invoke(formatted_prompt)

        return response
    except Exception as e:
        return f"翻譯過程中發生錯誤：{str(e)}"


# 定義語言選項
language_options = [
    "繁體中文", "簡體中文", "英文", "日文", "韓文",
    "法文", "德文", "西班牙文", "義大利文", "俄文"
]

domain_options = [
    "一般", "商業", "科技", "醫學", "法律",
    "文學", "學術", "新聞", "技術文件", "日常對話"
]

# 創建 Gradio 介面
with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="gray",
        neutral_hue="slate"
    ),
    title="AI 智能翻譯助手",
    css="""
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
    }
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .feature-box {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    """
) as interface:

    # 標題和說明
    gr.HTML("""
    <div class="main-header">
        <h1>🌐 AI 智能翻譯助手</h1>
        <p>專業的多語言翻譯服務，支援各種專業領域</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("""
            ### 📋 翻譯設定
            請選擇翻譯參數：
            """)

            # 輸入欄位
            source_lang = gr.Dropdown(
                choices=language_options,
                value="英文",
                label="🌍 源語言",
                info="選擇要翻譯的原始語言"
            )

            target_lang = gr.Dropdown(
                choices=language_options,
                value="繁體中文",
                label="🎯 目標語言",
                info="選擇要翻譯成的語言"
            )

            domain = gr.Dropdown(
                choices=domain_options,
                value="一般",
                label="📚 專業領域",
                info="選擇文本所屬的專業領域"
            )

            # 文本輸入
            input_text = gr.Textbox(
                label="📝 輸入文本",
                placeholder="請輸入要翻譯的文本...",
                lines=5,
                max_lines=10,
                info="支援長文本翻譯"
            )

            # 翻譯按鈕
            translate_btn = gr.Button(
                "🚀 開始翻譯",
                variant="primary",
                size="lg"
            )

            # 清除按鈕
            clear_btn = gr.Button(
                "🗑️ 清除",
                variant="secondary"
            )

        with gr.Column(scale=1):
            gr.Markdown("""
            ### 📄 翻譯結果
            翻譯完成後會顯示在這裡：
            """)

            # 輸出欄位
            output_text = gr.Textbox(
                label="✨ 翻譯結果",
                lines=10,
                interactive=False,
                show_copy_button=True
            )

            # 統計信息
            with gr.Row():
                char_count = gr.Textbox(
                    label="📊 字符數",
                    interactive=False,
                    scale=1
                )
                word_count = gr.Textbox(
                    label="📝 單詞數",
                    interactive=False,
                    scale=1
                )

    # 示例文本
    gr.Markdown("""
    ### 💡 使用範例
    """)

    with gr.Row():
        example_btn1 = gr.Button("📈 商業範例", variant="outline")
        example_btn2 = gr.Button("🔬 科技範例", variant="outline")
        example_btn3 = gr.Button("📚 學術範例", variant="outline")

    # 功能說明
    gr.Markdown("""
    ---
    ### 🔧 功能特色

    <div class="feature-box">
        <h4>🎯 專業翻譯</h4>
        <p>• 支援多種語言互譯</p>
        <p>• 針對不同專業領域優化</p>
        <p>• 保持原文語氣和風格</p>
    </div>

    <div class="feature-box">
        <h4>🤖 AI 驅動</h4>
        <p>• 使用先進的語言模型</p>
        <p>• 智能理解上下文</p>
        <p>• 提供高品質翻譯結果</p>
    </div>

    <div class="feature-box">
        <h4>⚡ 快速便捷</h4>
        <p>• 即時翻譯處理</p>
        <p>• 直觀的操作介面</p>
        <p>• 支援長文本翻譯</p>
    </div>
    """)

    # 事件處理
    def count_text(text):
        """計算文本統計信息"""
        if not text:
            return "0", "0"

        char_count = len(text)
        word_count = len(text.split())
        return str(char_count), str(word_count)

    def load_example(example_type):
        """載入示例文本"""
        examples = {
            "business": {
                "text": ("The quarterly revenue increased by 15% compared to "
                        "last year, demonstrating strong market performance "
                        "and customer satisfaction."),
                "source": "英文",
                "target": "繁體中文",
                "domain": "商業"
            },
            "tech": {
                "text": ("Machine learning algorithms can process vast amounts "
                        "of data to identify patterns and make predictions "
                        "with high accuracy."),
                "source": "英文",
                "target": "繁體中文",
                "domain": "科技"
            },
            "academic": {
                "text": ("The research methodology employed a mixed-methods "
                        "approach, combining quantitative surveys with "
                        "qualitative interviews to ensure comprehensive "
                        "data collection."),
                "source": "英文",
                "target": "繁體中文",
                "domain": "學術"
            }
        }

        example = examples.get(example_type, examples["business"])
        return (example["text"], example["source"], example["target"],
                example["domain"])

    # 綁定事件
    translate_btn.click(
        fn=translate_text,
        inputs=[source_lang, target_lang, domain, input_text],
        outputs=output_text
    )

    # 統計信息更新
    input_text.change(
        fn=count_text,
        inputs=input_text,
        outputs=[char_count, word_count]
    )

    # 清除功能
    clear_btn.click(
        fn=lambda: ("", "", "", ""),
        outputs=[input_text, output_text, char_count, word_count]
    )

    # 示例按鈕
    example_btn1.click(
        fn=lambda: load_example("business"),
        outputs=[input_text, source_lang, target_lang, domain]
    )

    example_btn2.click(
        fn=lambda: load_example("tech"),
        outputs=[input_text, source_lang, target_lang, domain]
    )

    example_btn3.click(
        fn=lambda: load_example("academic"),
        outputs=[input_text, source_lang, target_lang, domain]
    )


# 啟動介面
if __name__ == "__main__":
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        inbrowser=True
    )

