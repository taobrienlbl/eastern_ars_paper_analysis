from simplempi.parfor import parfor, pprint

mylist = range(10)

for item in parfor(mylist):
    pprint(item)
