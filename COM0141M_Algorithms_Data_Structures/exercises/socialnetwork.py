import math
import queue
from typing import NamedTuple
from user import User

class Connection(NamedTuple):
    distance: int
    user: User


class SocialNetwork:

    def __init__(self, name: str):
        self._name = name
        self._users: dict[str, User] = {}

    def create_user(self, user_id: str, name: str) -> User:
        if user_id in self._users:
            raise ValueError(f"User {user_id} already exists in {self._users.keys()}")
        self._users[user_id] = User(user_id, name)
        return self._users[user_id]

    def get_user(self, id: str) -> User:
        if id not in self._users.keys():
            raise ValueError(f"User {id} does not exist in {self._users.keys()}")
        return self._users[id]

    def add_relationship(self, user_one_ID: str, user_two_ID: str) -> bool:
        if any([u not in self._users for u in [user_one_ID, user_two_ID]]):
            raise ValueError(f"User not in dict")
        
        return (
            self._users[user_one_ID].add_connection(user_two_ID) and
            self._users[user_two_ID].add_connection(user_one_ID)
        )

    def connexion_degree(self, source_id: str, target_id: str) -> int:
        if not any([u in self._users for u in [source_id, target_id]]):
            return -1

        q: queue.Queue[Connection] = queue.Queue()
        q.put(Connection(0, self.get_user(source_id)))

        visited: list[str] = []
        visited.append(source_id)

        while q.qsize():
            curr: Connection = q.get()
            if curr.distance > 3:
                return -1

            if curr.user.get_id() == target_id:
                return curr.distance

            for conn_id in curr.user.get_connections():
                conn: User = self.get_user(conn_id)
                if conn.get_id() not in visited:
                    q.put(Connection(curr.distance + 1, conn))
                    visited.append(conn.get_id())

        return -1

    def get_close_network(self, user_id: str) -> set[str]:
        if user_id not in self._users:
            return set()

        ret: set[str] = set()
        ret.add(user_id)
        starting_user = self.get_user(user_id)

        # first connections
        for uid in starting_user.get_connections():
            ret.add(uid)

        # second connections
        for uid in ret:
            ret.update(set([u for u in self.get_user(uid).get_connections()]))

        # third connections
        for uid in ret:
            ret.update(set([u for u in self.get_user(uid).get_connections()]))

        return ret

    def closeness(self, user_id: str) -> float:
        user = self.get_user(user_id)

        numerator = len(self._users) - 1
        denominator = 0

        for i in self._users:
            conn = self.connexion_degree(user_id, i)
            if conn != -1:
                denominator += conn

        return numerator / denominator

