ACADEMY_DATABASE = {
    "players": {
        "P001": {"name": "Marcus Johnson", "age": 19, "position": "CB", "years_played": 4, "level": "Advanced", "current_club": "Youth Academy FC"},
        "P002": {"name": "Sofia Martinez", "age": 18, "position": "CAM", "years_played": 3, "level": "Intermediate", "current_club": "Regional United"},
        "P003": {"name": "Ahmed Al-Rashid", "age": 20, "position": "ST", "years_played": 5, "level": "Elite", "current_club": "Development League"},
        "P004": {"name": "Elena Kowalski", "age": 17, "position": "GK", "years_played": 4, "level": "Intermediate", "current_club": "Junior Academy"},
        "P005": {"name": "Carlos Rivera", "age": 21, "position": "CM", "years_played": 4, "level": "Advanced", "current_club": "Premier Youth"},
    },
    "coaches": {
        "C001": {"name": "James Mitchell", "age": 35, "specialty": "Youth Development", "years_experience": 8, "level": "Senior"},
        "C002": {"name": "Maria Santos", "age": 28, "specialty": "Tactical Analysis", "years_experience": 5, "level": "Assistant"},
        "C003": {"name": "David Chen", "age": 42, "specialty": "Goalkeeping", "years_experience": 12, "level": "Head Coach"},
    }
}

def get_user_data(talent_id):
    if talent_id.startswith('P') and talent_id in ACADEMY_DATABASE["players"]:
        return ACADEMY_DATABASE["players"][talent_id], "player"
    elif talent_id.startswith('C') and talent_id in ACADEMY_DATABASE["coaches"]:
        return ACADEMY_DATABASE["coaches"][talent_id], "coach"
    return None, None