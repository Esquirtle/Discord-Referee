from datetime import datetime

class MatchLogic:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_match(self, team_a, team_b, match_time):
        match_id = self.db_manager.insert_match(team_a, team_b, match_time)
        return match_id

    def get_match(self, match_id):
        match = self.db_manager.fetch_match(match_id)
        return match

    def update_match(self, match_id, updates):
        self.db_manager.update_match(match_id, updates)

    def delete_match(self, match_id):
        self.db_manager.delete_match(match_id)

    def get_ongoing_matches(self):
        ongoing_matches = self.db_manager.fetch_ongoing_matches()
        return ongoing_matches

    def get_match_statistics(self, match_id):
        statistics = self.db_manager.fetch_match_statistics(match_id)
        return statistics

    def schedule_match(self, match_id, new_time):
        self.db_manager.schedule_match(match_id, new_time)

    def join_match(self, match_id, team_id):
        self.db_manager.add_team_to_match(match_id, team_id)

    def leave_match(self, match_id, team_id):
        self.db_manager.remove_team_from_match(match_id, team_id)

    def get_match_history(self, team_id):
        history = self.db_manager.fetch_match_history(team_id)
        return history

    def log_match_result(self, match_id, result):
        self.db_manager.update_match_result(match_id, result)

    def get_upcoming_matches(self):
        upcoming_matches = self.db_manager.fetch_upcoming_matches()
        return upcoming_matches

    def get_match_schedule(self):
        schedule = self.db_manager.fetch_match_schedule()
        return schedule

    def format_match_time(self, match_time):
        return match_time.strftime("%Y-%m-%d %H:%M:%S")