import csv, sys



def main():
    orders = []
    with open(sys.argv[1]) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        orders = list(csvReader)

    orders.pop(0)
    for order in orders:
        order = list(map(int, order))
        #print (order)


    with open('product.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            pass

class Product:
    id = 0
    width = 0
    height = 0
    length = 0
    category = 0
    weight = 0
    volume = 0
    x = 0
    y = 0
    z = 0

    def __init__(self, id, width, length, height, catagory, weight):
        self.id = id
        self.width = width
        self.height = height
        self.length = length
        self.weight = weight
        self.category = catagory
        #print (width, height, length)
        self.volume = height * width * length


    def get_volume(self):
        return self.volume

    def get_category(self):
        return self.category

    def get_surface_area(self):
        return self.length * self.width

    def get_height(self):
        return self.height

    def normalize(self):
        vals = [self.width, self.length, self.height]
        vals.sort()
        self.length = vals[0]
        self.width = vals[1]
        self.height = vals[2]


    def set_coords(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z



class Box:
    id = 0
    products = []
    cur_weight = 0
    weight = 16.0
    width = 36.0
    breadth = 55.0
    height = 33.0
    volume = 65340
    cur_volume = 0
    max_zval = 0
    max_xval = 0

    def __init__(self, id):
        self.id = id

    def get_max_zval(self):
        return self.max_zval

    def get_max_xval(self):
        return self.max_xval

    def get_weight(self):
        return self.weight

    def get_cur_weight(self):
        total = 0
        for prod in self.products:
            total += prod.get_weight()
        return total

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_breadth(self):
        return self.breadth

    def get_volume(self):
        return self.volume

    def get_cur_volume(self):
        return self.cur_volume

    def add_product(self, product):
        product.append(product)




def solve(order):
    products = []
    for prod in order:
        id = prod.get("SKU_ID")
        #width = prod.get("EACH_WIDTH")
        width = prod['EACH_WIDTH']
        #height = prod.get("EACH.HEIGHT")
        length = prod["EACH_LENGTH"]
        height = prod["EACH_HEIGHT"]
        #weight = prod.get("EACH_WEIGHT")
        weight = prod["EACH_WEIGHT"]
        category = prod.get("SEGREGATION_CATEGORY")
        product = Product(id, float(width), float(length), float(height), category, weight)
        product.normalize()
        products.append(product)

    print (products)

    cat12 = list(filter(lambda x: x.get_category()==1 or x.get_category()==2, products))
    cat3 = list(filter(lambda x: x.get_category()==3, products))
    cat4 = list(filter(lambda x: x.get_category() == 4, products))
    cat5 = list(filter(lambda x: x.get_category() == 5, products))
    cat6 = list(filter(lambda x: x.get_category() == 6, products))
    cat7 = list(filter(lambda x: x.get_category() == 7, products))
    cat8 = list(filter(lambda x: x.get_category() == 8, products))


    #print (cat12)
    boxes = []
    box_id = 0
    cat12_boxes, box_id = boxify(cat12,box_id)
    cat3_boxes, box_id = boxify(cat3, box_id)
    cat4_boxes, box_id = boxify(cat4, box_id)
    cat5_boxes, box_id = boxify(cat5, box_id)
    cat6_boxes, box_id = boxify(cat6, box_id)
    cat7_boxes, box_id = boxify(cat7, box_id)
    cat8_boxes, box_id = boxify(cat8, box_id)
    boxes.append(cat12_boxes)
    boxes.append(cat3_boxes)
    boxes.append(cat4_boxes)
    boxes.append(cat5_boxes)
    boxes.append(cat6_boxes)
    boxes.append(cat7_boxes)
    boxes.append(cat8_boxes)

    result = []
    for boxs in boxes:
        print (boxs)
        result += boxs

    final_result = []
    for box in result:
        for product in box.products:
            final_result.append([box.id, product.id])

    return final_result


def category_sort(category):
    for i in range(1, len(category)):
        tmp = category[i]
        k = i
        while k > 0 and tmp.get_surface_area() > category[k - 1].get_surface_area():
            category[k] = category[k - 1]
            k -= 1
        category[k] = tmp
    return category


def place_in_box(box, products):
    for prod in products:
        if box.get_max_zval() + prod.get_height() <= box.get_height():
            if box.get_max_xval() + prod.get_width() <= box.get_width():
                if box.get_cur_weight() + prod.get_weight() <= box.weight:
                    box.add_product(prod)
                    return True, box, prod
    return False, box, None



def boxify(category,id):
    boxes = []
    box = Box(id)
    id+=1
    category = category_sort(category)
    while len(category) > 0:
        # find next best prod to add to boxy boi
        added, box, popper = place_in_box(box, category)
        if added:
            category.pop(popper)
            if len(category) == 0:
                boxes.append(box)
        else:
            boxes.append(box)
            box = Box()

    return boxes, id

def read_orders():
    with open('orderBoi.csv') as f:
        r = csv.DictReader(f)
        orders = []
        for line in enumerate(r):
            orders.append(line)
        return orders


def read_my_lines(csv_reader, lines_list):
    #print (lines_list)
    f.seek(0)
    for line_number, row in enumerate(csv_reader):
        for index in range (0, len(lines_list)):
            if (line_number == lines_list[index]):
                yield line_number, row

def read_my_lines_0(csv_reader, lines_list):
    #print (lines_list)
    f.seek(0)
    for line_number, row in enumerate(csv_reader):
        for index in range (0, len(lines_list)):
            if (line_number == lines_list[index]-1):
                yield line_number, row


if __name__ == '__main__':
    # Read in all the orders
    orders = read_orders()
    # Keep track of the total number of orders
    no_orders = int(orders[len(orders)-1][1]['ORDER_ID'])
    # This will be a list of lists
    # Each element is a list of the product IDs of the indexed order (+1)
    order_lists = []
    for i in range (0, no_orders):
        order_lists.append([])
    for i in range (0, len(orders)):
        index = int(orders[i][1]['ORDER_ID']) - 1
        order_lists[index].append(int(orders[i][1]['SKU_ID']))

    # Now we want to return a dictionary for every product in a particular order
    with open('product.csv') as f:
        r = csv.DictReader(f)
        for i in range (0, len(order_lists)):
            current_order_list = []
            for line_number, line in read_my_lines(r, order_lists[i]):
                    #print (line_number, line)
                current_order_list.append(line)
            print (solve(current_order_list))
        f.close()

#main()

