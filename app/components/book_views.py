import reflex as rx
from app.states.book_state import BookState, Book


def status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.cond(
            status == "Available",
            "bg-emerald-100 text-emerald-700 ring-1 ring-emerald-600/20",
            rx.cond(
                status == "Borrowed",
                "bg-amber-100 text-amber-700 ring-1 ring-amber-600/20",
                "bg-gray-100 text-gray-700 ring-1 ring-gray-600/20",
            ),
        )
        + " px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider shadow-sm",
    )


def book_card_grid(book: Book) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=book["cover_url"],
                class_name="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110",
            ),
            rx.el.div(
                status_badge(book["status"]),
                class_name="absolute top-3 right-3 shadow-sm",
            ),
            class_name="h-48 overflow-hidden relative bg-gray-200",
        ),
        rx.el.div(
            rx.el.h3(
                book["title"], class_name="font-bold text-gray-900 mb-1 line-clamp-1"
            ),
            rx.el.p(
                book["author"], class_name="text-sm text-indigo-600 font-medium mb-2"
            ),
            rx.el.div(
                rx.el.span(
                    book["genre"],
                    class_name="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded",
                ),
                rx.el.span(book["year"], class_name="text-xs text-gray-400"),
                class_name="flex items-center justify-between mt-auto",
            ),
            class_name="p-4 flex flex-col h-32",
        ),
        on_click=lambda: BookState.open_detail_modal(book),
        class_name="bg-white rounded-2xl overflow-hidden border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300 cursor-pointer group hover:-translate-y-1",
    )


def book_row_list(book: Book) -> rx.Component:
    return rx.el.div(
        rx.image(
            src=book["cover_url"],
            class_name="w-12 h-16 object-cover rounded-md shadow-sm",
        ),
        rx.el.div(
            rx.el.h3(book["title"], class_name="font-bold text-gray-900"),
            rx.el.p(book["author"], class_name="text-sm text-indigo-600"),
            class_name="ml-4 flex-1",
        ),
        rx.el.div(
            book["genre"], class_name="text-sm text-gray-600 w-32 hidden md:block"
        ),
        rx.el.div(
            book["isbn"],
            class_name="text-sm text-gray-500 w-40 hidden lg:block font-mono",
        ),
        rx.el.div(status_badge(book["status"]), class_name="w-24 flex justify-end"),
        on_click=lambda: BookState.open_detail_modal(book),
        class_name="flex items-center p-4 bg-white border border-gray-100 rounded-xl hover:shadow-md hover:border-indigo-100 transition-all cursor-pointer mb-2 group",
    )


def books_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2("All Books", class_name="text-lg font-bold text-gray-800"),
                rx.el.span(
                    f"{BookState.filtered_books.length()} items",
                    class_name="text-sm text-gray-500 font-medium ml-2",
                ),
                class_name="flex items-baseline",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("layout-grid", class_name="w-4 h-4"),
                    class_name=rx.cond(
                        BookState.view_mode == "grid",
                        "p-2 bg-indigo-100 text-indigo-600 rounded-lg",
                        "p-2 text-gray-400 hover:text-gray-600",
                    ),
                    on_click=lambda: BookState.set_view_mode("grid"),
                ),
                rx.el.button(
                    rx.icon("list", class_name="w-4 h-4"),
                    class_name=rx.cond(
                        BookState.view_mode == "list",
                        "p-2 bg-indigo-100 text-indigo-600 rounded-lg",
                        "p-2 text-gray-400 hover:text-gray-600",
                    ),
                    on_click=lambda: BookState.set_view_mode("list"),
                ),
                class_name="flex items-center gap-1 bg-white border border-gray-200 rounded-xl p-1 shadow-sm",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.cond(
            BookState.filtered_books.length() > 0,
            rx.cond(
                BookState.view_mode == "grid",
                rx.el.div(
                    rx.foreach(BookState.filtered_books, book_card_grid),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
                ),
                rx.el.div(
                    rx.foreach(BookState.filtered_books, book_row_list),
                    class_name="flex flex-col gap-2",
                ),
            ),
            rx.el.div(
                rx.icon("book-x", class_name="w-16 h-16 text-gray-200 mb-4"),
                rx.el.h3(
                    "No books found", class_name="text-lg font-semibold text-gray-900"
                ),
                rx.el.p(
                    "Try adjusting your search or filters.",
                    class_name="text-gray-500 text-sm",
                ),
                class_name="flex flex-col items-center justify-center py-20 text-center bg-white rounded-2xl border border-dashed border-gray-200",
            ),
        ),
    )