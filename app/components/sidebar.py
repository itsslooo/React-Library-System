import reflex as rx
from app.states.auth_state import AuthState


def sidebar_item(
    icon_name: str, text: str, href: str, is_active: bool = False
) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(
                icon_name,
                class_name=f"w-5 h-5 {rx.cond(is_active, 'text-white', 'text-indigo-200')}",
            ),
            rx.el.span(text, class_name="font-medium"),
            class_name=f"flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 {rx.cond(is_active, 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/30', 'text-indigo-100 hover:bg-indigo-800 hover:text-white')}",
        ),
        href=href,
        class_name="block mb-2",
    )


def sidebar(current_page: str) -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.icon("library", class_name="w-8 h-8 text-white"),
            rx.el.h1(
                "LibMaster", class_name="text-xl font-bold text-white tracking-tight"
            ),
            class_name="flex items-center gap-3 px-6 py-8 mb-6",
        ),
        rx.el.nav(
            rx.el.div(
                rx.el.p(
                    "MENU",
                    class_name="px-6 text-xs font-semibold text-indigo-300 mb-4 tracking-wider",
                ),
                rx.cond(
                    AuthState.is_admin,
                    sidebar_item(
                        "layout-dashboard",
                        "Dashboard",
                        "/dashboard",
                        current_page == "dashboard",
                    ),
                ),
                rx.cond(
                    AuthState.is_authenticated,
                    sidebar_item("book", "Books", "/", current_page == "books"),
                ),
                sidebar_item(
                    "arrow-left-right",
                    "Borrowing",
                    "/borrowing",
                    current_page == "borrowing",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.button(
                        rx.el.div(
                            rx.icon("log-out", class_name="w-5 h-5 text-indigo-200"),
                            rx.el.span(
                                "Logout", class_name="font-medium text-indigo-100"
                            ),
                            class_name="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-indigo-800 transition-all duration-200",
                        ),
                        on_click=AuthState.logout,
                        class_name="w-full text-left mb-2",
                    ),
                    rx.el.button(
                        rx.el.div(
                            rx.icon("log-in", class_name="w-5 h-5 text-indigo-200"),
                            rx.el.span(
                                "Sign In", class_name="font-medium text-indigo-100"
                            ),
                            class_name="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-indigo-800 transition-all duration-200",
                        ),
                        on_click=AuthState.toggle_auth_panel,
                        class_name="w-full text-left mb-2",
                    ),
                )
            ),
        ),
        rx.cond(
            AuthState.is_authenticated,
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src=f"https://api.dicebear.com/9.x/notionists/svg?seed={AuthState.user['avatar_seed']}",
                        class_name="w-10 h-10 rounded-full bg-indigo-500 border-2 border-indigo-400 shrink-0",
                    ),
                    rx.el.div(
                        rx.el.p(
                            AuthState.user["name"],
                            class_name="text-sm font-semibold text-white line-clamp-1",
                        ),
                        rx.el.p(
                            AuthState.user["role"],
                            class_name="text-[10px] text-indigo-300 font-bold tracking-wider uppercase mt-0.5",
                        ),
                        class_name="flex flex-col min-w-0 overflow-hidden",
                    ),
                    class_name="flex items-center gap-3",
                ),
                class_name="mt-auto p-6 border-t border-indigo-800",
            ),
            rx.el.div(
                rx.el.button(
                    "Sign In / Register",
                    on_click=AuthState.toggle_auth_panel,
                    class_name="w-full py-2.5 px-4 bg-white/10 hover:bg-white/20 text-white text-sm font-medium rounded-lg transition-all border border-white/10",
                ),
                class_name="mt-auto p-6 border-t border-indigo-800",
            ),
        ),
        class_name="hidden md:flex w-64 bg-indigo-900 h-screen flex-col fixed left-0 top-0 z-30 shadow-xl",
    )