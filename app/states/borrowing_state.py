import reflex as rx
from typing import TypedDict, Optional
import datetime
from app.states.book_state import BookState


class Loan(TypedDict):
    id: str
    book_id: str
    book_title: str
    book_cover: str
    borrower_id: str
    borrower_name: str
    borrower_avatar: str
    borrow_date: str
    due_date: str
    return_date: Optional[str]
    status: str
    late_fee: float


class BorrowingState(rx.State):
    loans: list[Loan] = [
        {
            "id": "L001",
            "book_id": "2",
            "book_title": "To Kill a Mockingbird",
            "book_cover": "https://m.media-amazon.com/images/I/81gepf1eMqL._AC_UF1000,1000_QL80_.jpg",
            "borrower_id": "U001",
            "borrower_name": "Alice Johnson",
            "borrower_avatar": "Alice",
            "borrow_date": "2023-10-01",
            "due_date": "2023-10-15",
            "return_date": None,
            "status": "Active",
            "late_fee": 0.0,
        },
        {
            "id": "L002",
            "book_id": "5",
            "book_title": "The Hobbit",
            "book_cover": "https://m.media-amazon.com/images/I/712cDO7d73L._AC_UF1000,1000_QL80_.jpg",
            "borrower_id": "U003",
            "borrower_name": "Charlie Brown",
            "borrower_avatar": "Charlie",
            "borrow_date": "2023-09-15",
            "due_date": "2023-09-29",
            "return_date": None,
            "status": "Overdue",
            "late_fee": 5.0,
        },
    ]
    is_borrow_modal_open: bool = False
    borrower_name: str = ""
    due_date_offset: int = 14

    @rx.var
    def active_loans(self) -> list[Loan]:
        return [loan for loan in self.loans if loan["status"] in ["Active", "Overdue"]]

    @rx.var
    def returned_loans(self) -> list[Loan]:
        return [loan for loan in self.loans if loan["status"] == "Returned"]

    @rx.event
    async def toggle_borrow_modal(self):
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            auth_state.is_auth_panel_open = True
            yield rx.toast.info("Please sign in to borrow books.")
            return
        self.is_borrow_modal_open = not self.is_borrow_modal_open
        self.borrower_name = ""

    @rx.event
    def set_borrower_name(self, name: str):
        self.borrower_name = name

    @rx.event
    async def borrow_book(self):
        book_state = await self.get_state(BookState)
        if not book_state.current_book:
            yield rx.toast.error("No book selected.")
            return
        book = book_state.current_book
        if book["quantity"] <= 0:
            yield rx.toast.error(f"'{book['title']}' is currently out of stock.")
            return
        if not self.borrower_name.strip():
            yield rx.toast.warning("Please enter a borrower name.")
            return
        import random

        today = datetime.date.today()
        due = today + datetime.timedelta(days=self.due_date_offset)
        new_loan: Loan = {
            "id": f"L{random.randint(1000, 9999)}",
            "book_id": book["id"],
            "book_title": book["title"],
            "book_cover": book["cover_url"],
            "borrower_id": "guest",
            "borrower_name": self.borrower_name,
            "borrower_avatar": self.borrower_name,
            "borrow_date": today.isoformat(),
            "due_date": due.isoformat(),
            "return_date": None,
            "status": "Active",
            "late_fee": 0.0,
        }
        self.loans.insert(0, new_loan)
        for b in book_state.books:
            if b["id"] == book["id"]:
                b["quantity"] -= 1
                if b["quantity"] == 0:
                    b["status"] = "Borrowed"
                break
        book_state.books = book_state.books
        if book_state.current_book["id"] == book["id"]:
            book_state.current_book["quantity"] -= 1
            if book_state.current_book["quantity"] == 0:
                book_state.current_book["status"] = "Borrowed"
            book_state.current_book = book_state.current_book
        self.is_borrow_modal_open = False
        book_state.is_detail_modal_open = False
        yield rx.toast.success(f"Book borrowed to {self.borrower_name}")

    @rx.event
    async def return_book(self, loan_id: str):
        loan = next((l for l in self.loans if l["id"] == loan_id), None)
        if not loan:
            return
        if loan["status"] == "Returned":
            return
        loan["status"] = "Returned"
        loan["return_date"] = datetime.date.today().isoformat()
        due_date = datetime.datetime.fromisoformat(loan["due_date"]).date()
        today = datetime.date.today()
        if today > due_date:
            overdue_days = (today - due_date).days
            loan["late_fee"] = overdue_days * 1.0
        book_state = await self.get_state(BookState)
        for b in book_state.books:
            if b["id"] == loan["book_id"]:
                b["quantity"] += 1
                if b["quantity"] > 0:
                    b["status"] = "Available"
                break
        book_state.books = book_state.books
        yield rx.toast.success("Book returned successfully")