from datetime import datetime


class Category:
    def __init__(self, name: str, description: str, is_active: bool, create_at: datetime) -> None:
        self.name = name
        self.description = description
        self.is_active = is_active
        self.create_at = create_at
