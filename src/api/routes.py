from flask import Flask, request, jsonify, Blueprint
from api.models import db, GuildMember

from api.helpers import get_access_token  # Import the token helper function
from functools import wraps
import os
import requests
import logging

api = Blueprint('api', __name__)

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API key-based authentication decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key and api_key == os.environ.get('API_KEY'):
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized"}), 401
    return decorated_function

@api.route('/get-guild-players', methods=['GET'])
@require_api_key
def get_guild_players():
    realm_slug = os.environ.get('WOW_REALM_SLUG')
    guild_name = os.environ.get('WOW_GUILD_NAME')

    # Log the API request
    logger.info("Accessing /get-guild-players endpoint")

    try:
        # Retrieve the access token
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
        
        roster_response = requests.get(guild_url, headers=headers, params=params)
        
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

            db.session.commit()  # Commit the changes to the database
            return jsonify({"members": filtered_members}), 200
        else:
            return jsonify({"error": "Failed to fetch guild roster", "status_code": roster_response.status_code}), 500
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"error": get_access_token() }), 500
