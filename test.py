import re

f = open('./query_bool.txt')
lines = f.readlines()
# i = 0
for line in lines:
    line = line.strip('\n')
    pos1 = line.find(' ')
    query_number = int(line[1:pos1-1])
    query_str = line[pos1+1:]
    print(query_number)
f.close()