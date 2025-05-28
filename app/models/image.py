from datetime import datetime
from app import db

class Image(db.Model):
    """画像情報を管理するモデル"""
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.String(100), nullable=False)
    s3_key = db.Column(db.String(500), nullable=True)  # S3のオブジェクトキー
    s3_url = db.Column(db.String(1000), nullable=True)  # S3のURL
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Image {self.filename}>'
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'content_type': self.content_type,
            's3_key': self.s3_key,
            's3_url': self.s3_url,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'description': self.description
        } 