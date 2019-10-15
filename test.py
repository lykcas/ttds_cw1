import re

f = open('./query.txt')
lines = f.readlines()
i = 0
for line in lines:
    line = line.strip('\n')
    pos1 = line.find(' ')
    query_number = int(line[0:pos1])
    query_str = line[pos1+1:]
    print(query_number)
f.close()