import reflex as rx
from app.states.book_state import BookState
from app.states.auth_state import AuthState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Search books, authors, ISBN...",
                    on_change=BookState.set_search_query,
                    class_name="pl-10 pr-4 py-2.5 bg-gray-100 border-none rounded-xl w-64 md:w-96 text-sm focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all duration-200 placeholder-gray-400 outline-none",
                    default_value=BookState.search_query,
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("bell", class_name="w-5 h-5 text-gray-600"),
                    class_name="p-2.5 rounded-xl hover:bg-gray-100 transition-colors relative",
                ),
                rx.el.button(
                    rx.icon("moon", class_name="w-5 h-5 text-gray-600"),
                    on_click=rx.toggle_color_mode,
                    class_name="p-2.5 rounded-xl hover:bg-gray-100 transition-colors relative",
                ),
                rx.el.div(class_name="w-px h-8 bg-gray-200 mx-2"),
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        rx.cond(
                            AuthState.is_admin,
                            rx.el.button(
                                rx.icon("plus", class_name="w-5 h-5 mr-2"),
                                "Add Book",
                                on_click=BookState.toggle_add_modal,
                                class_name="flex items-center px-4 py-2.5 bg-indigo-600 text-white text-sm font-medium rounded-xl hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition-all hover:-translate-y-0.5",
                            ),
                            rx.fragment(),
                        ),
                        rx.el.div(
                            rx.image(
                                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={AuthState.user['avatar_seed']}",
                                class_name="w-9 h-9 rounded-full bg-indigo-500 border border-indigo-400",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    AuthState.user["name"],
                                    class_name="text-sm font-semibold text-gray-900 line-clamp-1",
                                ),
                                rx.el.button(
                                    "Logout",
                                    on_click=AuthState.logout,
                                    class_name="text-xs text-gray-500 hover:text-indigo-600 font-medium text-left",
                                ),
                                class_name="flex flex-col",
                            ),
                            class_name="flex items-center gap-3",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    rx.el.button(
                        "Sign In",
                        on_click=AuthState.toggle_auth_panel,
                        class_name="px-4 py-2.5 bg-gray-900 text-white text-sm font-medium rounded-xl hover:bg-gray-800 transition-all shadow-lg shadow-gray-200",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between",
        ),
        class_name="sticky top-0 z-20 bg-white/80 backdrop-blur-md border-b border-gray-200 px-8 py-4",
    )