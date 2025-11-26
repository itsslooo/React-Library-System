import reflex as rx
from app.states.auth_state import AuthState


def login_form_content() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.label(
                "Email Address",
                class_name="block text-sm font-medium text-gray-700 mb-1.5",
            ),
            rx.el.input(
                name="email",
                type="email",
                placeholder="Enter your email",
                required=True,
                class_name="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm outline-none",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Password", class_name="block text-sm font-medium text-gray-700 mb-1.5"
            ),
            rx.el.input(
                name="password",
                type="password",
                placeholder="Enter your password",
                required=True,
                class_name="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm outline-none",
            ),
            class_name="mb-6",
        ),
        rx.el.button(
            "Sign In",
            type="submit",
            class_name="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg shadow-md shadow-indigo-200 transition-all transform hover:-translate-y-0.5",
        ),
        rx.el.div(
            rx.el.p(
                "Demo Credentials:",
                class_name="font-bold text-xs text-gray-500 uppercase tracking-wide mb-2",
            ),
            rx.el.div(
                rx.el.span("Admin: ", class_name="font-medium text-gray-700"),
                rx.el.span(
                    "admin@libmaster.com / password", class_name="text-gray-500"
                ),
                class_name="text-xs",
            ),
            rx.el.div(
                rx.el.span("User: ", class_name="font-medium text-gray-700"),
                rx.el.span("john@example.com / password", class_name="text-gray-500"),
                class_name="text-xs mt-1",
            ),
            class_name="mt-8 p-4 bg-gray-50 rounded-lg border border-gray-100",
        ),
        on_submit=AuthState.login,
    )


def register_form_content() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.label(
                "Full Name", class_name="block text-sm font-medium text-gray-700 mb-1.5"
            ),
            rx.el.input(
                name="name",
                type="text",
                placeholder="John Doe",
                required=True,
                class_name="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm outline-none",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Email Address",
                class_name="block text-sm font-medium text-gray-700 mb-1.5",
            ),
            rx.el.input(
                name="email",
                type="email",
                placeholder="john@example.com",
                required=True,
                class_name="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm outline-none",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Password", class_name="block text-sm font-medium text-gray-700 mb-1.5"
            ),
            rx.el.input(
                name="password",
                type="password",
                placeholder="Create a password",
                required=True,
                class_name="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm outline-none",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Confirm Password",
                class_name="block text-sm font-medium text-gray-700 mb-1.5",
            ),
            rx.el.input(
                name="confirm_password",
                type="password",
                placeholder="Confirm your password",
                required=True,
                class_name="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm outline-none",
            ),
            class_name="mb-6",
        ),
        rx.el.button(
            "Create Account",
            type="submit",
            class_name="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg shadow-md shadow-indigo-200 transition-all transform hover:-translate-y-0.5",
        ),
        on_submit=AuthState.register,
    )


def auth_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-black/30 backdrop-blur-sm z-40 transition-opacity",
                on_click=AuthState.toggle_auth_panel,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Welcome to LibMaster",
                            class_name="text-xl font-bold text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="w-6 h-6 text-gray-500"),
                            on_click=AuthState.toggle_auth_panel,
                            class_name="p-2 hover:bg-gray-100 rounded-full transition-colors",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Sign In",
                            on_click=lambda: AuthState.set_auth_mode("login"),
                            class_name=rx.cond(
                                AuthState.auth_mode == "login",
                                "w-1/2 py-2 text-sm font-semibold text-indigo-600 border-b-2 border-indigo-600",
                                "w-1/2 py-2 text-sm font-medium text-gray-500 border-b border-gray-200 hover:text-gray-700",
                            ),
                        ),
                        rx.el.button(
                            "Register",
                            on_click=lambda: AuthState.set_auth_mode("register"),
                            class_name=rx.cond(
                                AuthState.auth_mode == "register",
                                "w-1/2 py-2 text-sm font-semibold text-indigo-600 border-b-2 border-indigo-600",
                                "w-1/2 py-2 text-sm font-medium text-gray-500 border-b border-gray-200 hover:text-gray-700",
                            ),
                        ),
                        class_name="flex mb-6",
                    ),
                    rx.cond(
                        AuthState.auth_mode == "login",
                        login_form_content(),
                        register_form_content(),
                    ),
                    class_name="h-full flex flex-col p-6 overflow-y-auto",
                ),
                class_name="fixed right-0 top-0 h-full w-full sm:w-[400px] bg-white shadow-2xl z-50 transform transition-transform duration-300 ease-in-out "
                + rx.cond(
                    AuthState.is_auth_panel_open, "translate-x-0", "translate-x-full"
                ),
            ),
            class_name=rx.cond(
                AuthState.is_auth_panel_open,
                "fixed inset-0 z-40",
                "fixed inset-0 z-40 pointer-events-none opacity-0",
            ),
        )
    )