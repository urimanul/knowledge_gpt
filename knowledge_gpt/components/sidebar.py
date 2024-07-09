import streamlit as st

from knowledge_gpt.components.faq import faq
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()


def sidebar():
    with st.sidebar:
        #st.markdown('<span style="font-size: 14px;">使用方法</span>', unsafe_allow_html=True)
        
        st.markdown(
            "## 使用方法\n"
            "1. 以下に [OpenAI API キー](https://platform.openai.com/account/api-keys) を入力します🔑\n" # noqa: E501
            "2. PDF、docx、または txt ファイルをアップロードします📄\n"
            "3. ドキュメントについて質問してください💬\n"
        )

        flgCheck_A = st.checkbox('キー入力')
        if flgCheck_A:
            #st.text('Checkbox A has checked')
            api_key_input = st.text_input(
                "OpenAI API Key",
                type="password",
                disabled=False,
                placeholder="ここに OpenAI API キーを貼り付けます (sk-...)",
                help="APIキーはhttps://platform.openai.com/account/api-keys から取得できます。",  # noqa: E501
                value=os.environ.get("OPENAI_API_KEY", None)
                or st.session_state.get("OPENAI_API_KEY", ""),
            )
        else:
            # DBへ接続
            conn = mysql.connector.connect(
            user='smairuser',
            password='smairuser',
            host='www.ryhintl.com',
            database='smair',
            port=36000
            )

            # DBの接続確認
            if not conn.is_connected():
                raise Exception("MySQLサーバへの接続に失敗しました")

            cur = conn.cursor(dictionary=True)  # 取得結果を辞書型で扱う設定

            query__for_fetching = """
            SELECT api_key FROM openai_payload;
            """

            cur.execute(query__for_fetching)

            for fetched_line in cur.fetchall():
                st.session_state["OPENAI_API_KEY"] = fetched_line['api_key']

        cur.close()

        st.session_state["OPENAI_API_KEY"] = api_key_input

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "📖KnowledgeGPT を使用すると、自分のことについて質問できます。 "
            "文書を参照し、即座に引用して正確な回答を得ることができます。"
        )
        st.markdown(
            "このツールは開発中です。"
            "[GitHub](https://github.com/urimanul/knowledge_gpt/)でプロジェクトを展開しています。" 
        )
        
        st.markdown("---")

        faq()
