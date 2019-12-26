from bamboo_bot import Bamboo_Bot

b = Bamboo_Bot()
print('types')
types = b.client.get_time_off_types()
for t in types:
    print(t)
# print('policies')
# pols = b.client.get_time_off_policies()
# for p in pols:
#     print(p)