def func(**kwargs):
    print(kwargs)

func(name='name', value='value')

# wrong
# func({
#     'name': 'name',
#     'value': 'value'
# })