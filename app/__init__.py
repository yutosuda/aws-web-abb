from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import config

# 拡張機能の初期化
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_name='default'):
    """
    Flaskアプリケーションファクトリー
    
    Args:
        config_name (str): 設定名 ('development', 'production', 'testing')
    
    Returns:
        Flask: 設定済みのFlaskアプリケーション
    """
    app = Flask(__name__)
    
    # 設定の読み込み
    app.config.from_object(config[config_name])
    
    # 拡張機能の初期化
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # ブループリントの登録
    from app.routes.main import main_bp
    from app.routes.upload import upload_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(upload_bp, url_prefix='/upload')
    
    # エラーハンドラーの登録
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # アプリケーションコンテキスト内でのデータベーステーブル作成
    with app.app_context():
        # モデルのインポート（循環インポートを避けるため）
        from app.models import image
        
        # データベーステーブルの作成
        db.create_all()
    
    return app 