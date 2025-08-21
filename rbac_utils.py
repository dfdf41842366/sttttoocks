import json
from pathlib import Path

RBAC_FILE = Path(__file__).parent / "rbac_sample.json"

def get_user_role(username):
    with open(RBAC_FILE) as f:
        data = json.load(f)
    for user in data["users"]:
        if user["username"] == username:
            return user["role"]
    return None

def can_access(username, operation):
    with open(RBAC_FILE) as f:
        data = json.load(f)
    role = get_user_role(username)
    for r in data["roles"]:
        if r["roleName"] == role:
            return operation in r["permissions"]
    return False

if __name__ == "__main__":
    print(can_access("alice", "deploy"))
    print(can_access("bob", "deploy"))
