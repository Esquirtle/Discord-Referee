def is_valid_username(username):
    return isinstance(username, str) and 3 <= len(username) <= 20

def is_valid_team_name(team_name):
    return isinstance(team_name, str) and 3 <= len(team_name) <= 30

def is_valid_match_id(match_id):
    return isinstance(match_id, int) and match_id > 0

def is_valid_tournament_id(tournament_id):
    return isinstance(tournament_id, int) and tournament_id > 0

def is_valid_league_id(league_id):
    return isinstance(league_id, int) and league_id > 0

def is_valid_profile_data(profile_data):
    return isinstance(profile_data, dict) and 'username' in profile_data and is_valid_username(profile_data['username'])