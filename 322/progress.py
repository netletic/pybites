from datetime import datetime


def ontrack_reading(books_goal: int, books_read: int, day_of_year: int = None) -> bool:
    if not day_of_year:
        day_of_year = datetime.now().timetuple().tm_yday
    expected_books_read = books_goal / 365 * day_of_year
    return books_read >= expected_books_read


if __name__ == "__main__":
    print(ontrack_reading(60, 2, 3))
