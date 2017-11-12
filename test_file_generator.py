import csv, random


if __name__ == '__main__':
    test_data = []
    with open('product.csv') as f:
        r = csv.reader(f)
        p=[]
        for el in r:
            p.append(el)
            #print(p)
        f.close()

        for i in range(1, random.randint(0,10000)):
            for j in range(0, random.randint(0,200)):
                #rand = random.randint(0, len(p))
                test_data.append([i,random.randint(0,len(p))])
        #print (test_data)
    with open("test_data.csv", "w") as csvfile:
        o = csv.writer(csvfile)
        o.writerow(["ORDER_ID", "SKU_ID"])
        for d in test_data:
            d = list(map(str,d))
            #print (d)
            o.writerow(d)
        csvfile.close()
