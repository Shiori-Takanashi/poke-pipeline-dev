# Development Setup

このページでは、poke-pipelineの開発環境のセットアップ方法について説明します。

## 前提条件

### 必要なソフトウェア

- **Python 3.8+**: 開発言語
- **Git**: バージョン管理
- **Poetry** (推奨): パッケージ管理
- **VS Code** (推奨): 開発環境

### 推奨する開発環境

- **OS**: Linux, macOS, Windows WSL2
- **エディタ**: VS Code with Python extension
- **Terminal**: bash, zsh, or PowerShell

## 環境構築

### 1. プロジェクトのクローン

```bash
git clone <repository-url>
cd poke-pipeline
```

### 2. 仮想環境の設定

#### Poetry を使用する場合（推奨）

```bash
# Poetryのインストール
curl -sSL https://install.python-poetry.org | python3 -

# 依存関係のインストール
poetry install

# 仮想環境のアクティブ化
poetry shell
```

#### venv を使用する場合

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境のアクティブ化
source venv/bin/activate  # Linux/macOS
# または
venv\Scripts\activate     # Windows

# 依存関係のインストール
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### 3. 開発ツールの設定

#### pre-commit hooks の設定

```bash
# pre-commitのインストール
pip install pre-commit

# フックの設定
pre-commit install
```

#### VS Code の設定

`.vscode/settings.json` を作成：

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

## 開発ワークフロー

### 1. 新機能の開発

```bash
# 新しいブランチの作成
git checkout -b feature/new-feature

# 開発の実行
# ... コードの実装 ...

# コードの整形
black .
isort .

# リントの実行
flake8 .
mypy .

# テストの実行
pytest

# コミット
git add .
git commit -m "feat: add new feature"

# プッシュ
git push origin feature/new-feature
```

### 2. コード品質の管理

#### フォーマッタの実行

```bash
# Black（コードフォーマッタ）
black .

# isort（インポート整理）
isort .

# 両方を一度に実行
make format
```

#### リンターの実行

```bash
# flake8（構文チェック）
flake8 .

# mypy（型チェック）
mypy .

# 両方を一度に実行
make lint
```

### 3. テストの実行

```bash
# 全テストの実行
pytest

# カバレッジ付きテスト
pytest --cov=src

# 特定のテストファイルのみ実行
pytest tests/test_transform.py

# 詳細出力
pytest -v

# 並列実行
pytest -n auto
```

## 開発用ツール

### Makefile の活用

プロジェクトルートの `Makefile` を活用：

```bash
# 依存関係のインストール
make install

# 開発用依存関係のインストール
make install-dev

# コードの整形
make format

# リントの実行
make lint

# テストの実行
make test

# 全チェックの実行
make check-all

# ドキュメントの生成
make docs

# クリーンアップ
make clean
```

### デバッグ環境

#### Python デバッガの使用

```python
# コード内でのブレークポイント
import pdb; pdb.set_trace()

# または（Python 3.7+）
breakpoint()
```

#### VS Code デバッガの設定

`.vscode/launch.json` を作成：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Demo",
            "type": "python",
            "request": "launch",
            "module": "cli.demo",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/"],
            "console": "integratedTerminal"
        }
    ]
}
```

## 設定ファイル

### pyproject.toml

```toml
[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

### .flake8

```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    venv,
    .venv,
    build,
    dist
```

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
        language_version: python3.8

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.1
    hooks:
      - id: mypy
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. 依存関係のエラー

```bash
# キャッシュのクリア
pip cache purge

# 仮想環境の再作成
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. インポートエラー

```bash
# PYTHONPATHの設定
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# または、setup.pyを使用
pip install -e .
```

#### 3. テストエラー

```bash
# テストキャッシュのクリア
pytest --cache-clear

# 詳細な出力でデバッグ
pytest -vvv --tb=long
```

### 開発環境のリセット

```bash
# 全てのキャッシュとビルドファイルを削除
make clean

# 仮想環境の再作成
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt
```

## 継続的インテグレーション

### GitHub Actions の設定

`.github/workflows/ci.yml` の例：

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt

    - name: Run linting
      run: |
        black --check .
        isort --check-only .
        flake8 .
        mypy .

    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## 次のステップ

- [Testing](testing.md) - テストの書き方
- [Contributing](contributing.md) - コントリビューション方法
- [Usage](../usage.md) - 基本的な使用方法
