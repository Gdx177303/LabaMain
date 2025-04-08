from abc import ABC, abstractmethod

    class Base(ABC):
        @abstractmethod
        def area(self):
            pass

        @abstractmethod
        def perimeter(self):
            pass


    class Rectangle(Base):

        def __init__(self, length, width):

            self.length = length
            self.width = width


        def area(self):
            return self.length * self.width

        def perimeter(self):

            return 2 * (self.length + self.width)


rect = Rectangle(length 4, width 5)
print("Pole prostokata", rect.area())
print("Obwod prostokata", rect.perimeter())


class Balwan(ABC):

    @abstractmethod
    def create_balwan(self):
        pass

    @abstractmethod
    def delete_balwan(self):
        pass

class CyrkNaKolo(Balwan):

    @abstractmethod
    def create_balwan(self):
        print("Balwand created")

    @abstractmethod
    def delete_balwan(self):
        print("Balwan deleted")

class Cyrk:

    def __init__(self):
        self.spektakl = CyrkNaKolo()

    def wystep(self):
        print("Cyrk started")
        self.spektakl.create_balwan()
        print("Balwan robi cos")
        self.spektakl.delete_balwan()
        print("Koniec wystepu")

cyrk = Cyrk()
cyrk.wystep()