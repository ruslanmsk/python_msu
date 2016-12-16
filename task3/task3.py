class Error(Exception):
    pass

class DisparityError(Error):
    #несоразмерность
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class TypeError(Error):
    # неправельный тип
    def __init__(self, message):
        self.message = message

class IndexError(Error):
    def __init__(self,message):
        self.message = message

class GetError(Error):
    def __init__(self, message):
        self.message = message



class Matrix:
    A = []
    b = []
    x = []

    def __init__(self, A_, b_):
        try:
            n = len(A_[0])
            for i in range(n):
                self.x.append(0)

            if len(b) != n:
                raise DisparityError("len(b) != n","Неверное размерность столбца")

            for i in A_:
                if len(i) != n:
                    raise DisparityError("len(i) != len(A_[0])","Недопустимый размер матрицы")
                for j in i:
                    if type(j) != int:
                        raise TypeError("Элементы не целые числа")

            for i in b_:
                if type(j) != int:
                    raise TypeError("Элементы не целые числа")

        except DisparityError as err:
            print(err.message)
        except TypeError as err:
            print(err.message)
        else:
            self.A = A_[:]
            self.b = b_[:]

    def __getitem__(self, item):
        A = self.A[:]
        b = self.b[:]

        k = 0
        m = len(A)
        n = len(A[0])

        try:
            if item < 0 or item >= n:
                raise IndexError("Неверный индекс")
            while k < m:
                # Поиск строки с максимальным A[i][k]
                max = abs(A[k][k])
                index = k
                for i in range(k + 1, m, 1):
                    if abs(A[i][k]) > max:
                        max = abs(A[i][k])
                        index = i

                # Перестановка строк
                if max == 0:
                    # нет ненулевых диагональных элементов
                    raise DisparityError("max == 0","Нулевая колонка матрицы")

                for j in range(m):
                    A[k][j], A[index][j] = A[index][j], A[k][j]

                b[k], b[index] = b[index], b[k]

                # Нормализация уравнений
                for i in range(k, n, 1):
                    tmp = A[i][k]
                    if abs(tmp) == 0:
                        continue  # для нулевого коэффициента пропустить
                    for j in range(n):
                        A[i][j] = A[i][j] / tmp
                    b[i] = b[i] / tmp
                    if i == k:
                        continue  # уравнение не вычитать само из себя
                    for j in range(n):
                        A[i][j] = A[i][j] - A[k][j]
                    b[i] = b[i] - b[k]
                k += 1
            # обратная
            for k in range(m - 1, -1, -1):
                self.x[k] = b[k]
                for i in range(k):
                    b[i] = b[i] - A[i][k] * self.x[k]

        except IndexError as err:
            print(err.message)
        except DisparityError as err:
            print(err.message)
        else:
            return self.x[item]

    def __setitem__(self, item, value):
        try:
            raise GetError("Нельзя переопределить элемент")
        except GetError as err:
            print(err.message)


A = [[2, 1, 1], [1, 1, 0], [3, -1, 2]]
b = [2, -2, 2]

m = Matrix(A, b)
print(m[2])
m.__setitem__(3,3)
