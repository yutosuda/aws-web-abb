import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from werkzeug.utils import secure_filename
from PIL import Image as PILImage
from app.models.image import Image
from app import db

# アップロード用のブループリント
upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    """
    許可されたファイル形式かチェック
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def validate_image(file):
    """
    画像ファイルの検証
    """
    try:
        # PILで画像を開いて検証
        img = PILImage.open(file)
        img.verify()
        file.seek(0)  # ファイルポインタをリセット
        return True
    except Exception:
        return False

@upload_bp.route('/')
def upload_form():
    """
    アップロードフォームページ
    """
    return render_template('upload.html')

@upload_bp.route('/process', methods=['POST'])
def upload_file():
    """
    ファイルアップロード処理
    """
    if 'file' not in request.files:
        flash('ファイルが選択されていません', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    description = request.form.get('description', '')
    
    if file.filename == '':
        flash('ファイルが選択されていません', 'error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # ファイル検証
        if not validate_image(file):
            flash('有効な画像ファイルではありません', 'error')
            return redirect(request.url)
        
        # ファイルサイズチェック
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > current_app.config['MAX_CONTENT_LENGTH']:
            flash('ファイルサイズが大きすぎます（最大5MB）', 'error')
            return redirect(request.url)
        
        # 安全なファイル名の生成
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        try:
            # 現在はローカル保存（後でS3に変更）
            upload_folder = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            
            # データベースに保存
            new_image = Image(
                filename=unique_filename,
                original_filename=original_filename,
                file_size=file_size,
                content_type=file.content_type,
                description=description
            )
            
            db.session.add(new_image)
            db.session.commit()
            
            flash('画像が正常にアップロードされました！', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'アップロード中にエラーが発生しました: {str(e)}', 'error')
            return redirect(request.url)
    
    else:
        flash('許可されていないファイル形式です', 'error')
        return redirect(request.url)

@upload_bp.route('/api', methods=['POST'])
def api_upload():
    """
    API経由でのファイルアップロード
    """
    if 'file' not in request.files:
        return jsonify({'error': 'ファイルが選択されていません'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'ファイルが選択されていません'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': '許可されていないファイル形式です'}), 400
    
    if not validate_image(file):
        return jsonify({'error': '有効な画像ファイルではありません'}), 400
    
    try:
        # ファイル処理（上記と同様）
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # ファイルサイズ取得
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        # ローカル保存
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # データベース保存
        new_image = Image(
            filename=unique_filename,
            original_filename=original_filename,
            file_size=file_size,
            content_type=file.content_type,
            description=request.form.get('description', '')
        )
        
        db.session.add(new_image)
        db.session.commit()
        
        return jsonify({
            'message': '画像が正常にアップロードされました',
            'image': new_image.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'アップロード中にエラーが発生しました: {str(e)}'}), 500 