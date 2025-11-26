import reflex as rx
from typing import TypedDict, Optional
import asyncio


class User(TypedDict):
    id: str
    name: str
    email: str
    role: str
    avatar_seed: str


class AuthState(rx.State):
    users: list[dict] = [
        {
            "id": "u1",
            "name": "Admin User",
            "email": "admin@libmaster.com",
            "password": "password",
            "role": "admin",
            "avatar_seed": "Admin",
        },
        {
            "id": "u2",
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password",
            "role": "user",
            "avatar_seed": "John",
        },
    ]
    user: Optional[User] = None

    @rx.var
    def is_authenticated(self) -> bool:
        return self.user is not None

    @rx.var
    def is_admin(self) -> bool:
        return self.user is not None and self.user["role"] == "admin"

    is_auth_panel_open: bool = False
    auth_mode: str = "login"

    @rx.event
    def toggle_auth_panel(self):
        self.is_auth_panel_open = not self.is_auth_panel_open

    @rx.event
    def set_auth_mode(self, mode: str):
        self.auth_mode = mode

    @rx.event
    async def login(self, form_data: dict):
        email = form_data.get("email")
        password = form_data.get("password")
        found_user = next(
            (
                u
                for u in self.users
                if u["email"] == email and u["password"] == password
            ),
            None,
        )
        if found_user:
            self.user = {
                "id": found_user["id"],
                "name": found_user["name"],
                "email": found_user["email"],
                "role": found_user["role"],
                "avatar_seed": found_user["avatar_seed"],
            }
            self.is_auth_panel_open = False
            return rx.toast.success(f"Welcome back, {self.user['name']}!")
        else:
            return rx.toast.error("Invalid email or password")

    @rx.event
    async def register(self, form_data: dict):
        name = form_data.get("name")
        email = form_data.get("email")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")
        if password != confirm_password:
            return rx.toast.error("Passwords do not match")
        if any((u["email"] == email for u in self.users)):
            return rx.toast.error("Email already exists")
        import random

        new_user = {
            "id": f"u{random.randint(1000, 9999)}",
            "name": name,
            "email": email,
            "password": password,
            "role": "user",
            "avatar_seed": name,
        }
        self.users.append(new_user)
        self.user = {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "role": new_user["role"],
            "avatar_seed": new_user["avatar_seed"],
        }
        self.is_auth_panel_open = False
        return rx.toast.success("Account created successfully!")

    @rx.event
    def logout(self):
        self.user = None
        return rx.toast.info("Logged out successfully.")