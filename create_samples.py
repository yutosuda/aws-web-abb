#!/usr/bin/env python3
"""
テスト用サンプル画像生成スクリプト
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_image(filename, size, color, text):
    """サンプル画像を生成"""
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    
    # テキストを中央に描画
    try:
        # デフォルトフォントを使用
        font = ImageFont.load_default()
    except:
        font = None
    
    # テキストのサイズを取得
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width, text_height = 100, 20
    
    # 中央に配置
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    # uploadsディレクトリに保存
    img.save(f'uploads/{filename}')
    print(f'サンプル画像を作成: uploads/{filename}')

def main():
    """メイン処理"""
    # uploadsディレクトリを作成
    os.makedirs('uploads', exist_ok=True)
    
    # 複数のサンプル画像を作成
    create_sample_image('sample1.jpg', (800, 600), '#3498db', 'Sample Image 1')
    create_sample_image('sample2.png', (600, 400), '#e74c3c', 'Sample Image 2')
    create_sample_image('sample3.jpg', (1024, 768), '#2ecc71', 'Sample Image 3')
    
    print('サンプル画像の作成が完了しました！')

if __name__ == '__main__':
    main() 