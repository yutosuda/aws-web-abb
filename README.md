# 画像アップロード＆閲覧Webアプリ（AWS上構築）

## プロジェクト概要

このプロジェクトは、ユーザーがWebブラウザから画像ファイルをアップロードし、アップロード済み画像を一覧・閲覧できるWebアプリケーションをAWS上に構築するものです。

## 主な機能

- 🖼️ **画像アップロード**: ブラウザから画像ファイル（jpg, png, gif等）をアップロード
- 📱 **画像一覧表示**: アップロード済み画像をサムネイル形式で一覧表示
- 🔍 **画像閲覧**: サムネイルクリックで元画像を表示
- 🗑️ **画像削除**: 不要な画像の削除（発展機能）

## 技術スタック

### フロントエンド
- HTML/CSS/JavaScript
- Bootstrap 5.3（モダンなUI）

### バックエンド
- Python 3.12
- Flask 3.0（軽量Webフレームワーク）
- SQLAlchemy 2.0（データベースORM）

### AWS サービス
- **EC2**: Webアプリケーションホスティング
- **S3**: 画像ファイルストレージ
- **IAM**: アクセス権限管理
- **VPC**: ネットワーク設定

## セットアップ手順

### 1. 仮想環境の作成
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集して必要な設定を行う
```

### 4. データベースの初期化
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. アプリケーションの起動
```bash
flask run
```

## プロジェクト構造

```
aws-web-abb/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── image.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── upload.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── upload.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── run.py
```

## セキュリティ機能

- 🔒 **S3バケット**: パブリックアクセス完全禁止
- 🔑 **署名付きURL**: 安全な画像アクセス
- 🛡️ **ファイル検証**: アップロード時の形式・サイズチェック
- 🚫 **CSRF保護**: クロスサイトリクエストフォージェリ対策

## 開発者向け情報

### 初心者向け学習ポイント

1. **Webアプリケーション開発**
   - Flask フレームワークの基本
   - MVC アーキテクチャパターン
   - RESTful API 設計

2. **AWSクラウドサービス**
   - EC2 インスタンス管理
   - S3 オブジェクトストレージ
   - IAM 権限管理

3. **セキュリティ**
   - ファイルアップロードの安全な実装
   - アクセス制御とデータ保護

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 