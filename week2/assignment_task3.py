
def func3(index):
    diffs = [-2, -3, 1, 2]   
    value = 25               
    for k in range(index):   
        value += diffs[k % 4]   
    print(value)

func3(1)   # print 23
func3(5)   # print 21
func3(10)  # print 16
func3(30)  # print 6
