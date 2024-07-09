import streamlit as st

from knowledge_gpt.components.faq import faq
from dotenv import load_dotenv
import os

load_dotenv()


def sidebar():
    with st.sidebar:
        st.markdown(
            "## 使用方法\n"
            "1. 以下に [OpenAI API キー](https://platform.openai.com/account/api-keys) を入力します🔑\n" # noqa: E501
            "2. PDF、docx、または txt ファイルをアップロードします📄\n"
            "3. ドキュメントについて質問してください💬\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="ここに OpenAI API キーを貼り付けます (sk-...)",
            help="APIキーはhttps://platform.openai.com/account/api-keys から取得できます。",  # noqa: E501
            value=os.environ.get("OPENAI_API_KEY", None)
            or st.session_state.get("OPENAI_API_KEY", ""),
        )

        st.session_state["OPENAI_API_KEY"] = api_key_input

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "📖KnowledgeGPT を使用すると、自分のことについて質問できます。 "
            "文書を参照し、即座に引用して正確な回答を得ることができます。"
        )
        st.markdown(
            "このツールは開発中です。"
            "[GitHub](https://github.com/mmz-001/knowledge_gpt) でプロジェクトに貢献できます。 "  # noqa: E501
            "フィードバックや提案をお送りください💡"
        )
        st.markdown("Created by RYH")
        st.markdown("---")

        faq()
