import os
from app import create_app

# 環境変数から設定を取得（デフォルトは開発環境）
config_name = os.environ.get('FLASK_ENV', 'development')

# アプリケーションの作成
app = create_app(config_name)

if __name__ == '__main__':
    # 開発サーバーの起動
    app.run(
        host='0.0.0.0',  # 外部からのアクセスを許可
        port=5000,
        debug=True
    ) 