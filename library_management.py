import datetime


class Books:

    def __init__(self, name, author, publisher, publishing_date, category):
        self.name = name
        self.author = author
        self.publisher = publisher
        self.publishing_date = publishing_date
        self.category = category

    def __repr__(self):
        return f'book {self.name} author {self.author}'


class Author:
    def __init__(self, name, books_list, dob, dod=None):
        self.name = name
        self.book_list = books_list
        self.dob = dob
        self.dod = dod

    def __repr__(self):
        return f' {self.name}'


class Publisher:
    def __init__(self, name, books_list, location):
        self.name = name
        self.books_list = books_list
        self.location = location


class Student:

    def __init__(self, name, email):
        self.name = name
        self.email = email


publisher1 = Publisher('one', ['a'], 'Yerevan')
publisher2 = Publisher('two', ['b'], 'Yerevan')
publisher3 = Publisher('three', ['c'], 'Yerevan')
author1 = Author('ab', ['a'], 1975)
author2 = Author('cd', ['b'], 1946, 2011)
author3 = Author('ef', ['c'], 1986)
book1 = Books('a', author1, publisher1, 2005, 'fiction')
book2 = Books('b', author2, publisher2, 2003, 'non fiction')
book3 = Books('c', author3, publisher3, 2004, 'fiction')


class AvailableBooks:
    books_list = [book1, book2, book3]
    book_items = {k: 1 for k in books_list}  # amen grqic qani hat ka

    @classmethod
    def add_book(cls, book):
        cls.books_list.append(book)

    @classmethod
    def add_item(cls, book, count=1):
        cls.book_items[book] += count


class BookRanking(AvailableBooks):
    rank = {k: 0 for k in AvailableBooks.books_list}
    current_rank = {k: 0 for k in AvailableBooks.books_list}

    @classmethod
    def book_rank(cls, book):
        cls.current_rank[book] += 1

    @classmethod
    def update_ranking(cls):
        cls.rank = cls.current_rank


class LibraryCard:
    borrowed_books = {}

    def __init__(self, st_id):
        self.st_id = st_id

    def borrow_book(self, book, librarian):
        return librarian.lend_the_book(self, book)

    def return_the_book(self, book, librarian):
        return librarian.get_the_book(self, book)

    def extend_borrowed(self, book, librarian):
        return librarian.extend_the_book(self, book)


class Librarian(BookRanking):

    def __init__(self, library_name):
        self.library_name = library_name

    @classmethod
    def lend_the_book(cls, library_card, book):
        if len(library_card.borrowed_books) > 4:
            print('you have exceed max count of borrowed books'
                  'please try later or return one of borrowed')
        elif cls.book_items[book] < 1:
            print('Sorry book is not available now')
        else:
            cls.book_items[book] -= 1
            cls.book_rank(book)
            date_start = datetime.datetime.now()
            date_end = date_start + datetime.timedelta(days=14)
            period = date_start.strftime('%d-%m-%y') + ' to ' + date_end.strftime('%d-%m-%y')
            print(f'you have borrowed book {book.name} for period {period}')
            library_card.borrowed_books[book] = date_end

    @classmethod
    def get_the_book(cls, library_card, book):
        cls.book_items[book] += 1
        del library_card.borrowed_books[book]
        print(f'you have returned book {book.name} ')

    @classmethod
    def extend_the_book(cls, library_card, book):
        if cls.high_demand(book):
            print('book has high demand \n sorry extension is refused ')
        else:
            date_start = datetime.datetime.now()
            date_end = date_start + datetime.timedelta(days=7)
            period = date_start.strftime('%d-%m-%y') + ' to ' + date_end.strftime('%d-%m-%y')
            print(f'you have borrowed book {book.name} for period {period}')
            library_card.borrowed_books[book] = date_end

    @classmethod
    def high_demand(cls, book):
        borrowing_times_list = list(cls.rank.values())
        borrowing_times_list.sort()
        hd_value = borrowing_times_list[int((5/100)*len(borrowing_times_list))]
        if cls.rank[book] >= hd_value:
            return True
        else:
            return False


librarian_1 = Librarian('a_lib')
st_id_1 = input('please input your student id: ')
lib_card = LibraryCard(st_id_1)
action = input('please select one of the options:\n borrow, return, extend: ')
book_name = input('please enter book name: ')
book_flag = False
for lib_book in AvailableBooks.books_list:
    if book_name == lib_book.name:
        book_selected = lib_book
        book_flag = True
        break
if book_flag:
    if action == 'borrow':
        lib_card.borrow_book(book_selected, librarian_1)
    elif action == 'return':
        lib_card.return_the_book(book_selected, librarian_1)
    elif action == 'extend':
        lib_card.extend_borrowed(book_selected, librarian_1)
    else:
        print('wrong action')
else:
    print('book is not listed in library')
