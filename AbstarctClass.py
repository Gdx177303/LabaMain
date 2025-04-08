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