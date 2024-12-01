from typing import Dict, List, Tuple, Optional

from .llm_service import LLMService
from ..schemas import ChatMessage


class QuestionService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def process_question(
        self,
        question: str,
        system_context: Dict,
        chat_history: List[Dict]
    ) -> Tuple[bool, str, Optional[ChatMessage]]:
        """
        質問を処理して回答を生成
        Returns: (is_valid: bool, message: str, chat_message: Optional[ChatMessage])
        """
        # 質問の妥当性を検証
        is_valid, error_message = self.llm_service.validate_architecture_question(
            question,
            system_context
        )

        if not is_valid:
            return False, error_message, None

        # 回答を生成
        answer = self.llm_service.get_architecture_answer(question, system_context)

        chat_message = ChatMessage(
            role="assistant",
            content=answer
        )

        return True, answer, chat_message
