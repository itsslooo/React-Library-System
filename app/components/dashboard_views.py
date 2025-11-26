import reflex as rx
from app.states.dashboard_state import (
    DashboardState,
    ChartData,
    ActivityItem,
    PopularBook,
)
from app.states.book_state import BookState
from app.states.borrowing_state import BorrowingState


def metric_card(
    title: str, value: str, icon: str, color_class: str, trend: str = "+0%"
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"w-6 h-6 {color_class}"),
                class_name="p-3 rounded-xl bg-white shadow-sm border border-gray-100",
            ),
            rx.el.div(
                rx.el.span(
                    trend,
                    class_name="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.h3(value, class_name="text-2xl font-bold text-gray-900 mb-1"),
            rx.el.p(title, class_name="text-sm text-gray-500 font-medium"),
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300",
    )


def activity_item(item: ActivityItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                rx.cond(item["type"] == "Borrow", "arrow-up-right", "arrow-down-left"),
                class_name="w-4 h-4 text-white",
            ),
            class_name=rx.cond(
                item["type"] == "Borrow",
                "w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center shrink-0",
                "w-8 h-8 rounded-full bg-emerald-500 flex items-center justify-center shrink-0",
            ),
        ),
        rx.el.div(
            rx.el.p(
                rx.el.span(
                    item["borrower_name"], class_name="font-semibold text-gray-900"
                ),
                rx.el.span(
                    " " + item["type"].lower() + "ed ", class_name="text-gray-500"
                ),
                rx.el.span(
                    item["book_title"], class_name="font-medium text-indigo-600"
                ),
                class_name="text-sm",
            ),
            rx.el.p(item["date"], class_name="text-xs text-gray-400 mt-0.5"),
            class_name="ml-3 flex-1",
        ),
        class_name="flex items-start py-3 border-b border-gray-50 last:border-0",
    )


def popular_book_row(book: PopularBook, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.span(f"{index + 1}", class_name="text-sm font-bold text-gray-400 w-6"),
        rx.image(
            src=book["cover_url"],
            class_name="w-8 h-10 object-cover rounded shadow-sm mx-3",
        ),
        rx.el.div(
            rx.el.p(
                book["title"],
                class_name="text-sm font-semibold text-gray-900 line-clamp-1",
            ),
            rx.el.p(book["author"], class_name="text-xs text-gray-500 line-clamp-1"),
            class_name="flex-1 min-w-0",
        ),
        rx.el.div(
            rx.el.span(
                f"{book['count']} borrows",
                class_name="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-1 rounded-md",
            )
        ),
        class_name="flex items-center py-3 border-b border-gray-50 last:border-0",
    )


def simple_bar_chart() -> rx.Component:
    return rx.recharts.bar_chart(
        rx.recharts.cartesian_grid(vertical=False, stroke_dasharray="3 3"),
        rx.recharts.graphing_tooltip(
            cursor=False,
            content_style={
                "backgroundColor": "white",
                "borderRadius": "8px",
                "border": "1px solid #f3f4f6",
                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
            },
        ),
        rx.recharts.bar(
            data_key="value", fill="#6366f1", radius=[4, 4, 0, 0], bar_size=30
        ),
        rx.recharts.x_axis(
            data_key="label",
            axis_line=False,
            tick_line=False,
            custom_attrs={"fontSize": "12px", "color": "#6b7280"},
        ),
        rx.recharts.y_axis(
            axis_line=False,
            tick_line=False,
            custom_attrs={"fontSize": "12px", "color": "#6b7280"},
        ),
        data=DashboardState.borrow_trend,
        width="100%",
        height=200,
    )


def simple_pie_chart() -> rx.Component:
    return rx.el.div(
        rx.recharts.pie_chart(
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "white",
                    "borderRadius": "8px",
                    "border": "1px solid #f3f4f6",
                    "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                }
            ),
            rx.recharts.pie(
                rx.foreach(
                    DashboardState.genre_stats,
                    lambda item: rx.recharts.cell(fill=item["color"]),
                ),
                data=DashboardState.genre_stats,
                data_key="value",
                name_key="label",
                cx="50%",
                cy="50%",
                inner_radius=40,
                outer_radius=60,
                padding_angle=5,
                stroke="#fff",
                stroke_width=2,
            ),
            width="100%",
            height=180,
        ),
        rx.el.div(
            rx.foreach(
                DashboardState.genre_stats,
                lambda stat: rx.el.div(
                    rx.el.div(
                        class_name="w-2 h-2 rounded-full mr-2",
                        style={"background_color": stat["color"]},
                    ),
                    rx.el.span(
                        stat["label"], class_name="text-xs text-gray-600 flex-1"
                    ),
                    rx.el.span(
                        stat["value"], class_name="text-xs font-bold text-gray-900"
                    ),
                    class_name="flex items-center w-1/2 p-1",
                ),
            ),
            class_name="flex flex-wrap mt-4 gap-y-1 justify-center",
        ),
        class_name="flex flex-col items-center justify-center h-full py-2",
    )


def overdue_alert() -> rx.Component:
    return rx.cond(
        DashboardState.overdue_count > 0,
        rx.el.div(
            rx.el.div(
                rx.icon("badge_alert", class_name="w-5 h-5 text-red-500"),
                rx.el.div(
                    rx.el.h4(
                        "Attention Needed", class_name="text-sm font-bold text-red-900"
                    ),
                    rx.el.p(
                        f"{DashboardState.overdue_count} overdue items require action",
                        class_name="text-xs text-red-700",
                    ),
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.button(
                "View All",
                class_name="text-xs font-bold text-red-600 hover:bg-red-100 px-3 py-1.5 rounded-lg transition-colors",
                on_click=lambda: rx.redirect("/borrowing"),
            ),
            class_name="bg-red-50 border border-red-100 rounded-xl p-4 flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.icon("check_check", class_name="w-5 h-5 text-emerald-500 mr-3"),
            rx.el.span(
                "All clear! No overdue items.",
                class_name="text-sm font-medium text-emerald-800",
            ),
            class_name="bg-emerald-50 border border-emerald-100 rounded-xl p-4 flex items-center mb-6",
        ),
    )


def quick_actions() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Quick Actions",
            class_name="text-sm font-bold text-gray-900 uppercase tracking-wide mb-4",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("book-plus", class_name="w-5 h-5 mb-2 text-indigo-600"),
                rx.el.span("Add Book", class_name="text-xs font-medium text-gray-700"),
                on_click=BookState.toggle_add_modal,
                class_name="flex flex-col items-center justify-center p-4 bg-indigo-50 hover:bg-indigo-100 rounded-xl transition-colors border border-indigo-100",
            ),
            rx.el.button(
                rx.icon("arrow-right-left", class_name="w-5 h-5 mb-2 text-orange-600"),
                rx.el.span("Borrow", class_name="text-xs font-medium text-gray-700"),
                on_click=BorrowingState.toggle_borrow_modal,
                class_name="flex flex-col items-center justify-center p-4 bg-orange-50 hover:bg-orange-100 rounded-xl transition-colors border border-orange-100",
            ),
            rx.el.button(
                rx.icon("download", class_name="w-5 h-5 mb-2 text-emerald-600"),
                rx.el.span(
                    "Export Report", class_name="text-xs font-medium text-gray-700"
                ),
                on_click=DashboardState.export_csv,
                class_name="flex flex-col items-center justify-center p-4 bg-emerald-50 hover:bg-emerald-100 rounded-xl transition-colors border border-emerald-100",
            ),
            class_name="grid grid-cols-2 gap-3",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm h-full",
    )


def dashboard_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            metric_card(
                "Total Books",
                DashboardState.total_books.to_string(),
                "library",
                "text-indigo-600",
                "+12%",
            ),
            metric_card(
                "Available",
                DashboardState.available_books.to_string(),
                "book-check",
                "text-emerald-600",
                "+5%",
            ),
            metric_card(
                "Borrowed",
                DashboardState.borrowed_books.to_string(),
                "book-up",
                "text-amber-600",
                "+8%",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Borrowing Trends",
                            class_name="text-lg font-bold text-gray-900 mb-6",
                        ),
                        simple_bar_chart(),
                        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex-1",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Genre Distribution",
                            class_name="text-lg font-bold text-gray-900 mb-4",
                        ),
                        simple_pie_chart(),
                        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm w-full md:w-80 shrink-0",
                    ),
                    class_name="flex flex-col md:flex-row gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Recent Activity",
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        rx.el.button(
                            "View All",
                            class_name="text-sm font-medium text-indigo-600 hover:text-indigo-800",
                        ),
                        class_name="flex items-center justify-between mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(DashboardState.recent_activity, activity_item),
                        class_name="space-y-1",
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm",
                ),
                class_name="flex-1 min-w-0",
            ),
            rx.el.div(
                overdue_alert(),
                quick_actions(),
                rx.el.div(
                    rx.el.h3(
                        "Popular Books",
                        class_name="text-lg font-bold text-gray-900 mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(
                            DashboardState.popular_books,
                            lambda b, i: popular_book_row(b, i),
                        )
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm mt-6",
                ),
                class_name="w-full lg:w-80 shrink-0 flex flex-col gap-2",
            ),
            class_name="flex flex-col lg:flex-row gap-8",
        ),
        class_name="pb-8",
    )