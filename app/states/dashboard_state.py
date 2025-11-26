import reflex as rx
from typing import TypedDict
import datetime
import csv
import io
from app.states.book_state import BookState
from app.states.borrowing_state import BorrowingState


class PopularBook(TypedDict):
    title: str
    author: str
    count: int
    cover_url: str


class ActivityItem(TypedDict):
    id: str
    type: str
    book_title: str
    borrower_name: str
    date: str
    status: str


class ChartData(TypedDict):
    label: str
    value: float
    color: str


class DashboardState(rx.State):
    total_books: int = 0
    available_books: int = 0
    borrowed_books: int = 0
    overdue_count: int = 0
    recent_activity: list[ActivityItem] = []
    popular_books: list[PopularBook] = []
    genre_stats: list[ChartData] = []
    borrow_trend: list[ChartData] = []
    theme_mode: str = "light"

    @rx.event
    async def load_dashboard_data(self):
        book_state = await self.get_state(BookState)
        borrowing_state = await self.get_state(BorrowingState)
        self.total_books = len(book_state.books)
        self.available_books = len(
            [b for b in book_state.books if b["status"] == "Available"]
        )
        self.borrowed_books = len(
            [b for b in book_state.books if b["status"] == "Borrowed"]
        )
        loans = borrowing_state.loans
        self.overdue_count = len([l for l in loans if l["status"] == "Overdue"])
        activity = []
        sorted_loans = sorted(loans, key=lambda x: x["borrow_date"], reverse=True)
        for loan in sorted_loans[:10]:
            activity.append(
                {
                    "id": f"borrow_{loan['id']}",
                    "type": "Borrow",
                    "book_title": loan["book_title"],
                    "borrower_name": loan["borrower_name"],
                    "date": loan["borrow_date"],
                    "status": "Active" if loan["return_date"] is None else "Returned",
                }
            )
            if loan["return_date"]:
                activity.append(
                    {
                        "id": f"return_{loan['id']}",
                        "type": "Return",
                        "book_title": loan["book_title"],
                        "borrower_name": loan["borrower_name"],
                        "date": loan["return_date"],
                        "status": "Completed",
                    }
                )
        self.recent_activity = sorted(activity, key=lambda x: x["date"], reverse=True)[
            :6
        ]
        book_borrow_counts = {}
        for loan in loans:
            bid = loan["book_id"]
            book_borrow_counts[bid] = book_borrow_counts.get(bid, 0) + 1
        pop_books = []
        for bid, count in book_borrow_counts.items():
            book = next((b for b in book_state.books if b["id"] == bid), None)
            if book:
                pop_books.append(
                    {
                        "title": book["title"],
                        "author": book["author"],
                        "count": count,
                        "cover_url": book["cover_url"],
                    }
                )
        self.popular_books = sorted(pop_books, key=lambda x: x["count"], reverse=True)[
            :5
        ]
        genres = {}
        for book in book_state.books:
            g = book["genre"]
            genres[g] = genres.get(g, 0) + 1
        colors = [
            "#6366f1",
            "#8b5cf6",
            "#ec4899",
            "#f43f5e",
            "#f97316",
            "#eab308",
            "#22c55e",
            "#06b6d4",
        ]
        self.genre_stats = [
            {"label": k, "value": v, "color": colors[i % len(colors)]}
            for i, (k, v) in enumerate(genres.items())
        ]
        self.borrow_trend = [
            {"label": "May", "value": 12, "color": "#6366f1"},
            {"label": "Jun", "value": 19, "color": "#6366f1"},
            {"label": "Jul", "value": 15, "color": "#6366f1"},
            {"label": "Aug", "value": 25, "color": "#6366f1"},
            {"label": "Sep", "value": 32, "color": "#6366f1"},
            {"label": "Oct", "value": 28, "color": "#6366f1"},
        ]

    @rx.event
    def toggle_theme(self):
        self.theme_mode = "dark" if self.theme_mode == "light" else "light"

    @rx.event
    async def export_csv(self):
        borrowing_state = await self.get_state(BorrowingState)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            ["Loan ID", "Book", "Borrower", "Borrow Date", "Due Date", "Status"]
        )
        for loan in borrowing_state.loans:
            writer.writerow(
                [
                    loan["id"],
                    loan["book_title"],
                    loan["borrower_name"],
                    loan["borrow_date"],
                    loan["due_date"],
                    loan["status"],
                ]
            )
        csv_string = output.getvalue()
        return rx.download(data=csv_string, filename="library_report.csv")