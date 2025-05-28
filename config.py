import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

class Config:
    """基本設定クラス"""
    # セキュリティ用の秘密鍵
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # データベース設定
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ファイルアップロード設定
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB制限
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # AWS設定
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('AWS_REGION') or 'ap-northeast-1'
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

class DevelopmentConfig(Config):
    """開発環境用設定"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # SQLクエリをログ出力

class ProductionConfig(Config):
    """本番環境用設定"""
    DEBUG = False

class TestingConfig(Config):
    """テスト環境用設定"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# 設定の選択
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 