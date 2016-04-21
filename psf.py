1、插入排序  
def insert_sort(lists):  
    # 插入排序  
    count = len(lists)  
    for i in range(1, count):  
        key = lists[i]  
        j = i - 1  
        while j >= 0:  
            if lists[j] > key:  
                lists[j + 1] = lists[j]  
                lists[j] = key  
            j -= 1  
    return lists  
   
2、希尔排序  
def shell_sort(lists):  
    # 希尔排序  
    count = len(lists)  
    step = 2  
    group = count / step  
    while group > 0:  
        for i in range(0, group):  
            j = i + group  
            while j < count:  
                k = j - group  
                key = lists[j]  
                while k >= 0:  
                    if lists[k] > key:  
                        lists[k + group] = lists[k]  
                        lists[k] = key  
                    k -= group  
                j += group  
        group /= step  
    return lists  
   
3、冒泡排序  
def bubble_sort(lists):  
    # 冒泡排序  
    count = len(lists)  
    for i in range(0, count):  
        for j in range(i + 1, count):  
            if lists[i] > lists[j]:  
                lists[i], lists[j] = lists[j], lists[i]  
    return lists  
   
4、快速排序  
def quick_sort(lists, left, right):  
    # 快速排序  
    if left >= right:  
        return lists  
    key = lists[left]  
    low = left  
    high = right  
    while left < right:  
        while left < right and lists[right] >= key:  
            right -= 1  
        lists[left] = lists[right]  
        while left < right and lists[left] <= key:  
            left += 1  
        lists[right] = lists[left]  
    lists[right] = key  
    quick_sort(lists, low, left - 1)  
    quick_sort(lists, left + 1, high)  
    return lists  
   
5、直接选择排序  
def select_sort(lists):  
    # 选择排序  
    count = len(lists)  
    for i in range(0, count):  
        min = i  
        for j in range(i + 1, count):  
            if lists[min] > lists[j]:  
                min = j  
        lists[min], lists[i] = lists[i], lists[min]  
    return lists  
   
6、堆排序  
# 调整堆  
def adjust_heap(lists, i, size):  
    lchild = 2 * i + 1  
    rchild = 2 * i + 2  
    max = i  
    if i < size / 2:  
        if lchild < size and lists[lchild] > lists[max]:  
            max = lchild  
        if rchild < size and lists[rchild] > lists[max]:  
            max = rchild  
        if max != i:  
            lists[max], lists[i] = lists[i], lists[max]  
            adjust_heap(lists, max, size)  
# 创建堆  
def build_heap(lists, size):  
    for i in range(0, (size/2))[::-1]:  
        adjust_heap(lists, i, size)  
# 堆排序  
def heap_sort(lists):  
    size = len(lists)  
    build_heap(lists, size)  
    for i in range(0, size)[::-1]:  
        lists[0], lists[i] = lists[i], lists[0]  
        adjust_heap(lists, 0, i)  
   
7、归并排序  
def merge(left, right):  
    i, j = 0, 0  
    result = []  
    while i < len(left) and j < len(right):  
        if left[i] <= right[j]:  
            result.append(left[i])  
            i += 1  
        else:  
            result.append(right[j])  
            j += 1  
    result += left[i:]  
    result += right[j:]  
    return result  
def merge_sort(lists):  
    # 归并排序  
    if len(lists) <= 1:  
        return lists  
    num = len(lists) / 2  
    left = merge_sort(lists[:num])  
    right = merge_sort(lists[num:])  
    return merge(left, right)  
   
8、基数排序  
import math  
def radix_sort(lists, radix=10):  
    k = int(math.ceil(math.log(max(lists), radix)))  
    bucket = [[] for i in range(radix)]  
    for i in range(1, k+1):  
        for j in lists:  
            bucket[j/(radix**(i-1)) % (radix**i)].append(j)  
        del lists[:]  
        for z in bucket:  
            lists += z  
            del z[:]  
    return lists
