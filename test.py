a = [
    {'x': 1},
    {'x': 2},
    {'x': 3},
]
a.sort(reverse=True, key=lambda i: i['x'])
print(a)