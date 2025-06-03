
def arr_size(arr, size):
    s = []
    for i in range(0, int(len(arr)) + 1, size):
        c = arr[i:i + size]
        s.append(c)
    newlist = [x for x in s if x]
    return newlist
