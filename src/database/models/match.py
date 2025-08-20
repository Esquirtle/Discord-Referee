class Match:
    def __init__(self, match_id, team_a, team_b, score_a=0, score_b=0, status='pending'):
        self.match_id = match_id
        self.team_a = team_a
        self.team_b = team_b
        self.score_a = score_a
        self.score_b = score_b
        self.status = status

    def update_score(self, score_a, score_b):
        self.score_a = score_a
        self.score_b = score_b
        self.status = 'completed'

    def get_match_info(self):
        return {
            'match_id': self.match_id,
            'team_a': self.team_a,
            'team_b': self.team_b,
            'score_a': self.score_a,
            'score_b': self.score_b,
            'status': self.status
        }