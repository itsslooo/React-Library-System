import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.book_views import books_view
from app.components.add_book_form import add_book_modal
from app.components.book_detail import book_detail_modal
from app.components.borrowing_views import borrowing_view
from app.components.borrow_book_modal import borrow_book_modal
from app.components.dashboard_views import dashboard_view
from app.components.auth_views import auth_panel
from app.states.book_state import BookState
from app.states.dashboard_state import DashboardState
from app.states.auth_state import AuthState


def genre_filter_item(genre: str) -> rx.Component:
    is_selected = BookState.selected_genre == genre
    return rx.el.button(
        rx.el.span(genre),
        rx.cond(is_selected, rx.icon("check", class_name="w-3 h-3 ml-auto"), None),
        on_click=lambda: BookState.set_genre(genre),
        class_name=rx.cond(
            is_selected,
            "w-full text-left px-3 py-2 rounded-lg text-sm font-medium bg-indigo-50 text-indigo-700 flex items-center",
            "w-full text-left px-3 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 flex items-center",
        ),
    )


def books_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="books"),
        rx.el.div(
            header(),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Categories",
                                class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4",
                            ),
                            rx.el.div(
                                rx.foreach(BookState.genres, genre_filter_item),
                                class_name="space-y-1",
                            ),
                            class_name="bg-white rounded-2xl p-6 shadow-sm border border-gray-100",
                        ),
                        class_name="w-64 shrink-0 hidden xl:block",
                    ),
                    rx.el.div(books_view(), class_name="flex-1 min-w-0"),
                    class_name="flex gap-8 p-8 max-w-[1600px] mx-auto",
                ),
                class_name="flex-1 overflow-y-auto bg-slate-50/50",
            ),
            class_name="flex-1 flex flex-col min-w-0 md:pl-64 transition-all duration-300",
        ),
        add_book_modal(),
        book_detail_modal(),
        borrow_book_modal(),
        auth_panel(),
        class_name="flex min-h-screen font-['Poppins'] bg-slate-50 text-gray-900",
    )


def borrowing_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="borrowing"),
        rx.el.div(
            header(),
            rx.el.main(
                rx.el.div(
                    rx.el.div(borrowing_view(), class_name="flex-1 min-w-0"),
                    class_name="flex gap-8 p-8 max-w-[1600px] mx-auto",
                ),
                class_name="flex-1 overflow-y-auto bg-slate-50/50",
            ),
            class_name="flex-1 flex flex-col min-w-0 md:pl-64 transition-all duration-300",
        ),
        auth_panel(),
        class_name="flex min-h-screen font-['Poppins'] bg-slate-50 text-gray-900",
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="dashboard"),
        rx.el.div(
            header(),
            rx.el.main(
                rx.el.div(
                    rx.el.div(dashboard_view(), class_name="flex-1 min-w-0"),
                    class_name="flex gap-8 p-8 max-w-[1600px] mx-auto",
                ),
                class_name="flex-1 overflow-y-auto bg-slate-50/50",
            ),
            class_name="flex-1 flex flex-col min-w-0 md:pl-64 transition-all duration-300",
        ),
        add_book_modal(),
        borrow_book_modal(),
        auth_panel(),
        class_name="flex min-h-screen font-['Poppins'] bg-slate-50 text-gray-900",
        on_mount=DashboardState.load_dashboard_data,
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(books_page, route="/")
app.add_page(dashboard_page, route="/dashboard")
app.add_page(borrowing_page, route="/borrowing")