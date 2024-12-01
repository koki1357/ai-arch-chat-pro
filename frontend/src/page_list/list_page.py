import os
import requests
import streamlit as st
from typing import List, Dict


def fetch_architectures() -> List[Dict]:
    """Azure Functionsからアーキテクチャ一覧を取得"""
    try:
        url = os.getenv("AZURE_FUNCTION_URL") + "/select-all-system"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["documents"]
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return []


def run_page():
    st.header("システムアーキテクチャ一覧 📚")

    # システム一覧の取得
    with st.spinner("システム一覧を取得中..."):
        architectures = fetch_architectures()

    if not architectures:
        st.warning("システムが見つかりませんでした。")
        return

    # フィルタリングオプション
    st.subheader("フィルター設定")
    col1, col2 = st.columns(2)

    with col1:
        # クラウドプロバイダーでフィルター
        providers = list(set(arch["cloud_provider"] for arch in architectures))
        selected_provider = st.multiselect(
            "クラウドプロバイダー",
            options=providers,
            default=providers
        )

    with col2:
        # チームでフィルター
        teams = list(set(arch["team"]["primary"] for arch in architectures))
        selected_teams = st.multiselect(
            "チーム",
            options=teams,
            default=teams
        )

    # キーワード検索
    search_query = st.text_input(
        "🔍 「システム名」または「概要」で検索",
        placeholder="検索キーワードを入力..."
    ).lower()

    # フィルタリングの適用
    filtered_architectures = [
        arch for arch in architectures
        if arch["cloud_provider"] in selected_provider
        and arch["team"]["primary"] in selected_teams
        and (search_query == "" or
             search_query in arch["system_name"].lower() or
             search_query in arch["description"].lower())
    ]

    # 結果の表示
    st.subheader(f"システム一覧 ({len(filtered_architectures)}件)")

    if not filtered_architectures:
        st.info("条件に一致するシステムが見つかりませんでした。")
        return

    for arch in filtered_architectures:
        with st.expander(f"🏗️ {arch['system_name']}", expanded=False):
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown("**概要**")
                st.write(arch["description"])

            with col2:
                st.markdown("**基本情報**")
                st.write(f"📍 **プロバイダー:** {arch['cloud_provider']}")
                st.write(f"👥 **チーム:** {arch['team']['primary']}")
                if arch['repository']['application']:
                    st.write(f"📁 [リポジトリ]({arch['repository']['application']})")

            with col3:
                st.markdown("**利用サービス**")
                for service in arch["cloud_services"]:
                    st.write(f"• {service}")

            # メタデータの表示
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"🕒 **作成日時:** {arch['created_at'][:10]}")
            with col2:
                if arch['updated_at']:
                    st.write(f"🔄 **更新日時:** {arch['updated_at'][:10]}")

            # システムIDの表示（デバッグ用、必要に応じて非表示に）
            st.markdown(f"<small>System ID: {arch['id']}</small>", unsafe_allow_html=True)


if __name__ == "__main__":
    run_page()
