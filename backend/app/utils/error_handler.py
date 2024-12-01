from typing import Dict, Any
import traceback
import logging


class ErrorHandler:
    @staticmethod
    def handle_error(error: Exception, context: Dict[str, Any] = None) -> Dict[str, str]:
        """
        エラーハンドリングとログ記録
        """
        error_id = str(hash(str(error)))

        # エラーの詳細をログに記録
        logging.error(f"Error ID: {error_id}")
        logging.error(f"Error Type: {type(error).__name__}")
        logging.error(f"Error Message: {str(error)}")
        if context:
            logging.error(f"Context: {context}")
        logging.error(f"Traceback: {traceback.format_exc()}")

        # クライアントへの応答を生成
        return {
            "error_id": error_id,
            "error_type": type(error).__name__,
            "message": str(error)
        }
