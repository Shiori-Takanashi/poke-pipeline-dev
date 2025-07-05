# その他のディレクトリとファイル解説

## debug/ ディレクトリ

デバッグとトラブルシューティング用のスクリプトが格納されています。

### debug_fetch_target.py
データ取得機能のデバッグ用スクリプトです。

**主な機能:**
- 特定のエンドポイントのみをテスト実行
- API レスポンスの詳細確認
- エラーの詳細ログ出力
- パフォーマンス測定

**使用場面:**
- データ取得が失敗した時の原因調査
- 新しいエンドポイント追加時のテスト
- API 仕様変更の影響確認

## dev/ ディレクトリ

開発用のユーティリティとツールが格納されています。

### tree.py
プロジェクト構造の可視化ツールです。

**主な機能:**
- ディレクトリ構造の表示
- ファイルサイズ情報の表示
- 特定パターンのファイルフィルタリング
- Markdown 形式での出力

**使用例:**
```python
# プロジェクト全体の構造表示
python dev/tree.py

# 特定ディレクトリのみ表示
python dev/tree.py --path src/

# Python ファイルのみ表示
python dev/tree.py --filter "*.py"
```

## ルートディレクトリのファイル

### requirements.txt
プロダクション環境で必要なPythonパッケージの一覧です。

**主要な依存関係（推定）:**
```txt
aiohttp>=3.8.0      # 非同期HTTP通信
aiofiles>=0.8.0     # 非同期ファイル操作
tqdm>=4.64.0        # プログレスバー
pandas>=1.5.0       # データ分析
sqlite3             # データベース（標準ライブラリ）
```

**管理方法:**
```bash
# パッケージのインストール
pip install -r requirements.txt

# 現在の環境から requirements.txt を生成
pip freeze > requirements.txt

# 特定パッケージの更新
pip install --upgrade aiohttp
pip freeze | grep aiohttp >> requirements.txt
```

### requirements-test.txt
テスト環境で追加で必要なパッケージの一覧です。

**テスト関連パッケージ（推定）:**
```txt
pytest>=7.0.0       # テストフレームワーク
pytest-asyncio      # 非同期テスト対応
coverage>=6.0        # テストカバレッジ測定
mock>=4.0.0          # モックオブジェクト
pytest-mock         # pytest用モック
```

**使用方法:**
```bash
# テスト環境のセットアップ
pip install -r requirements.txt
pip install -r requirements-test.txt

# テスト実行
pytest tests/

# カバレッジ付きテスト
coverage run -m pytest tests/
coverage report
```

## 開発ワークフロー

### 環境構築
```bash
# 1. 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. 依存関係のインストール
pip install -r requirements.txt
pip install -r requirements-test.txt

# 3. プロジェクト構造の確認
python dev/tree.py
```

### 開発時のベストプラクティス

#### ブランチ戦略
```bash
# 機能開発用ブランチ
git checkout -b feature/new-endpoint

# バグ修正用ブランチ
git checkout -b bugfix/fetch-error

# ホットフィックス用ブランチ
git checkout -b hotfix/critical-bug
```

#### コード品質チェック
```bash
# フォーマッターの実行
black src/ tests/

# リンターの実行
flake8 src/ tests/

# 型チェック
mypy src/

# テスト実行
pytest tests/ -v
```

#### デバッグプロセス
```bash
# 1. 問題の再現
python debug/debug_fetch_target.py

# 2. ログの確認
grep "ERROR" logs/*.log

# 3. 特定機能のテスト
pytest tests/test_fetch_target.py::test_specific_case -v

# 4. デバッガーでの実行
python -m pdb src/fetch/fetch_target.py
```

## プロジェクト管理

### ディレクトリ監視
```bash
# ファイル変更の監視
find . -name "*.py" | entr -r python debug/debug_fetch_target.py
```

### パフォーマンス分析
```python
import cProfile
import pstats

# プロファイリング実行
cProfile.run('main_function()', 'profile_stats')

# 結果の分析
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative').print_stats(10)
```

### リソース使用量監視
```bash
# メモリ使用量の監視
python -m memory_profiler src/fetch/fetch_target.py

# CPU使用量の監視
top -p $(pgrep -f python)
```

## 注意点とトラブルシューティング

### よくある問題
1. **依存関係の競合**: requirements.txt の定期更新
2. **非同期処理のデッドロック**: セマフォとタイムアウトの調整
3. **メモリ不足**: 大量データ処理時のバッチサイズ調整
4. **API制限**: リクエスト頻度の制御

### 解決方法
```python
# メモリ効率的な処理
def process_data_in_chunks(data, chunk_size=1000):
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        yield process_chunk(chunk)

# エラーハンドリング
async def robust_fetch(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await fetch_data(url)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```
