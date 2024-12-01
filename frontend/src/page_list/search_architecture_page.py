import os
import requests
import streamlit as st

from dotenv import load_dotenv
from typing import Dict, List

from utils.session_state_manager import SessionStateManager
from backend.app.domain.services.embedding_service import EmbeddingService
from backend.app.domain.services.llm_service import LLMService

load_dotenv()

AZURE_FUNCTION_URL = os.getenv('AZURE_FUNCTION_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def fetch_all_systems() -> List[Dict]:
    """Azure Functionsから全システムを取得"""
    try:
        response = requests.get(f"{AZURE_FUNCTION_URL}/select-all-system")
        if response.status_code == 200:
            return response.json()["documents"]
        return []
    except Exception as e:
        st.error(f"システムの取得中にエラーが発生しました: {str(e)}")
        return []


def run_page():
    SessionStateManager.initialize_states()

    # サービスの初期化
    embedding_service = EmbeddingService(OPENAI_API_KEY)
    llm_service = LLMService(OPENAI_API_KEY)

    st.title("システムアーキテクチャ検索・相談")

    # システム概要入力セクション
    st.subheader("📝 システム概要")
    new_description = st.text_area(
        "検討中のシステム概要を入力してください...",
        value=SessionStateManager.get_state('current_system_description'),
        height=150,
        key="system_description"
    )

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        search_clicked = st.button(
            "🔍 全件検索",
            key="search_button",
            help="入力されたシステム概要に類似したシステムを検索します"
        )
    with col2:
        vector_search_clicked = st.button(
            "🔍 ベクトル検索",
            key="vector_search_button",
            help="入力内容をベクトル化して類似度の高い上位3件を表示します"
        )

    if search_clicked or vector_search_clicked:
        if not new_description.strip():
            st.error("システム概要を入力してください。")
            return

        SessionStateManager.set_state('current_system_description', new_description)
        with st.spinner("類似システムを検索中..."):
            # 全システムを取得して類似度計算
            all_systems = fetch_all_systems()
            if all_systems:
                results = embedding_service.calculate_similarity(new_description, all_systems)
                
                if vector_search_clicked:
                    # ベクトル検索の場合は上位3件のみを表示
                    results = results[:3]
                    st.success(f"類似度の高い上位{len(results)}件のシステムを表示します")
                else:
                    st.success(f"{len(results)}件のシステムが見つかりました")
                
                SessionStateManager.set_state('search_results', results)
            else:
                st.error("システムの検索中にエラーが発生しました。")

    # 検索結果セクション
    results = SessionStateManager.get_state('search_results')
    if results:
        st.subheader("🎯 検索結果")
        for idx, system in enumerate(results):
            with st.expander(
                f"{system['system_name']} (類似度: {system.get('similarity', 0):.1f}%)",
                expanded=idx == 0  # 最初の結果のみ展開
            ):
                st.markdown(f"""
                **クラウドプロバイダー:** {system['cloud_provider']}
                **チーム:** {system['team']['primary']}
                **説明:** {system['description']}
                """)

                st.markdown("**利用サービス:**")
                services_cols = st.columns(3)
                for i, service in enumerate(system['cloud_services']):
                    with services_cols[i % 3]:
                        st.markdown(f"- {service}")

                if st.button("このシステムについて質問する", key=f"select_{system['id']}"):
                    SessionStateManager.set_state('selected_system', system)
                    SessionStateManager.clear_chat_history()
                    st.success(f"{system['system_name']}について質問できます")

    # チャットセクション
    selected_system = SessionStateManager.get_state('selected_system')
    if selected_system:
        st.subheader("💬 システムについての質問")

        # チャット履歴の表示
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(chat["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(chat["content"])

        # 質問入力
        with st.container():
            question = st.text_input(
                "質問を入力してください...",
                key="question_input",
                placeholder="例: このシステムのスケーラビリティについて教えてください"
            )

            col1, col2 = st.columns([1, 5])
            with col1:
                send_clicked = st.button(
                    "送信",
                    key="send_question",
                    help="質問を送信します"
                )

            if send_clicked and question:
                with st.spinner("回答を生成中..."):
                    # 質問の妥当性を検証
                    is_valid, error_message = llm_service.validate_architecture_question(
                        question,
                        selected_system
                    )

                    if is_valid:
                        # 質問を履歴に追加
                        SessionStateManager.add_chat_message("user", question)

                        # 回答を生成
                        answer = llm_service.get_architecture_answer(
                            question,
                            selected_system
                        )

                        # 回答を履歴に追加
                        SessionStateManager.add_chat_message("assistant", answer)
                        st.rerun()
                    else:
                        st.error(error_message)


if __name__ == "__main__":
    run_page()
