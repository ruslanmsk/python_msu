import time
import random


# возведение в степень
def exponentiation(a, n):
    if n == 0:
        return 1
    if n % 2 == 1:
        return a * exponentiation(a, n - 1)
    else:
        b = exponentiation(a, n / 2)
        return b * b;


# печать десятичной записи числа рекурсивно
def printDecimalNumber(n):
    print(str(n)[0], end="")
    if len(str(n)) > 1:
        rank = 1
        while len(str(rank)) < len(str(n)):
            rank *= 10
        printDecimalNumber(n - int(str(n)[0]) * rank)


# вывод n максимальных чисел из двух списков
def maximum(l1, l2, n):
    if len(l1) + len(l2) < n:
        print("Некорректное значение n")
        return
    quickSort(l1)
    quickSort(l2)
    sort_arr = []
    while n > 0:
        if len(l1) == 0:
            if len(l2) == 0:
                print("Нет n различных чисел")
                return
            if len(sort_arr) > 0:
                if sort_arr[len(sort_arr) - 1] == l2[len(l2) - 1]:
                    l2.pop()
                    continue
            sort_arr.append(l2[len(l2) - 1])
            l2.pop()

        if len(l2) == 0:
            if len(l1) == 0:
                print("Нет n различных чисел")
                return
            if len(sort_arr) > 0:
                if sort_arr[len(sort_arr) - 1] == l1[len(l1) - 1]:
                    l1.pop()
                    continue
            sort_arr.append(l1[len(l1) - 1])
            l1.pop()

        if l1[len(l1) - 1] > l2[len(l2) - 1]:
            if len(sort_arr) > 0:
                if sort_arr[len(sort_arr) - 1] == l1[len(l1) - 1]:
                    l1.pop()
                    continue
            sort_arr.append(l1[len(l1) - 1])
            l1.pop()
        else:
            if len(sort_arr) > 0:
                if sort_arr[len(sort_arr) - 1] == l2[len(l2) - 1]:
                    l2.pop()
                    continue
            sort_arr.append(l2[len(l2) - 1])
            l2.pop()
        n -= 1
    return sort_arr


# все что относится к сортировке
def quickSort(alist):
    quickSortHelper(alist, 0, len(alist) - 1)


def quickSortHelper(alist, first, last):
    if first < last:
        splitpoint = partition(alist, first, last)
        quickSortHelper(alist, first, splitpoint - 1)
        quickSortHelper(alist, splitpoint + 1, last)


def partition(alist, first, last):
    pivotvalue = alist[first]
    leftmark = first + 1
    rightmark = last
    done = False
    while not done:
        while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
            leftmark = leftmark + 1
        while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark - 1
        if rightmark < leftmark:
            done = True
        else:
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp
    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp
    return rightmark


# конец сотрировки


# вычисление времени в k итерациях в массивах длины m по поиску n наибольших чисел
def result(m, n, k):
    timer = 0
    for i in range(k):
        a = [random.randint(0, 2 * m) for i in range(m)]
        b = [random.randint(0, 2 * m) for i in range(m)]
        start = time.clock()
        maximum(a, b, n)
        end = time.clock()
        timer += end - start
    return timer / k


# функция для первого задания
def task1():
    f = open('results_КучеровРИ.txt', 'w')
    params = [[10, 1, 2, 5], [100, 2, 5, 10], [1000, 5, 50, 100], [1000000, 5, 100, 1000]]
    k = 10
    for i in range(len(params)):
        m = params[i][0]
        for j in range(len(params[i]) - 1):
            n = params[i][j + 1]
            res = result(m, n, k)
            f.write('M = ' + str(m) + ', N = ' + str(n) + ', time = ' + str(res) + 's\n')
    f.close()


# получение всех элементов начиная с максимального в произвольном количестве списков(min-не выводить ничего ниже этого)
def getSortElems(n, *lists, min=None):
    allList = []
    for i in range(len(lists)):
        allList += lists[i]

    allList = list(set(allList))
    allList = sorted(allList)
    i = 1
    if n > len(allList):
        maxCount = len(allList)
    else:
        maxCount = n
    while i <= maxCount:
        if min is not None:
            if allList[len(allList) - i] >= min:
                yield allList[len(allList) - i]
                i += 1
        else:
            yield allList[len(allList) - i]
            i += 1
