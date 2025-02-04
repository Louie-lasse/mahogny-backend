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
            await s.login(user, password)
        except Exception as e:
            print(e)
            return False
        finally:
            s.__exit__(None, None, None)

        session_id = str(uuid.uuid4())
        self.user_sessions[session_id] = (s, time.time())
        return session_id

    def clear_sessions(self) -> None:
        """
        Removes sessions older than 30 minutes
        """
        now = time.time()
        
        old = {k: v for k, v in self.user_sessions.items() if now - v[1] > self.SESSION_TIMEOUT}

        for k in old:
            old[k][0].__exit__(None, None, None)

        self.user_sessions = self.user_sessions - old

    def get_session(self, session_id: str) -> Scraper|None:
        self.clear_sessions()
        if session_id in self.user_sessions:
            return self.user_sessions[session_id][0]
        return None
