from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, GuildMember  # Import the GuildMember model
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
import os
import requests

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


@api.route('/get-guild-players', methods=['GET'])
def get_guild_players():
    client_id = os.environ.get('BNET_CLIENT_ID')
    client_secret = os.environ.get('BNET_CLIENT_SECRET')
    realm_slug = os.environ.get('WOW_REALM_SLUG')
    guild_name = os.environ.get('WOW_GUILD_NAME')
    
    # Check if required environment variables are set
    if not all([client_id, client_secret, realm_slug, guild_name]):
        return jsonify({"error": "Missing environment variables"}), 400

    # Step 1: Obtain the access token
    try:
        token_response = requests.post(
            'https://oauth.battle.net/token',
            auth=(client_id, client_secret),
            data={'grant_type': 'client_credentials'}
        )
        
        if token_response.status_code != 200:
            return jsonify({"error": "Failed to fetch token", "status_code": token_response.status_code}), 500
        
        # Extract the access token from the response
        access_token = token_response.json().get('access_token')
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "An error occurred while requesting the token", "details": str(e)}), 500

    # Step 2: Make the guild roster API request
    guild_url = f"https://eu.api.blizzard.com/data/wow/guild/{realm_slug}/{guild_name}/roster"
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    params = {
        'namespace': 'profile-eu',
        'locale': 'en_US'
    }
    
    try:
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
            # Return an error if the guild roster API request fails
            return jsonify({"error": "Failed to fetch guild roster", "status_code": roster_response.status_code}), 500
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "An error occurred while requesting guild roster", "details": str(e)}), 500
