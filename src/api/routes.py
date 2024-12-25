from flask import Flask, request, jsonify, Blueprint
from api.models import db, User, GuildMember
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests
import logging
from api.helpers import get_access_token  # Import the token helper function

api = Blueprint('api', __name__)

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Check if the user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    # Determine if the first user is admin
    is_admin = User.query.count() == 0  # First user becomes admin

    # Create a new user and hash the password
    new_user = User(username=username, email=email, is_admin=is_admin)
    new_user.set_password(password)  # Use the set_password method to hash the password

    # Add user to the database
    db.session.add(new_user)
    db.session.commit()

    first_user_created = User.query.count() == 1  # Check if this is the first user
    return jsonify({"message": "User created", "firstUserCreated": first_user_created}), 201


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Find the user in the database
    user = User.query.filter_by(email=email).first()

    # Validate user credentials
    if user and user.check_password(password):
        # Generate JWT token with user identity
        access_token = create_access_token(identity={"id": user.id, "is_admin": user.is_admin})
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    

@api.route('/check-users', methods=['GET'])
def check_users():
    try:
        users_count = User.query.count()
        return jsonify({"exists": users_count > 0}), 200
    except Exception as e:
        logger.error(f"Error checking users: {e}")
        return jsonify({"error": "Failed to check users"}), 500


@api.route('/get-guild-players', methods=['GET'])
@jwt_required()
def get_guild_players():
    # Retrieve the JWT identity to get user information
    current_user = get_jwt_identity()

    # Check if the user has admin privileges
    if not current_user.get("is_admin"):
        return jsonify({"error": "Unauthorized access"}), 403

    realm_slug = os.environ.get('WOW_REALM_SLUG')
    guild_name = os.environ.get('WOW_GUILD_NAME')

    # Log the API request
    logger.info("Accessing /get-guild-players endpoint")

    try:
        # Retrieve the access token using the helper function
        access_token = get_access_token()

        # Make the guild roster API request
        guild_url = f"https://eu.api.blizzard.com/data/wow/guild/{realm_slug}/{guild_name}/roster"
        headers = {
            'Authorization': f"Bearer {access_token}"
        }
        params = {
            'namespace': 'profile-eu',
            'locale': 'en_US'
        }

        # Send the request to the Blizzard API
        roster_response = requests.get(guild_url, headers=headers, params=params)

        # Check if the response is successful
        if roster_response.status_code == 200:
            # Process the response to filter the required data
            data = roster_response.json()
            guild_info = data.get("guild", {})
            faction = guild_info.get("faction", {}).get("name", "")
            guild_realm_name = guild_info.get("realm", {}).get("name", "")
            guild_realm_slug = guild_info.get("realm", {}).get("slug", "")

            members = data.get("members", [])
            filtered_members = []

            for member in members:
                character = member.get("character", {})
                level = character.get("level", 0)

                # Only include level 80 characters
                if level == 80:
                    filtered_member = {
                        "character_name": character.get("name"),
                        "guild_realm_name": guild_realm_name,
                        "guild_realm_slug": guild_realm_slug,
                        "playable_class_id": character.get("playable_class", {}).get("id"),
                        "playable_race_id": character.get("playable_race", {}).get("id"),
                        "guild_faction": faction,
                        "member_realm_slug": character.get("realm", {}).get("slug")
                    }
                    filtered_members.append(filtered_member)

                    # Save to the database
                    new_member = GuildMember(
                        character_name=filtered_member["character_name"],
                        guild_realm_name=filtered_member["guild_realm_name"],
                        guild_realm_slug=filtered_member["guild_realm_slug"],
                        playable_class_id=filtered_member["playable_class_id"],
                        playable_race_id=filtered_member["playable_race_id"],
                        guild_faction=filtered_member["guild_faction"],
                        member_realm_slug=filtered_member["member_realm_slug"]
                    )
                    db.session.add(new_member)

            # Commit the changes to the database
            db.session.commit()
            return jsonify({"members": filtered_members}), 200
        else:
            return jsonify({"error": "Failed to fetch guild roster", "status_code": roster_response.status_code}), 500

    except Exception as e:
        # Log and return the error
        logger.error(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500
