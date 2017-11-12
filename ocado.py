import csv, sys, ocado_solve, time


def read_orders(filename):
    with open(filename) as f:
        r = csv.DictReader(f)
        orders = []
        for line in enumerate(r):
            orders.append(line)
        return orders


def read_my_lines(csv_reader, lines_list):
    f.seek(0)
    for line_number, row in enumerate(csv_reader):
        for index in range(0, len(lines_list)):
            if (line_number == lines_list[index]):
                yield line_number, row


def read_my_lines_0(csv_reader, lines_list):
    f.seek(0)
    for line_number, row in enumerate(csv_reader):
        for index in range(0, len(lines_list)):
            if line_number == lines_list[index] - 1:
                yield line_number, row


def fast_load(order_lists):
    order_queries = [[] for x in range(len(order_lists))]

    with open('product.csv') as f:
        reader = csv.reader(f)
        reader = list(reader)
        for i in range(len(order_lists)):
            for j in range(len(order_lists[i])):
                dict_form = {"SKU_ID": (reader[order_lists[i][j]][0]),
                             "EACH_HEIGHT": float(reader[order_lists[i][j]][1]),
                             "EACH_LENGTH": float(reader[order_lists[i][j]][2]),
                             "EACH_WIDTH": float(reader[order_lists[i][j]][3]),
                             "EACH_WEIGHT": float(reader[order_lists[i][j]][4]),
                             "EACH_VOLUME": float(reader[order_lists[i][j]][5]),
                             "SEGREGATION_CATEGORY": (reader[order_lists[i][j]][6])}
                order_queries[i].append(dict_form)
        f.close()
    return order_queries


if __name__ == '__main__':
    t0 = time.time()

    filename = sys.argv[1]
    # Read in all the orders
    orders = read_orders(filename)

    print("Time to t1:", time.time() - t0)
    t1 = time.time()

    # Keep track of the total number of orders
    no_orders = int(orders[len(orders) - 1][1]['ORDER_ID'])
    # This will be a list of lists
    # Each element is a list of the product IDs of the indexed order (+1)
    index_dict = {}
    reverse_index_dict = {}
    cur_index=0
    order_lists = []

    for i in range(0, len(orders)):

        if int(orders[i][1]['ORDER_ID']) in index_dict:
            index = index_dict[int(orders[i][1]['ORDER_ID'])]
        else:
            order_lists.append([])
            index_dict[int(orders[i][1]['ORDER_ID'])] = cur_index
            reverse_index_dict[cur_index] = int(orders[i][1]['ORDER_ID'])
            index = cur_index
            cur_index += 1

        order_lists[index].append(int(orders[i][1]['SKU_ID']))

    print("Time to t2:", time.time() - t1)
    t2 = time.time()

    #print(order_lists)

    order_queries = []
    print(orders)


    # Now we want to return a dictionary for every product in a particular order
    # with open('product.csv') as f:
    #      r = csv.DictReader(f)
    #      for i in range(0, len(order_lists)):
    #          current_order_list = []
    #          for line_number, line in read_my_lines(r, order_lists[i]):
    #              # print (line_number, line)
    #              for key in line:
    #                  line[key] = float(line[key])
    #              current_order_list.append(line)
    #
    #           # [dict([a, float(x)] for a, x in b.items()) for b in current_order_list]
    #          order_queries.append(current_order_list)
    #      f.close()

    order_queries = fast_load(order_lists)

    print("Time to t3:", time.time() - t2)
    t3 = time.time()

    # at this stage we have order_queries containing a list
    #   of lists of dictionaries containing information about a single
    #   product
    offset = 0
    for i in range(len(order_queries)):
        result = ocado_solve.process_order(order_queries[i], offset)
        offset = result[len(result)-1][0]

        for r in result:
            print(reverse_index_dict[i], r[0], r[1])
    #print(ocado_solve.process_order(order_queries[0]))
    print("Time to finish:", time.time() - t3)