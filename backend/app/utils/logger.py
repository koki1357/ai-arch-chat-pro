import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime


class Logger:
    @staticmethod
    def setup_logger(name: str, log_dir: str = "logs") -> logging.Logger:
        """
        ロガーのセットアップ
        """
        # ログディレクトリの作成
        os.makedirs(log_dir, exist_ok=True)

        # ロガーの設定
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # ファイルハンドラの設定
        log_file = os.path.join(
            log_dir,
            f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)

        # フォーマッタの設定
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)

        # ハンドラの追加
        logger.addHandler(file_handler)

        return logger
