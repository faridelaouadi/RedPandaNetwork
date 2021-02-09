from testing import *
import asyncio

filepaths = [1,2,3,4,5,6,7,8,9,10,11]

results = asyncio.run(main(filepaths))
print(results)

def break_up_filepaths(filepaths,divisor):
    number_of_lists = ( len(filepaths) // divisor ) + 1# 11//5 = 2
    list_of_lists = []
    counter = 0
    for i in range(len(number_of_lists)):
        sub_list = filepaths[counter:counter+divisor]
        list_of_lists.append(sub_list)
        counter += divisor
    print(list_of_lists)

break_up_filepaths(filepaths,5)