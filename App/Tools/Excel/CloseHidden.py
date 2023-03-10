import xlwings


def CloseHidden() -> int:
    Count = 0

    # OLD
    # if xlwings.apps.count != 0:
    #    Books = xlwings.books
    #    for Book in Books:
    #        Book: xlwings.Book = Book
    #        print(Book.name)
    #        App = Book.app

    #        if App.visible == False:
    #            Count += 1
    #            print("Closed:", Book.name)
    #            Book.save()
    #            Book.close()
    #            if len(App.books) == 0:
    #                App.quit()

    Apps = xlwings.apps
    for App in Apps:
        App: xlwings.App = App

        if App.visible == False:

            if len(App.books) != 0:

                Books = App.books
                for Book in Books:
                    Book: xlwings.Book = Book
                    Count += 1
                    print("Closed:", Book.name)
                    Book.save()
                    Book.close()

                App.quit()

    return Count
