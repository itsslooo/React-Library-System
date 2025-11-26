import reflex as rx
from app.states.book_state import BookState


def form_field(
    label: str,
    name: str,
    type: str = "text",
    placeholder: str = "",
    required: bool = True,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1.5"),
        rx.el.input(
            type=type,
            name=name,
            placeholder=placeholder,
            required=required,
            class_name="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm outline-none",
        ),
        class_name="mb-4",
    )


def add_book_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 animate-fade-in"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        "Add New Book", class_name="text-xl font-bold text-gray-900"
                    ),
                    rx.radix.primitives.dialog.close(
                        rx.icon(
                            "x",
                            class_name="w-5 h-5 text-gray-500 hover:text-gray-700 cursor-pointer",
                        )
                    ),
                    class_name="flex items-center justify-between mb-6",
                ),
                rx.el.form(
                    rx.el.div(
                        form_field(
                            "Book Title", "title", placeholder="Enter book title"
                        ),
                        form_field("Author", "author", placeholder="Author name"),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                    ),
                    rx.el.div(
                        form_field("ISBN", "isbn", placeholder="ISBN-13"),
                        form_field(
                            "Publisher", "publisher", placeholder="Publisher name"
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                    ),
                    rx.el.div(
                        form_field(
                            "Publication Year",
                            "year",
                            type="number",
                            placeholder="YYYY",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Genre",
                                class_name="block text-sm font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.select(
                                rx.foreach(
                                    BookState.genres, lambda g: rx.el.option(g, value=g)
                                ),
                                name="genre",
                                class_name="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm outline-none bg-white",
                            ),
                            class_name="mb-4",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                    ),
                    rx.el.div(
                        form_field(
                            "Quantity",
                            "quantity",
                            type="number",
                            placeholder="Number of copies",
                        ),
                        form_field(
                            "Cover URL",
                            "cover_url",
                            placeholder="https://example.com/image.jpg",
                            required=False,
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=BookState.toggle_add_modal,
                            class_name="px-4 py-2.5 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors",
                        ),
                        rx.el.button(
                            "Add Book",
                            type="submit",
                            class_name="px-4 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-md shadow-indigo-200",
                        ),
                        class_name="flex justify-end gap-3 mt-6 pt-6 border-t border-gray-100",
                    ),
                    on_submit=BookState.add_new_book,
                    reset_on_submit=True,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-2xl shadow-2xl p-6 w-full max-w-2xl z-50 max-h-[90vh] overflow-y-auto focus:outline-none",
            ),
        ),
        open=BookState.is_add_modal_open,
        on_open_change=BookState.toggle_add_modal,
    )