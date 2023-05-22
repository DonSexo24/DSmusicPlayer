from DSnest import HashMap


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Users:
    def __init__(self, filename):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        users = HashMap[str, User]()
        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()
                for line in lines:
                    username, password = line.strip().split(":")
                    user = User(username, password)
                    users.put_in(username, user)
        except FileNotFoundError:
            pass
        return users

    def save_users(self):
        with open(self.filename, "w") as file:
            for user in self.users:
                file.write(f"{user.username}:{user.password}\n")
                print(user.username, user.password)

    def put(self, username, user):
        self.users.put_in(username, user)
        self.save_users()

    def get(self, username):
        return self.users.get(username)

    def contains(self, username: str):
        return self.users.contains_key(username)
