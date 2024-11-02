from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, it's a security breach
        }

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
