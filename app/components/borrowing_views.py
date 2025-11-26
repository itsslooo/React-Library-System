import reflex as rx
from app.states.borrowing_state import BorrowingState, Loan


def loan_status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.cond(
            status == "Active",
            "bg-blue-100 text-blue-700 ring-1 ring-blue-600/20",
            rx.cond(
                status == "Overdue",
                "bg-red-100 text-red-700 ring-1 ring-red-600/20",
                rx.cond(
                    status == "Returned",
                    "bg-emerald-100 text-emerald-700 ring-1 ring-emerald-600/20",
                    "bg-gray-100 text-gray-700 ring-1 ring-gray-600/20",
                ),
            ),
        )
        + " px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider shadow-sm",
    )


def active_loan_row(loan: Loan) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=loan["book_cover"],
                class_name="w-10 h-14 object-cover rounded shadow-sm",
            ),
            rx.el.div(
                rx.el.h4(
                    loan["book_title"],
                    class_name="font-bold text-gray-900 text-sm line-clamp-1",
                ),
                rx.el.p("ID: " + loan["book_id"], class_name="text-xs text-gray-500"),
                class_name="ml-3",
            ),
            class_name="flex items-center w-1/3",
        ),
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/notionists/svg?seed={loan['borrower_avatar']}",
                    class_name="w-8 h-8 rounded-full bg-indigo-50",
                ),
                rx.el.span(
                    loan["borrower_name"],
                    class_name="ml-2 text-sm font-medium text-gray-700",
                ),
                class_name="flex items-center",
            ),
            class_name="w-1/4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span("Borrowed: ", class_name="text-xs text-gray-400"),
                rx.el.span(loan["borrow_date"], class_name="text-sm text-gray-600"),
                class_name="mb-1",
            ),
            rx.el.div(
                rx.el.span("Due: ", class_name="text-xs text-gray-400"),
                rx.el.span(
                    loan["due_date"],
                    class_name=rx.cond(
                        loan["status"] == "Overdue",
                        "text-sm font-bold text-red-600",
                        "text-sm text-gray-600",
                    ),
                ),
            ),
            class_name="w-1/5",
        ),
        rx.el.div(
            loan_status_badge(loan["status"]), class_name="w-1/6 flex justify-center"
        ),
        rx.el.div(
            rx.el.button(
                "Return",
                on_click=lambda: BorrowingState.return_book(loan["id"]),
                class_name="px-3 py-1.5 text-xs font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-lg transition-colors",
            ),
            class_name="w-auto ml-auto",
        ),
        class_name="flex items-center p-4 bg-white border border-gray-100 rounded-xl hover:shadow-md transition-all mb-3",
    )


def borrowing_view() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Active Loans", class_name="text-lg font-bold text-gray-800 mb-6"),
        rx.cond(
            BorrowingState.active_loans.length() > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Book Details",
                        class_name="text-xs font-bold text-gray-400 uppercase tracking-wider w-1/3 pl-4",
                    ),
                    rx.el.span(
                        "Borrower",
                        class_name="text-xs font-bold text-gray-400 uppercase tracking-wider w-1/4",
                    ),
                    rx.el.span(
                        "Dates",
                        class_name="text-xs font-bold text-gray-400 uppercase tracking-wider w-1/5",
                    ),
                    rx.el.span(
                        "Status",
                        class_name="text-xs font-bold text-gray-400 uppercase tracking-wider w-1/6 text-center",
                    ),
                    rx.el.span(
                        "Action",
                        class_name="text-xs font-bold text-gray-400 uppercase tracking-wider w-auto ml-auto pr-4",
                    ),
                    class_name="flex mb-3 px-2",
                ),
                rx.el.div(
                    rx.foreach(BorrowingState.active_loans, active_loan_row),
                    class_name="space-y-2",
                ),
            ),
            rx.el.div(
                rx.icon("check_check", class_name="w-12 h-12 text-gray-300 mb-3"),
                rx.el.p("No active loans", class_name="text-gray-500 font-medium"),
                class_name="flex flex-col items-center justify-center py-12 bg-white rounded-2xl border border-dashed border-gray-200",
            ),
        ),
    )