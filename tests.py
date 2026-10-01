import pytest
from main import BooksCollector


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # ---------- add_new_book ----------

    # пример теста: добавление двух книг
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize('name', [
        'Гарри Поттер',
        'А' * 40,
    ])
    def test_add_new_book_adds_valid_name(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.get_books_genre()
        assert collector.get_books_genre()[name] == ''

    @pytest.mark.parametrize('name', [
        '',
        'А' * 41,
    ])
    def test_add_new_book_does_not_add_invalid_name(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name not in collector.get_books_genre()

    def test_add_new_book_does_not_add_duplicate(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Гарри Поттер')
        assert len(collector.get_books_genre()) == 1

    # ---------- set_book_genre / get_book_genre ----------

    @pytest.mark.parametrize('genre', [
        'Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии',
    ])
    def test_set_book_genre_sets_valid_genre(self, genre):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', genre)
        assert collector.get_book_genre('Книга') == genre

    def test_set_book_genre_does_not_set_invalid_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Несуществующий жанр')
        assert collector.get_book_genre('Книга') == ''

    def test_set_book_genre_does_not_set_genre_for_unknown_book(self):
        collector = BooksCollector()
        collector.set_book_genre('Неизвестная книга', 'Ужасы')
        assert collector.get_book_genre('Неизвестная книга') is None

    # ---------- get_books_with_specific_genre ----------

    def test_get_books_with_specific_genre_returns_only_matching(self):
        collector = BooksCollector()
        collector.add_new_book('Ужастик')
        collector.set_book_genre('Ужастик', 'Ужасы')
        collector.add_new_book('Смешинка')
        collector.set_book_genre('Смешинка', 'Комедии')
        assert collector.get_books_with_specific_genre('Ужасы') == ['Ужастик']

    # ---------- get_books_genre ----------

    def test_get_books_genre_returns_current_dict(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Фантастика')
        assert collector.get_books_genre() == {'Книга': 'Фантастика'}

    # ---------- get_books_for_children ----------

    def test_get_books_for_children_excludes_age_rating(self):
        collector = BooksCollector()
        collector.add_new_book('Ужастик')
        collector.set_book_genre('Ужастик', 'Ужасы')
        collector.add_new_book('Мультик')
        collector.set_book_genre('Мультик', 'Мультфильмы')
        collector.add_new_book('Без жанра')
        assert collector.get_books_for_children() == ['Мультик']

    # ---------- add_book_in_favorites ----------

    def test_add_book_in_favorites_adds_book(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        assert collector.get_list_of_favorites_books() == ['Книга']

    def test_add_book_in_favorites_does_not_add_unknown_book(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Неизвестная книга')
        assert collector.get_list_of_favorites_books() == []

    def test_add_book_in_favorites_does_not_add_duplicate(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.add_book_in_favorites('Книга')
        assert collector.get_list_of_favorites_books() == ['Книга']

    # ---------- delete_book_from_favorites ----------

    def test_delete_book_from_favorites_removes_book(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.delete_book_from_favorites('Книга')
        assert collector.get_list_of_favorites_books() == []
