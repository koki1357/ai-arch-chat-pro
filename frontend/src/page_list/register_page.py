import os
import streamlit as st

from dotenv import load_dotenv
from typing import Dict

from backend.app.domain.services.register_service import RegisterService
from backend.app.domain.services.embedding_service import EmbeddingService

load_dotenv()

AZURE_FUNCTION_URL = os.getenv('AZURE_FUNCTION_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def validate_system_data(data: Dict) -> tuple[bool, str]:
    """システムデータのバリデーション"""
    required_fields = ['system_name', 'description', 'cloud_provider', 'cloud_services', 'team', 'repository']

    # 必須フィールドチェック
    for field in required_fields:
        if field not in data:
            return False, f"必須フィールドが不足しています: {field}"

    # クラウドプロバイダーの値をチェック
    if data['cloud_provider'] not in ['AWS', 'Azure', 'GCP']:
        return False, "クラウドプロバイダーは AWS, Azure, GCP のいずれかである必要があります"

    return True, ""

def run_page():
    st.header("システムアーキテクチャ登録 📃")

    # サービスの初期化
    architecture_service = RegisterService(AZURE_FUNCTION_URL)
    embedding_service = EmbeddingService(OPENAI_API_KEY)

    with st.form("architecture_form"):
        # 基本情報
        st.subheader("基本情報")
        system_name = st.text_input("システム名", placeholder="例: 注文管理システム")
        description = st.text_area("システム説明", placeholder="システムの概要、目的、主要機能などを記述してください")

        # クラウド情報
        st.subheader("クラウド情報")
        cloud_provider = st.selectbox(
            "クラウドプロバイダー",
            options=['AWS', 'Azure', 'GCP']
        )

        # クラウドサービス
        services_input = st.text_area(
            "利用クラウドサービス",
            placeholder="サービスをカンマ区切りで入力 (例: EC2, S3, Lambda)",
            help="複数のサービスはカンマ(,)で区切って入力してください"
        )

        # チーム情報
        st.subheader("チーム情報")
        team_name = st.text_input("担当チーム名", placeholder="例: プラットフォームチーム")

        # リポジトリ情報
        st.subheader("リポジトリ情報")
        repository_url = st.text_input("アプリケーションリポジトリURL", placeholder="例: https://github.com/org/repo")

        submitted = st.form_submit_button("登録")

    if submitted:
        try:
            # クラウドサービスをリスト化
            cloud_services = [
                service.strip() 
                for service in services_input.split(",") 
                if service.strip()
            ]
            
            # Generate embedding for description
            description_vector = embedding_service.get_embedding(description)
            print(description_vector)
            # リクエストデータの作成
            architecture_data = {
                "system_name": system_name,
                "description": description,
                "description_vector": description_vector.tolist(),  # Convert numpy array to list
                "cloud_provider": cloud_provider,
                "cloud_services": cloud_services,
                "team": {
                    "primary": team_name
                },
                "repository": {
                    "application": repository_url
                }
            }

            # バリデーション
            is_valid, error_message = validate_system_data(architecture_data)

            if not is_valid:
                st.error(error_message)
                return

            # 登録処理
            with st.spinner("システムを登録中..."):
                result = architecture_service.register_system(architecture_data)

            # 成功メッセージとレスポンスの表示
            st.success("システムが正常に登録されました！")

            # 登録されたデータの表示
            with st.expander("登録されたデータ", expanded=True):
                st.json(result)

        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")

        # # デバッグ情報の表示（開発時のみ）
        # with st.expander("デバッグ情報", expanded=False):
        #     st.write("Request URL:", f"{architecture_service.base_url}/register-system")
        #     st.write("Request Data:")
        #     st.json(architecture_data)


if __name__ == "__main__":
    run_page()
