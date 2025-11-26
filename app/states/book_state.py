import reflex as rx
from typing import TypedDict, Optional


class Book(TypedDict):
    id: str
    title: str
    author: str
    isbn: str
    publisher: str
    year: str
    genre: str
    quantity: int
    cover_url: str
    status: str
    description: str


class BookState(rx.State):
    books: list[Book] = [
        {
            "id": "1",
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "isbn": "978-0743273565",
            "publisher": "Scribner",
            "year": "1925",
            "genre": "Classic",
            "quantity": 5,
            "cover_url": "https://m.media-amazon.com/images/I/71FTb9X6wsL._AC_UF1000,1000_QL80_.jpg",
            "status": "Available",
            "description": "The Great Gatsby is a 1925 novel by American writer F. Scott Fitzgerald. Set in the Jazz Age on Long Island, near New York City, the novel depicts first-person narrator Nick Carraway's interactions with mysterious millionaire Jay Gatsby and Gatsby's obsession to reunite with his former lover, Daisy Buchanan.",
        },
        {
            "id": "2",
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "isbn": "978-0446310789",
            "publisher": "J.B. Lippincott & Co.",
            "year": "1960",
            "genre": "Fiction",
            "quantity": 3,
            "cover_url": "https://m.media-amazon.com/images/I/81gepf1eMqL._AC_UF1000,1000_QL80_.jpg",
            "status": "Borrowed",
            "description": "To Kill a Mockingbird is a novel by the American author Harper Lee. It was published in 1960 and was instantly successful. In the United States, it is widely read in high schools and middle schools. To Kill a Mockingbird has become a classic of modern American literature, winning the Pulitzer Prize.",
        },
        {
            "id": "3",
            "title": "1984",
            "author": "George Orwell",
            "isbn": "978-0451524935",
            "publisher": "Secker & Warburg",
            "year": "1949",
            "genre": "Dystopian",
            "quantity": 8,
            "cover_url": "https://m.media-amazon.com/images/I/71rpa1-kyvL._AC_UF1000,1000_QL80_.jpg",
            "status": "Available",
            "description": "Nineteen Eighty-Four is a dystopian social science fiction novel and cautionary tale written by the English novelist George Orwell. It was published on 8 June 1949 by Secker & Warburg as Orwell's ninth and final book completed in his lifetime.",
        },
        {
            "id": "4",
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "isbn": "978-1503290563",
            "publisher": "T. Egerton",
            "year": "1813",
            "genre": "Romance",
            "quantity": 2,
            "cover_url": "https://m.media-amazon.com/images/I/71Q1tPupLF-L._AC_UF1000,1000_QL80_.jpg",
            "status": "Available",
            "description": "Pride and Prejudice is an 1813 novel of manners by Jane Austen. The novel follows the character development of Elizabeth Bennet, the dynamic protagonist of the book who learns about the repercussions of hasty judgments and comes to appreciate the difference between superficial goodness and actual goodness.",
        },
        {
            "id": "5",
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "isbn": "978-0547928227",
            "publisher": "George Allen & Unwin",
            "year": "1937",
            "genre": "Fantasy",
            "quantity": 0,
            "cover_url": "https://m.media-amazon.com/images/I/712cDO7d73L._AC_UF1000,1000_QL80_.jpg",
            "status": "Borrowed",
            "description": "The Hobbit, or There and Back Again is a children's fantasy novel by English author J. R. R. Tolkien. It was published on 21 September 1937 to wide critical acclaim, being nominated for the Carnegie Medal and awarded a prize from the New York Herald Tribune for best juvenile fiction.",
        },
        {
            "id": "6",
            "title": "Dune",
            "author": "Frank Herbert",
            "isbn": "978-0441172719",
            "publisher": "Chilton Books",
            "year": "1965",
            "genre": "Sci-Fi",
            "quantity": 6,
            "cover_url": "https://m.media-amazon.com/images/I/81ym3QUd3KL._AC_UF1000,1000_QL80_.jpg",
            "status": "Available",
            "description": "Dune is a 1965 epic science fiction novel by American author Frank Herbert, originally published as two separate serials in Analog magazine. It tied with Roger Zelazny's This Immortal for the Hugo Award in 1966, and it won the inaugural Nebula Award for Best Novel.",
        },
    ]
    search_query: str = ""
    view_mode: str = "grid"
    selected_genre: str = "All"
    is_add_modal_open: bool = False
    is_detail_modal_open: bool = False
    current_book: Optional[Book] = None
    genres: list[str] = [
        "All",
        "Fiction",
        "Non-Fiction",
        "Sci-Fi",
        "Mystery",
        "Classic",
        "Romance",
        "Fantasy",
        "Dystopian",
    ]

    @rx.var
    def filtered_books(self) -> list[Book]:
        filtered = self.books
        if self.selected_genre != "All":
            filtered = [b for b in filtered if b["genre"] == self.selected_genre]
        if self.search_query:
            query = self.search_query.lower()
            filtered = [
                b
                for b in filtered
                if query in b["title"].lower()
                or query in b["author"].lower()
                or query in b["isbn"].lower()
            ]
        return filtered

    @rx.var
    def total_books_count(self) -> int:
        return len(self.books)

    @rx.var
    def available_books_count(self) -> int:
        return len([b for b in self.books if b["status"] == "Available"])

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_view_mode(self, mode: str):
        self.view_mode = mode

    @rx.event
    def set_genre(self, genre: str):
        self.selected_genre = genre

    @rx.event
    async def toggle_add_modal(self):
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            auth_state.is_auth_panel_open = True
            yield rx.toast.info("Please sign in to add books.")
            return
        self.is_add_modal_open = not self.is_add_modal_open

    @rx.event
    def open_detail_modal(self, book: Book):
        self.current_book = book
        self.is_detail_modal_open = True

    @rx.event
    def close_detail_modal(self):
        self.is_detail_modal_open = False
        self.current_book = None

    @rx.event
    def add_new_book(self, form_data: dict):
        import random

        new_book: Book = {
            "id": str(random.randint(1000, 9999)),
            "title": form_data["title"],
            "author": form_data["author"],
            "isbn": form_data["isbn"],
            "publisher": form_data["publisher"],
            "year": form_data["year"],
            "genre": form_data["genre"],
            "quantity": int(form_data["quantity"]),
            "cover_url": form_data.get("cover_url", "/placeholder.svg")
            or "/placeholder.svg",
            "status": "Available",
            "description": "No description provided.",
        }
        self.books.insert(0, new_book)
        self.is_add_modal_open = False
        yield rx.toast.success(f"Book '{new_book['title']}' added successfully!")