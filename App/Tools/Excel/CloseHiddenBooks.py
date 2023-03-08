import xlwings

if xlwings.apps.count != 0:
    Books = xlwings.books
    for Book in Books:
        Book: xlwings.Book = Book
        print(Book.name)
        App = Book.app

        if App.visible == False:
            print("Closed:", Book.name)
            Book.save()
            Book.close()
            if len(App.books) == 0:
                App.quit()
