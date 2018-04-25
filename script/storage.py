class Data(object):

    """Class data """

    def __init__(self):
        """Initialize storage and currnetitem """

        self.storage = []

        self.currentitem = 0

    def add(self, data):
        """Add data to storage index 0."""

        self.storage.insert(0, data)

        self.currentitem = 0

    def remove(self):
        """Remove last element from storage."""

        self.storage.pop()

    def viewData(self):
        """View data in storage."""

        if self.storage == []:
            print("NO DATA IN STORAGE\n")
        else:
            print('DISPLAYING STORAGE DATA:')
            print(self.storage, "\n")

    def isLast(self):
        """ Returns True if current element is last element in storage list"""

        if(self.storage).index(self.storage[self.currentitem]) == len(self.storage) - 1:
            return True
        return False

    def isFirst(self):
        """ Returns True if current element is First element in storage list"""

        if(self.storage).index(self.storage[self.currentitem]) == 0:
            return True
        return False

    def prev(self):
        """ Returns a next element in storage list index + 1"""
        try:
            if Data.isLast(self):

                return self.storage[self.currentitem][0], self.storage[self.currentitem][1]
            else:
                self.currentitem += 1

                return self.storage[self.currentitem][0], self.storage[self.currentitem][1]
        except IndexError:
            pass

    def next(self):
        """ Returns a previous element in storage list index -1"""
        try:
            if Data.isFirst(self):

                return self.storage[self.currentitem][0], self.storage[self.currentitem][1]
            else:
                self.currentitem -= 1

                return self.storage[self.currentitem][0], self.storage[self.currentitem][1]
        except IndexError:
            pass
