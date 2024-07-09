import streamlit as st

from knowledge_gpt.components.sidebar import sidebar

from knowledge_gpt.ui import (
    wrap_doc_in_html,
    is_query_valid,
    is_file_valid,
    is_open_ai_key_valid,
    display_file_read_error,
)

from knowledge_gpt.core.caching import bootstrap_caching

from knowledge_gpt.core.parsing import read_file
from knowledge_gpt.core.chunking import chunk_file
from knowledge_gpt.core.embedding import embed_files
from knowledge_gpt.core.qa import query_folder
from knowledge_gpt.core.utils import get_llm


EMBEDDING = "openai"
VECTOR_STORE = "faiss"
MODEL_LIST = ["gpt-3.5-turbo", "gpt-4"]

# Uncomment to enable debug mode
# MODEL_LIST.insert(0, "debug")

st.set_page_config(page_title="KnowledgeGPT", page_icon="📖", layout="wide")
st.header("📖KnowledgeGPT")

# Enable caching for expensive functions
bootstrap_caching()

sidebar()

openai_api_key = st.session_state.get("OPENAI_API_KEY")


if not openai_api_key:
    st.warning(
        "サイドバーに OpenAI API キーを入力します。キーは次の場所で入手できます"
        " https://platform.openai.com/account/api-keys."
    )


uploaded_file = st.file_uploader(
    "PDF、docx、または txt ファイルをアップロードする",
    type=["pdf", "docx", "txt"],
    help="スキャンされたドキュメントはまだサポートされていません。",
)

model: str = st.selectbox("Model", options=MODEL_LIST)  # type: ignore

with st.expander("オプション"):
    return_all_chunks = st.checkbox("ベクトル検索から取得したすべてのチャンクを表示")
    show_full_doc = st.checkbox("解析された文書の内容を表示する")


if not uploaded_file:
    st.stop()

try:
    file = read_file(uploaded_file)
except Exception as e:
    display_file_read_error(e, file_name=uploaded_file.name)

chunked_file = chunk_file(file, chunk_size=300, chunk_overlap=0)

if not is_file_valid(file):
    st.stop()


if not is_open_ai_key_valid(openai_api_key, model):
    st.stop()


with st.spinner("ドキュメントのインデックス作成中...これには時間がかかる場合があります⏳"):
    folder_index = embed_files(
        files=[chunked_file],
        embedding=EMBEDDING if model != "debug" else "debug",
        vector_store=VECTOR_STORE if model != "debug" else "debug",
        openai_api_key=openai_api_key,
    )

with st.form(key="qa_form"):
    query = st.text_area("書類について質問する")
    submit = st.form_submit_button("サブミット")


if show_full_doc:
    with st.expander("Document"):
        # Hack to get around st.markdown rendering LaTeX
        st.markdown(f"<p>{wrap_doc_in_html(file.docs)}</p>", unsafe_allow_html=True)


if submit:
    if not is_query_valid(query):
        st.stop()

    # Output Columns
    answer_col, sources_col = st.columns(2)

    llm = get_llm(model=model, openai_api_key=openai_api_key, temperature=0)
    result = query_folder(
        folder_index=folder_index,
        query=query,
        return_all=return_all_chunks,
        llm=llm,
    )

    with answer_col:
        st.markdown("#### Answer")
        st.markdown(result.answer)

    with sources_col:
        st.markdown("#### Sources")
        for source in result.sources:
            st.markdown(source.page_content)
            st.markdown(source.metadata["source"])
            st.markdown("---")
