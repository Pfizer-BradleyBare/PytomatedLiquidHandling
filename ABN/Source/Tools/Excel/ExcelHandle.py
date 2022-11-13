import xlwings
import pythoncom
import threading


class ExcelHandle:
    Lock = threading.Lock()

    def __init__(self, Visible: bool):
        self.App: xlwings.App | None = None
        self.Book: xlwings.Book | None = None
        self.Visible: bool = Visible

    def __enter__(self):
        ExcelHandle.Lock.acquire()
        return self

    def __exit__(self, type, value, traceback):
        if self.Book is not None:
            self.Book.save()
            self.Book.close()

            if self.App is not None:
                if len(self.App.books) == 0:
                    self.App.quit()

        ExcelHandle.Lock.release()

    def IsValid(self) -> bool:
        return self.Book is not None

    def OpenBook(self, ExcelFilePath: str):
        if xlwings.apps.count != 0:
            for Book in xlwings.books:
                if Book.fullname == ExcelFilePath:
                    self.App = Book.app
                    self.Book = Book

        if self.App is None:
            pythoncom.CoInitialize()  # Required for some reason.
            self.App = xlwings.App(visible=self.Visible, add_book=False)
            self.Book = self.App.books.open(ExcelFilePath)

    def GetBook(self) -> xlwings.Book:
        if self.Book is None:
            raise Exception("Excel Book not open!")

        return self.Book
