class User:
    def __init__(self, user_id: int, last_daily: str, message_counter: int):
        self.id = user_id
        self.last_daily = last_daily
        self.message_counter = message_counter