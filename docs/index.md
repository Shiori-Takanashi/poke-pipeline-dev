# poke-pipeline

POKE-PIPELINE-DEVは、ポケモンのデータを対象としたETL（Extract-Transform-Load）パイプラインプロジェクトです。

Pythonによる非同期処理を活用し、**PokéAPI**（ポケモンの公開RESTful API）から大量のデータを効率的に取得・加工・格納することを目的としています。

## プロジェクト概要

**目的:** ポケモンの公式APIからデータを抽出し、扱いやすい形式で蓄積することで、データ分析やアプリケーション開発に活用できる基盤を構築すること。

**概要:** PokéAPI（[https://pokeapi.co](https://pokeapi.co)）が提供するポケモンに関する各種リソース（ポケモン、フォーム、種族、タイプ、ゲームバージョン等）のデータをETLパイプラインで収集します。

## 主な特徴

- **非同期処理**による高速なデータ取得
- **構造化データ**の保存とトランスフォーム
- **モジュール分離**による保守性の高い設計
- **型ヒント**と**テスト**による品質保証

## 技術スタック

- **言語:** Python 3.x
- **HTTPクライアント:** aiohttp（非同期処理）
- **データベース:** SQLite（将来的にPostgreSQL対応）
- **データモデル:** pydantic
- **CLI:** click, InquirerPy
- **開発ツール:** black, isort, flake8, mypy, pytest

## クイックスタート

```bash
# 依存関係のインストール
pip install -r requirements.txt

# デモ実行
python -m cli.demo
```

詳細は[Getting Started](getting-started.md)を参照してください。

## ドキュメント

- [Getting Started](getting-started.md) - 環境構築とセットアップ
- [Usage](usage.md) - 基本的な使用方法
- [Architecture](architecture.md) - システム設計について
- [API Reference](api/jsontransformer.md) - APIドキュメント
- [Examples](examples/basic.md) - 使用例

## ライセンス

このプロジェクトは個人の学習・ポートフォリオ目的で作成されています。
ポケモンに関する知的財産は任天堂等に帰属します。
