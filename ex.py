class A:
    def __init__(self):
        pass

    def y(self):
        return 0

class B(A):
    def __init__(self):
        super()
        self.x = 1
    
    def y(self):
        return self.x

def testing(obj: A):
    print(obj.x)


def run():
    testing(B())

if __name__ == "__main__":
    run()
