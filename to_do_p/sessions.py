class Session:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self, session: str | None = None):
        self.session = session

    def add_session(self, user: str):
        self.session = user

    def check_session(self):
        return self.session
