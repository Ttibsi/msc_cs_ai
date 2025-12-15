from typing import NamedTuple
import queue
from user import User

class Connection(NamedTuple):
    distance: int
    user: User


class SocialNetwork:
    _name: str
    _users: dict[str, User] = {}

    def __init__(self, name: str):
        self._name = name

    def create_user(self, id: str, name: str) -> User:
        if id in self._users:
            raise ValueError("user already exists")
        self._users[id] = User(id, name)
        return self._users[id]

    def get_user(self, id: str) -> User:
        if id not in self._users:
            raise ValueError("user not found")
        return self._users[id]

    def add_relationship(self, user_one_ID: str, user_two_ID: str) -> bool:
        if not any(u in self._users for u in [user_one_ID, user_two_ID]):
            raise ValueError("Incorrect user ID provided")
        
        return (
            self._users[user_one_ID].add_connection(user_two_ID) and
            self._users[user_two_ID].add_connection(user_one_ID)
        )

    def connexion_degree(self, source_id: str, target_id: str) -> int:
        if not any([u in self._users for u in [source_id, target_id]]):
            return -1

        q = queue.Queue()
        q.put(Connection(0, self.get_user(source_id)))

        visited: list[str] = []
        visited.append(source_id)
        distance = 0

        while len(q):
            curr = q.get()
            if curr.dist > 3:
                return -1

            if curr.user.get_id() == target_id:
                return curr.dist

            for conn in curr.user.get_connections():
                if conn.get_id() not in visited:
                    q.put(Connection(dist + 1, conn))
                    visited.append(conn.get_id())

        return -1

    def get_close_network(self, user_id: str) -> set[str]:
        if user_id not in self._users:
            return set()

        ret = set()

        return ret


