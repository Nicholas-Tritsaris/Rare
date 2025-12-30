import json
import shutil
from pathlib import Path

class AccountManager:
    def __init__(self, legendary_config_path="~/.config/legendary"):
        self.config_path = Path(legendary_config_path).expanduser()
        self.accounts_path = self.config_path / "accounts"
        self.accounts_path.mkdir(exist_ok=True)
        self.active_user_file = self.config_path / "user.json"
        self.active_account_store = self.config_path / "active_account.txt"

    def get_active_account_id(self):
        if self.active_account_store.exists():
            return self.active_account_store.read_text().strip()
        return None

    def set_active_account_id(self, account_id):
        self.active_account_store.write_text(account_id)

    def add_account(self):
        if not self.active_user_file.exists():
            return None

        with open(self.active_user_file, "r") as f:
            user_data = json.load(f)

        account_id = user_data.get("accountId")
        if not account_id:
            return None

        destination = self.accounts_path / f"{account_id}.json"
        shutil.copy(self.active_user_file, destination)
        self.set_active_account_id(account_id)
        return account_id

    def remove_account(self, account_id):
        account_file = self.accounts_path / f"{account_id}.json"
        if account_file.exists():
            account_file.unlink()

    def list_accounts(self):
        accounts = {}
        for account_file in self.accounts_path.glob("*.json"):
            with open(account_file, "r") as f:
                user_data = json.load(f)
            display_name = user_data.get("displayName", "Unknown")
            accounts[account_file.stem] = display_name
        return accounts

    def switch_account(self, account_id):
        account_file = self.accounts_path / f"{account_id}.json"
        if not account_file.exists():
            raise FileNotFoundError(f"Account '{account_id}' not found.")

        shutil.copy(account_file, self.active_user_file)
        self.set_active_account_id(account_id)

    def activate_last_used_account(self):
        last_active_id = self.get_active_account_id()
        if last_active_id:
            try:
                self.switch_account(last_active_id)
            except FileNotFoundError:
                self.active_account_store.unlink(missing_ok=True)
                self.active_user_file.unlink(missing_ok=True)
