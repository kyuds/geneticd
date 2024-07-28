from equations import Griewank

DIMENSIONS = 10

if __name__ == "__main__":
    g = Griewank()
    print(g([10, 1]))
