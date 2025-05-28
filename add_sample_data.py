#!/usr/bin/env python3
"""
サンプル画像データをデータベースに登録するスクリプト
"""

import os
from datetime import datetime
from app import create_app, db
from app.models.image import Image

def add_sample_images():
    """サンプル画像をデータベースに追加"""
    
    # サンプル画像の情報
    sample_images = [
        {
            'filename': 'sample1.jpg',
            'original_filename': 'サンプル画像1.jpg',
            'content_type': 'image/jpeg',
            'description': 'テスト用のサンプル画像です。青い背景に白いテキストが描かれています。'
        },
        {
            'filename': 'sample2.png',
            'original_filename': 'サンプル画像2.png',
            'content_type': 'image/png',
            'description': 'テスト用のサンプル画像です。赤い背景に白いテキストが描かれています。'
        },
        {
            'filename': 'sample3.jpg',
            'original_filename': 'サンプル画像3.jpg',
            'content_type': 'image/jpeg',
            'description': 'テスト用のサンプル画像です。緑の背景に白いテキストが描かれています。'
        }
    ]
    
    for img_data in sample_images:
        # ファイルが存在するかチェック
        file_path = os.path.join('uploads', img_data['filename'])
        if not os.path.exists(file_path):
            print(f"ファイルが見つかりません: {file_path}")
            continue
        
        # ファイルサイズを取得
        file_size = os.path.getsize(file_path)
        
        # 既に同じファイル名のレコードが存在するかチェック
        existing_image = Image.query.filter_by(filename=img_data['filename']).first()
        if existing_image:
            print(f"既に存在します: {img_data['filename']}")
            continue
        
        # 新しい画像レコードを作成
        new_image = Image(
            filename=img_data['filename'],
            original_filename=img_data['original_filename'],
            content_type=img_data['content_type'],
            file_size=file_size,
            description=img_data['description'],
            upload_date=datetime.utcnow()
        )
        
        # データベースに追加
        db.session.add(new_image)
        print(f"追加しました: {img_data['original_filename']} ({file_size} bytes)")
    
    # 変更をコミット
    try:
        db.session.commit()
        print("サンプル画像の登録が完了しました！")
    except Exception as e:
        db.session.rollback()
        print(f"エラーが発生しました: {e}")

def main():
    """メイン処理"""
    app = create_app()
    
    with app.app_context():
        # データベースの初期化
        db.create_all()
        
        # サンプル画像を追加
        add_sample_images()

if __name__ == '__main__':
    main() 