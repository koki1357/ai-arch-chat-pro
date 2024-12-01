import sys
from pathlib import Path


def setup_backend_path():
    """
    バックエンドのパスをPYTHONPATHに追加
    """
    # 現在のファイルの場所から見た相対パスでプロジェクトルートディレクトリを探す
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent.parent.parent  # frontend/src/utils から3階層上がプロジェクトルート

    # プロジェクトルートをPYTHONPATHに追加
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"Added project root path: {project_root}")

    backend_path = project_root / 'backend'
    if not backend_path.exists():
        print(f"Warning: Backend directory not found at {backend_path}")
        return

    # 必要な__init__.pyファイルが存在することを確認
    required_init_files = [
        backend_path / '__init__.py',
        backend_path / 'app' / '__init__.py',
        backend_path / 'app' / 'domain' / '__init__.py',
        backend_path / 'app' / 'domain' / 'services' / '__init__.py',
    ]

    for init_file in required_init_files:
        if not init_file.exists():
            init_file.parent.mkdir(parents=True, exist_ok=True)
            init_file.touch()
            print(f"Created {init_file}")

    # 現在のPYTHONPATHを表示（デバッグ用）
    print("\nCurrent PYTHONPATH:")
    for path in sys.path:
        print(f"  - {path}")
