def read_tha_books():
    """
    Analyse books from daScrolls.csv file. Count each of the type.
    :return: List of tuples in format [(type_of_book1, count1), (type_of_book2, count2)..]
    """

def load_books():
    books = []
    with open("daScrolls.csv", "r") as book_file:
        lines = book_file.readlines()
        for line in lines:
            row = line.split(";")
            books.append(row[1])

    dic = {}
    for i in range(len(books)):
        if books[i] in dic:
            dic[books[i]] += 1
        else:
            dic[books[i]] = 1
    dic["Other"] = dic.pop("")
    return list(dic.items())


  # if self.book_type from books
class Book:
    def __init__(self, name, book_type = , ability):
        self.name = name
        self.book_type = book_type
        self.ability = ability

    def __str__(self):
        return "Name: {0} type: {1} skill: {2}" (self.name, self.book_type, self.ability)
def load_books():
    books = []
    with open("daScrolls.csv", "r") as book_file:
        lines = book_file.readlines()
        for line in lines:
            row = line.split(";")
            books.append(Book(row[0], row[1], row[2]))


