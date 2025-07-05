# Getting Started

このガイドでは、poke-pipelineプロジェクトの環境構築から基本的な使用方法まで説明します。

## 前提条件

- Python 3.8以上
- インターネット接続（PokéAPIへのアクセス用）
- Git（プロジェクトのクローン用）

## インストール

### 1. プロジェクトのクローン

```bash
git clone <repository-url>
cd poke-pipeline
```

### 2. 仮想環境の作成（推奨）

```bash
# venvを使用する場合
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# または、condaを使用する場合
conda create -n poke-pipeline python=3.10
conda activate poke-pipeline
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 開発用依存関係のインストール（開発者向け）

```bash
pip install -r requirements-test.txt
```

## 初期設定

### 設定ファイルの確認

プロジェクトの設定は `config/` ディレクトリに格納されています：

- `config/constant.py` - 定数定義
- `config/target.py` - 対象エンドポイント設定
- `config/dirpath.py` - ディレクトリパス設定
- `config/filepath.py` - ファイルパス設定

### データベースの初期化

```bash
# SQLiteデータベースファイルの場所を確認
ls database/
```

デフォルトでは `database/poke.sqlite3` にデータが格納されます。

## 基本的な使用方法

### 1. デモの実行

```bash
python -m cli.demo
```

### 2. データの取得

```bash
# 特定のポケモンデータを取得
python -m src.fetch.main --pokemon-id 1

# 全ポケモンデータを取得（時間がかかります）
python -m src.fetch.main --all
```

### 3. データの変換

```bash
# JSONデータの変換
python -m src.extract.transform
```

## ディレクトリ構成

```
poke-pipeline/
├── cli/                    # CLI関連
├── config/                 # 設定ファイル
├── database/              # データベースファイル
├── docs/                  # ドキュメント
├── json/                  # 取得したJSONデータ
├── logs/                  # ログファイル
├── src/                   # メインソースコード
│   ├── check/            # データチェック
│   ├── extract/          # データ抽出・変換
│   └── fetch/            # データ取得
├── tests/                # テストコード
└── util/                 # ユーティリティ
```

## 次のステップ

- [Usage](usage.md) - 詳細な使用方法
- [Architecture](architecture.md) - システム設計
- [API Reference](api/jsontransformer.md) - APIドキュメント
- [Examples](examples/basic.md) - 使用例

## トラブルシューティング

### よくある問題

**Q: `ModuleNotFoundError` が発生する**
A: Pythonパスの設定を確認してください。プロジェクトルートから実行していることを確認し、必要に応じて `PYTHONPATH` を設定してください。

**Q: API取得が失敗する**
A: インターネット接続を確認し、PokéAPIのステータスを確認してください。レート制限に引っかかっている可能性もあります。

**Q: データベースエラーが発生する**
A: `database/` ディレクトリの権限を確認し、SQLiteファイルが書き込み可能であることを確認してください。

## サポート

問題が発生した場合は、以下を確認してください：

1. エラーメッセージの詳細
2. 実行環境（Python バージョン、OS）
3. 実行したコマンド
4. ログファイルの内容（`logs/` ディレクトリ）
