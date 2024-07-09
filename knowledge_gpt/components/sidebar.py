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

        flgCheck_A = st.checkbox('登録キー参照')
        if flgCheck_A:
            # Input User ID
            SPOID = st.text_input(
                "SPOID",
                type="password",
                disabled=False,
                placeholder="SPOIDを入力",
                help="SPOID",  # noqa: E501
                ),
            )

            USER = st.text_input(
                "USERID",
                type="password",
                disabled=False,
                placeholder="USERIDを入力",
                help="USERID",  # noqa: E501
                ),
            )

            PASSKEY = st.text_input(
                "PASSKEY",
                type="password",
                disabled=False,
                placeholder="PASSKEYを入力",
                help="PASSKEY",  # noqa: E501
                ),
            )

            HOST = st.text_input(
                "HOST",
                type="text",
                disabled=False,
                placeholder="HOSTを入力",
                help="HOST",  # noqa: E501
                ),
            )

            DBNAME = st.text_input(
                "DBNAME",
                type="text",
                disabled=False,
                placeholder="DBNAMEを入力",
                help="DBNAME",  # noqa: E501
                ),
            )
            
            # DBへ接続
            conn = mysql.connector.connect(
            user=USER,
            password=PASSKEY,
            host=HOST,
            database=DBNAME,
            port=36000
            )

            flgButton = st.button('認証')
            if flgButton:
                # DBの接続確認
                if not conn.is_connected():
                    raise Exception("MySQLサーバへの接続に失敗しました")

                cur = conn.cursor(dictionary=True)  # 取得結果を辞書型で扱う設定

                query__for_fetching = """
                SELECT api_key FROM openai_payload;
                """

                cur.execute(query__for_fetching)

                for fetched_line in cur.fetchall():
                    #st.session_state["OPENAI_API_KEY"] = fetched_line['api_key']
                    api_key_input = fetched_line['api_key']

                cur.close()
            else:
                st.write("認証情報が正しくありません。")
        else:
            api_key_input = st.text_input(
                "OpenAI API Key",
                type="password",
                disabled=False,
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
            "[GitHub](https://github.com/urimanul/knowledge_gpt/)でプロジェクトを展開しています。" 
        )
        
        st.markdown("---")

        faq()
