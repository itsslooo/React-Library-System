import reflex as rx
from app.states.borrowing_state import BorrowingState
from app.states.book_state import BookState


def borrow_book_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-[60] animate-fade-in"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        "Borrow Book", class_name="text-xl font-bold text-gray-900"
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
                        rx.el.span(
                            "Selected Book:",
                            class_name="text-sm font-medium text-gray-500 mb-1 block",
                        ),
                        rx.el.h4(
                            BookState.current_book["title"],
                            class_name="text-lg font-bold text-indigo-700",
                        ),
                        rx.el.p(
                            "by " + BookState.current_book["author"],
                            class_name="text-sm text-gray-600 mb-4",
                        ),
                        class_name="bg-indigo-50 p-4 rounded-xl mb-6 border border-indigo-100",
                    ),
                    rx.el.div(
                        rx.el.label(
                            rx.el.span("Borrower Name"),
                            class_name="block text-sm font-medium text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            placeholder="Enter borrower's name",
                            on_change=BorrowingState.set_borrower_name,
                            class_name="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm outline-none",
                            default_value=BorrowingState.borrower_name,
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=BorrowingState.toggle_borrow_modal,
                            class_name="px-4 py-2.5 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors",
                        ),
                        rx.el.button(
                            "Confirm Borrow",
                            on_click=BorrowingState.borrow_book,
                            class_name="px-4 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-md shadow-indigo-200",
                        ),
                        class_name="flex justify-end gap-3 pt-2",
                    ),
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-2xl shadow-2xl p-6 w-full max-w-md z-[60] focus:outline-none",
            ),
        ),
        open=BorrowingState.is_borrow_modal_open,
        on_open_change=BorrowingState.toggle_borrow_modal,
    )