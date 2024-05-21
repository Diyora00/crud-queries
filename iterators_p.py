class Fibonacci:
    def __init__(self, n):
        self.first = 0  # first term of fibonacci series
        self.second = 1  # second term of fibonacci series
        self.n = n  # number of terms
        self.till = 1  # variable to control terms  
        self.current = 0  # variable to get current term
        pass

    def __iter__(self):
        return self

    def __next__(self):
        if self.till == 1:
            self.till += 1
            return self.first
        if self.till == 2:
            self.till += 1
            return self.second
        if self.till > self.n:
            raise StopIteration
        self.current = self.first + self.second
        self.first = self.second
        self.second = self.current
        self.till += 1
        return self.current


f = Fibonacci(7)
print(next(f))
print(next(f))
print(next(f))
print(next(f))
print(next(f))
print(next(f))
print(next(f))
# for i in f:
#     print(i)
