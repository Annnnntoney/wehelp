# your code here, maybe
def func2(ss, start, end, criteria):
    if not hasattr(func2, "bookings"):
        func2.bookings = {}
    bookings = func2.bookings

    if ">=" in criteria:
        op = ">="
        field, value = criteria.split(">=")
    elif "<=" in criteria:
        op = "<="
        field, value = criteria.split("<=")
    else:
        op = "="
        field, value = criteria.split("=")

    candi = []
    for s in ss:
        free = True
        for (bs, be) in bookings.get(s["name"], []):
            if start < be and bs < end:   
                free = False
                break
        if not free:
            continue


        if op == "=":                     
            if s["name"] == value:
                candi.append(s)
        else:                             
            num = float(value)
            if op == ">=" and s[field] >= num:
                candi.append(s)
            elif op == "<=" and s[field] <= num:
                candi.append(s)

    if not candi:
        print("Sorry")
        return


    if op == ">=":
        best = min(candi, key=lambda s: s[field])   
    elif op == "<=":
        best = max(candi, key=lambda s: s[field])  
    else:
        best = candi[0]                            


    bookings.setdefault(best["name"], []).append((start, end))
    print(best["name"])


services=[
    {"name":"S1", "r":4.5, "c":1000},
    {"name":"S2", "r":3, "c":1200},
    {"name":"S3", "r":3.8, "c":800}
]

func2(services, 15, 17, "c>=800") # S3
func2(services, 11, 13, "r<=4") # S3
func2(services, 10, 12, "name=S3") # Sorry
func2(services, 15, 18, "r>=4.5") # S1
func2(services, 16, 18, "r>=4") # Sorry
func2(services, 13, 17, "name=S1") # Sorry
func2(services, 8, 9, "c<=1500") # S2
