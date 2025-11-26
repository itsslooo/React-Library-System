import reflex as rx
from app.states.book_state import BookState
from app.states.borrowing_state import BorrowingState


def detail_row(label: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(label, class_name="text-sm font-medium text-gray-500 w-32 shrink-0"),
        rx.el.span(value, class_name="text-sm font-medium text-gray-900"),
        class_name="flex items-start py-2 border-b border-gray-50 last:border-0",
    )


def book_detail_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 animate-fade-in"
            ),
            rx.radix.primitives.dialog.content(
                rx.cond(
                    BookState.current_book,
                    rx.el.div(
                        rx.el.div(
                            rx.radix.primitives.dialog.title(
                                "Book Details",
                                class_name="text-lg font-bold text-gray-900",
                            ),
                            rx.radix.primitives.dialog.close(
                                rx.icon(
                                    "x",
                                    class_name="w-5 h-5 text-gray-500 hover:text-gray-700 cursor-pointer",
                                )
                            ),
                            class_name="flex items-center justify-between mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.image(
                                    src=BookState.current_book["cover_url"],
                                    class_name="w-full h-64 object-cover rounded-xl shadow-md",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        BookState.current_book["status"],
                                        class_name=rx.cond(
                                            BookState.current_book["status"]
                                            == "Available",
                                            "bg-emerald-100 text-emerald-700",
                                            "bg-amber-100 text-amber-700",
                                        )
                                        + " px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide",
                                    ),
                                    class_name="flex justify-center mt-4",
                                ),
                                class_name="w-full md:w-1/3",
                            ),
                            rx.el.div(
                                rx.el.h2(
                                    BookState.current_book["title"],
                                    class_name="text-2xl font-bold text-gray-900 mb-1",
                                ),
                                rx.el.p(
                                    BookState.current_book["author"],
                                    class_name="text-lg text-indigo-600 font-medium mb-6",
                                ),
                                rx.el.div(
                                    detail_row("ISBN", BookState.current_book["isbn"]),
                                    detail_row(
                                        "Publisher", BookState.current_book["publisher"]
                                    ),
                                    detail_row("Year", BookState.current_book["year"]),
                                    detail_row(
                                        "Genre", BookState.current_book["genre"]
                                    ),
                                    detail_row(
                                        "Quantity",
                                        BookState.current_book["quantity"].to_string(),
                                    ),
                                    class_name="bg-gray-50 rounded-xl p-4 mb-6",
                                ),
                                rx.el.div(
                                    rx.el.h3(
                                        "Description",
                                        class_name="text-sm font-bold text-gray-900 mb-2",
                                    ),
                                    rx.el.p(
                                        BookState.current_book["description"],
                                        class_name="text-sm text-gray-600 leading-relaxed",
                                    ),
                                ),
                                class_name="w-full md:w-2/3",
                            ),
                            class_name="flex flex-col md:flex-row gap-8",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Close",
                                on_click=BookState.close_detail_modal,
                                class_name="px-4 py-2.5 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors",
                            ),
                            rx.cond(
                                BookState.current_book["status"] == "Available",
                                rx.el.button(
                                    "Borrow Book",
                                    on_click=BorrowingState.toggle_borrow_modal,
                                    class_name="px-4 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-md shadow-indigo-200",
                                ),
                                rx.el.button(
                                    "Currently Unavailable",
                                    disabled=True,
                                    class_name="px-4 py-2.5 text-sm font-medium text-gray-400 bg-gray-100 rounded-lg cursor-not-allowed",
                                ),
                            ),
                            class_name="flex justify-end gap-3 mt-8 pt-6 border-t border-gray-100",
                        ),
                    ),
                    rx.el.div("Loading...", class_name="p-8 text-center text-gray-500"),
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-2xl shadow-2xl p-6 w-full max-w-3xl z-50 max-h-[90vh] overflow-y-auto focus:outline-none",
            ),
        ),
        open=BookState.is_detail_modal_open,
        on_open_change=BookState.close_detail_modal,
    )