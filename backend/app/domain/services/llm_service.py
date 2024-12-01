from typing import Tuple, Dict
from openai import OpenAI
import json


class LLMService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def validate_architecture_question(self, question: str, system_context: Dict) -> Tuple[bool, str]:
        """システムアーキテクチャに関する質問かどうかを検証"""
        messages = [
            {
                "role": "system",
                "content": """
                あなたはシステムアーキテクチャの質問を検証する専門家です。
                入力された質問が、システムアーキテクチャ、設計、技術選択、スケーラビリティ、セキュリティ、
                デプロイメント、運用に関する質問であるかを判断してください。"""
            },
            {
                "role": "user",
                "content": f"""
                以下のシステムに対する質問が、システムアーキテクチャに関連する質問かどうかを判断してください。

                システム情報:
                {json.dumps(system_context, ensure_ascii=False)}

                質問:
                {question}

                回答は以下の形式で返してください：
                valid: true/false
                reason: 判断理由
                            """
            }
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=0
            )

            result = response.choices[0].message.content
            if "valid: true" in result.lower():
                return True, ""
            else:
                reason = result.split("reason:")[1].strip() if "reason:" in result else "システムアーキテクチャに関連しない質問です。"
                return False, reason

        except Exception as e:
            return False, f"検証中にエラーが発生しました: {str(e)}"

    def get_architecture_answer(self, question: str, system_context: Dict) -> str:
        """システムアーキテクチャに関する質問に回答"""
        messages = [
            {
                "role": "system",
                "content": f"""
                あなたはシステムアーキテクチャの専門家です。
                以下のシステムについて、アーキテクチャ、設計、技術選択、スケーラビリティ、
                セキュリティ、デプロイメント、運用の観点から質問に答えてください。

                システム情報:
                    - システム名: {system_context['system_name']}
                    - 説明: {system_context['description']}
                    - クラウドプロバイダー: {system_context['cloud_provider']}
                    - 利用サービス: {', '.join(system_context['cloud_services'])}"""
            },
            {
                "role": "user",
                "content": question
                }
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"回答の生成中にエラーが発生しました: {str(e)}"
