# database/ ディレクトリ解説

このディレクトリには、処理済みのポケモンデータを格納するSQLiteデータベースファイルが保存されています。

## ファイル一覧

### poke.sqlite3
プロジェクトのメインデータベースファイルです。JSON形式で取得した生データを、リレーショナルな構造に変換して格納しています。

## データベース構造（推定）

### 主要テーブル

#### pokemon_species
ポケモンの種族情報を格納するマスターテーブル
- `species_id`: 種族ID (Primary Key)
- `name`: 種族名
- `generation_id`: 世代ID
- `evolves_from_species_id`: 進化前の種族ID
- `evolution_chain_id`: 進化チェーンID
- `color_id`: 色ID
- `shape_id`: 形状ID
- `habitat_id`: 生息地ID

#### pokemon
個々のポケモンの情報を格納するテーブル
- `pokemon_id`: ポケモンID (Primary Key)
- `species_id`: 種族ID (Foreign Key)
- `name`: ポケモン名
- `height`: 高さ
- `weight`: 重さ
- `base_experience`: 基礎経験値
- `order`: 図鑑順序

#### pokemon_stats
ポケモンの種族値情報
- `pokemon_id`: ポケモンID (Foreign Key)
- `stat_id`: ステータスID (Foreign Key)
- `base_stat`: 基礎値
- `effort`: 努力値

#### pokemon_types
ポケモンのタイプ情報
- `pokemon_id`: ポケモンID (Foreign Key)
- `type_id`: タイプID (Foreign Key)
- `slot`: タイプスロット（1st, 2nd）

#### abilities
特性情報のマスターテーブル
- `ability_id`: 特性ID (Primary Key)
- `name`: 特性名
- `generation_id`: 登場世代

#### pokemon_abilities
ポケモンと特性の関連テーブル
- `pokemon_id`: ポケモンID (Foreign Key)
- `ability_id`: 特性ID (Foreign Key)
- `is_hidden`: 隠れ特性フラグ
- `slot`: 特性スロット

#### types
タイプ情報のマスターテーブル
- `type_id`: タイプID (Primary Key)
- `name`: タイプ名
- `generation_id`: 登場世代

#### moves
技情報のマスターテーブル
- `move_id`: 技ID (Primary Key)
- `name`: 技名
- `generation_id`: 登場世代
- `type_id`: 技のタイプID
- `power`: 威力
- `pp`: PP
- `accuracy`: 命中率
- `priority`: 優先度

## データベースの利点

### パフォーマンス
- **インデックス**: 高速な検索・ソート
- **JOIN操作**: 複数テーブル間の効率的な結合
- **集計クエリ**: COUNT、SUM、AVG等の高速実行

### データ整合性
- **外部キー制約**: データの整合性保証
- **正規化**: データの重複排除
- **トランザクション**: データの一貫性確保

### クエリ例

```sql
-- 特定のポケモンの基本情報取得
SELECT p.name, ps.name as species_name, p.height, p.weight
FROM pokemon p
JOIN pokemon_species ps ON p.species_id = ps.species_id
WHERE p.pokemon_id = 25;  -- ピカチュウ

-- タイプ別ポケモン数の集計
SELECT t.name, COUNT(*) as pokemon_count
FROM types t
JOIN pokemon_types pt ON t.type_id = pt.type_id
GROUP BY t.type_id, t.name
ORDER BY pokemon_count DESC;

-- 特定の特性を持つポケモンの検索
SELECT p.name, a.name as ability_name
FROM pokemon p
JOIN pokemon_abilities pa ON p.pokemon_id = pa.pokemon_id
JOIN abilities a ON pa.ability_id = a.ability_id
WHERE a.name = 'static';  -- せいでんき

-- 進化チェーンの取得
SELECT ps1.name as evolves_from, ps2.name as evolves_to
FROM pokemon_species ps1
JOIN pokemon_species ps2 ON ps1.species_id = ps2.evolves_from_species_id
ORDER BY ps1.evolution_chain_id, ps1.species_id;
```

## 接続方法

### Python での接続
```python
import sqlite3

# データベースに接続
conn = sqlite3.connect('database/poke.sqlite3')
cursor = conn.cursor()

# クエリ実行
cursor.execute("SELECT name FROM pokemon WHERE pokemon_id = ?", (25,))
result = cursor.fetchone()

# 接続を閉じる
conn.close()
```

### pandas での活用
```python
import pandas as pd
import sqlite3

# データベースに接続
conn = sqlite3.connect('database/poke.sqlite3')

# DataFrameとして読み込み
df = pd.read_sql_query("""
    SELECT p.name, p.height, p.weight, ps.name as species
    FROM pokemon p
    JOIN pokemon_species ps ON p.species_id = ps.species_id
""", conn)

conn.close()
```

## メンテナンス

### バックアップ
```bash
# データベースのバックアップ
cp database/poke.sqlite3 database/poke_backup_$(date +%Y%m%d).sqlite3
```

### 最適化
```sql
-- インデックスの再構築
REINDEX;

-- 統計情報の更新
ANALYZE;

-- 不要領域の削除
VACUUM;
```

### データ更新
1. **増分更新**: 新しいデータのみ追加
2. **完全更新**: 全データの再構築
3. **差分管理**: 変更されたデータのみ更新

## 注意点

- **ファイルサイズ**: データ量の増加に注意
- **同時アクセス**: SQLiteは読み込み専用での同時アクセスに対応
- **バージョン管理**: 大きなバイナリファイルのため、Git LFS等の使用を検討
- **定期メンテナンス**: VACUUM実行でデータベースサイズの最適化
