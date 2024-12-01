import requests
from typing import Tuple, Dict


class RegisterService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def validate_system_data(self, data: Dict) -> Tuple[bool, str]:
        """システムデータのバリデーション"""
        required_fields = [
            'system_name',
            'description',
            'cloud_provider',
            'cloud_services',
            'team',
            'repository'
        ]

        # 必須フィールドチェック
        for field in required_fields:
            if field not in data:
                return False, f"必須フィールドが不足しています: {field}"

        # チーム情報のチェック
        if not isinstance(data['team'], dict) or 'primary' not in data['team']:
            return False, "チーム情報にはprimaryフィールドが必要です"

        # リポジトリ情報のチェック
        if not isinstance(data['repository'], dict) or 'application' not in data['repository']:
            return False, "リポジトリ情報にはapplicationフィールドが必要です"

        # cloud_servicesが配列であることをチェック
        if not isinstance(data['cloud_services'], list) or not data['cloud_services']:
            return False, "cloud_servicesは空でない配列である必要があります"

        # cloud_providerの値をチェック
        if data['cloud_provider'] not in ['AWS', 'Azure', 'GCP']:
            return False, "cloud_providerは AWS, Azure, GCP のいずれかである必要があります"

        return True, ""

    def register_system(self, system_data: Dict) -> Dict:
        """システム情報を登録"""
        try:
            # バリデーション
            is_valid, error_message = self.validate_system_data(system_data)
            if not is_valid:
                raise ValueError(error_message)

            # APIリクエスト
            response = requests.post(
                f"{self.base_url}/register-system",
                json=system_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
            raise Exception(f"Failed to search systems: {str(e)}")
