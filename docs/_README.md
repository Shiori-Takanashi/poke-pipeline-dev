# ドキュメント索引

このディレクトリには、Poke-Pipeline プロジェクトの各ディレクトリとファイルに関する詳細なドキュメントが格納されています。

## ドキュメント一覧

### 主要ディレクトリ解説

- **[config-directory.md](./config-directory.md)** - 設定ファイル（`config/`）の解説
- **[src-directory.md](./src-directory.md)** - ソースコード（`src/`）の解説
- **[util-directory.md](./util-directory.md)** - ユーティリティ（`util/`）の解説
- **[tests-directory.md](./tests-directory.md)** - テストコード（`tests/`）の解説

### データディレクトリ解説

- **[json-directory.md](./json-directory.md)** - JSONデータ（`json/`）の解説
- **[database-directory.md](./database-directory.md)** - データベース（`database/`）の解説
- **[meta-directory.md](./meta-directory.md)** - メタデータ（`meta/`）の解説

### その他

- **[other-directories.md](./other-directories.md)** - その他のディレクトリとファイルの解説

## 読み方ガイド

### 新規参加者向け
1. **プロジェクト概要**: まず `README.md` を読んでプロジェクトの全体像を把握
2. **設定の理解**: `config-directory.md` で設定ファイルの構造を理解
3. **コード構造**: `src-directory.md` でメインコードの構造を理解
4. **データ形式**: `json-directory.md` と `database-directory.md` でデータの形式を理解

### 開発者向け
1. **開発環境**: `other-directories.md` で開発ツールとワークフローを確認
2. **テスト**: `tests-directory.md` でテスト手法を理解
3. **ユーティリティ**: `util-directory.md` で再利用可能な機能を確認
4. **デバッグ**: `other-directories.md` のデバッグ手法を参照

### 運用者向け
1. **データベース**: `database-directory.md` でデータベース管理を理解
2. **設定管理**: `config-directory.md` で設定の変更方法を確認
3. **メタデータ**: `meta-directory.md` でマッピング情報を理解
4. **監視**: `other-directories.md` でパフォーマンス監視を確認

## 更新ガイドライン

### ドキュメント更新のタイミング
- 新機能追加時
- 設定変更時
- ディレクトリ構造変更時
- 重要なバグ修正時

### 更新手順
1. 対象のドキュメントファイルを特定
2. 変更内容を反映
3. 他のドキュメントとの整合性を確認
4. 索引（この ファイル）の更新

### 記述スタイル
- **見出し**: 階層的な構造を維持
- **コード例**: 実際に動作するコードを記載
- **リンク**: 関連するファイルやドキュメントへのリンク
- **注意点**: 重要な制約や注意事項を明記

## 貢献方法

### ドキュメント改善
1. **不明な点の質問**: Issue で質問を投稿
2. **誤りの報告**: Pull Request で修正を提案
3. **追加情報**: 不足している情報を補完
4. **サンプル追加**: 実用的な使用例を追加

### レビュープロセス
1. **技術的正確性**: コードと実装の整合性確認
2. **可読性**: 初心者にも理解しやすい記述
3. **完全性**: 必要な情報の網羅性確認
4. **最新性**: 現在のコードベースとの同期

## 関連リソース

### 外部ドキュメント
- [PokeAPI 公式ドキュメント](https://pokeapi.co/docs/v2)
- [aiohttp ドキュメント](https://docs.aiohttp.org/)
- [SQLite ドキュメント](https://www.sqlite.org/docs.html)

### 開発ツール
- [Python 公式ドキュメント](https://docs.python.org/3/)
- [pytest ドキュメント](https://docs.pytest.org/)
- [Black フォーマッター](https://black.readthedocs.io/)

### プロジェクト管理
- GitHub Issues: バグ報告と機能要求
- GitHub Projects: 開発スケジュール管理
- GitHub Actions: CI/CD パイプライン

---

**最終更新**: 2025年7月1日
**バージョン**: 1.0.0
**メンテナー**: プロジェクトチーム
