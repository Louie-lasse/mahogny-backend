import time
from .scraper import Scraper
import uuid


class Session_manager():

    SESSION_TIMEOUT = 1800  # 30 minutes

    def __init__(self) -> None:
        self.user_sessions = {}
    
    async def add_user_session(self, user: str, password: str) -> bool|str:
        s = Scraper()
        try:
            res = await s.login(user, password)
        except Exception as e:
            print(e)
            res = False
        finally:
            s.__exit__(None, None, None)
        if not res:
            return False
        # create uuid for session id
        session_id = str(uuid.uuid4())
        self.user_sessions[session_id] = (s, time.time())
        return session_id

    def clear_sessions(self) -> None:
        """
        Removes sessions older than 30 minutes
        """
        now = time.time()
        self.user_sessions = {k: v for k, v in self.user_sessions.items() if now - v[1] < self.SESSION_TIMEOUT}

    def get_session(self, session_id: str) -> Scraper|None:
        self.clear_sessions()
        if session_id in self.user_sessions:
            return self.user_sessions[session_id][0]
        return None
