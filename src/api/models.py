from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # hashed password
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)  # new field for admin

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class GuildMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(100), nullable=False)
    guild_realm_name = db.Column(db.String(100), nullable=False)
    guild_realm_slug = db.Column(db.String(100), nullable=False)
    playable_class_id = db.Column(db.Integer, nullable=False)
    playable_race_id = db.Column(db.Integer, nullable=False)
    guild_faction = db.Column(db.String(50), nullable=False)
    member_realm_slug = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<GuildMember {self.character_name}>'

    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name,
            "guild_realm_name": self.guild_realm_name,
            "guild_realm_slug": self.guild_realm_slug,
            "playable_class_id": self.playable_class_id,
            "playable_race_id": self.playable_race_id,
            "guild_faction": self.guild_faction,
            "member_realm_slug": self.member_realm_slug,
        }
