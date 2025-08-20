def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

def calculate_win_rate(wins, losses):
    if wins + losses == 0:
        return 0
    return (wins / (wins + losses)) * 100

def paginate_list(items, page_size):
    for i in range(0, len(items), page_size):
        yield items[i:i + page_size]

def extract_user_id(user_mention):
    return int(user_mention.strip('<@!>')) if user_mention else None

def is_valid_team_name(name):
    return 3 <= len(name) <= 20 and name.isalnum()