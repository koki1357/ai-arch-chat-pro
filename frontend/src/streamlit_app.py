import os
import streamlit as st
from dotenv import load_dotenv
from utils.path_setup import setup_backend_path
setup_backend_path()

from page_list import list_page, register_page, search_architecture_page  # noqa: E402

load_dotenv()


def main():
    st.set_page_config(
        page_title="Mr.Architect",
        page_icon="🤖",
        layout="wide"
    )

    # デフォルトのヘッダーを非表示にするCSS
    hide_streamlit_style = """
        <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    list_page_name = os.getenv('LIST_PAGE')
    register_page_name = os.getenv('REGISTER_PAGE')
    search_architecture_page_name = os.getenv('SEARCH_ARCHITECHURE_PAGE')

    # サイドバーでページ選択
    task = st.sidebar.selectbox(
        'タスクを選んでください！',
        options=[
            search_architecture_page_name,
            list_page_name,
            register_page_name],
        index=0
    )

    if task == register_page_name:
        register_page.run_page()
    elif task == list_page_name:
        list_page.run_page()
    elif task == search_architecture_page_name:
        search_architecture_page.run_page()


if __name__ == '__main__':
    main()
