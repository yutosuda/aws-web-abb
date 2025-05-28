import os
from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app, abort, Response
from app.models.image import Image
from app import db

# メインページ用のブループリント
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    メインページ - 画像一覧を表示
    """
    # ページネーション用のパラメータ
    page = request.args.get('page', 1, type=int)
    per_page = 12  # 1ページあたりの画像数
    
    # 画像を新しい順で取得
    images = Image.query.order_by(Image.upload_date.desc()).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template('index.html', images=images)

@main_bp.route('/image/<int:image_id>')
def image_detail(image_id):
    """
    画像詳細ページ
    """
    image = Image.query.get_or_404(image_id)
    return render_template('image_detail.html', image=image)

@main_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    アップロードされた画像ファイルを表示
    
    Args:
        filename (str): 画像ファイル名
    
    Returns:
        Response: 画像ファイルのレスポンス
    """
    try:
        # 絶対パスを使用してアップロードフォルダを取得
        upload_folder = os.path.abspath(current_app.config['UPLOAD_FOLDER'])
        
        # セキュリティチェック: ファイルが存在するか確認
        file_path = os.path.join(upload_folder, filename)
        
        current_app.logger.info(f"画像ファイルパス: {file_path}")
        current_app.logger.info(f"ファイル存在確認: {os.path.exists(file_path)}")
        
        if not os.path.exists(file_path):
            current_app.logger.warning(f"ファイルが見つかりません: {file_path}")
            return Response("File not found", status=404, mimetype='text/plain')
        
        # 安全にファイルを送信
        return send_from_directory(upload_folder, filename)
    
    except Exception as e:
        current_app.logger.error(f"画像表示エラー: {str(e)}")
        return Response(f"Internal server error: {str(e)}", status=500, mimetype='text/plain')

@main_bp.route('/api/images')
def api_images():
    """
    画像一覧をJSON形式で返すAPI
    """
    images = Image.query.order_by(Image.upload_date.desc()).all()
    return jsonify([image.to_dict() for image in images])

@main_bp.route('/api/image/<int:image_id>')
def api_image_detail(image_id):
    """
    特定の画像情報をJSON形式で返すAPI
    """
    image = Image.query.get_or_404(image_id)
    return jsonify(image.to_dict()) 