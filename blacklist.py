from db import db


class TokenBlacklist(db.Model):
    __tablename__ = 'blacklist'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    
    def __init__(self, jti):
        self.jti = jti
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_jti(cls, jti):
        return cls.query.filter_by(jti=jti).first()