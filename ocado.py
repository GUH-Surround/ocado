import csv, sys, ocado_solve, time


def read_orders(filename):
    with open(filename) as f:
        r = csv.DictReader(f)
        orders = []
        for line in enumerate(r):
            orders.append(line)
        f.close()
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
                #   print(i, j, order_lists[i][j])
                dict_form = {"SKU_ID": (reader[order_lists[i][j]+1][0]),
                             "EACH_HEIGHT": float(reader[order_lists[i][j]+1][1]),
                             "EACH_LENGTH": float(reader[order_lists[i][j]+1][2]),
                             "EACH_WIDTH": float(reader[order_lists[i][j]+1][3]),
                             "EACH_WEIGHT": float(reader[order_lists[i][j]+1][4]),
                             "EACH_VOLUME": float(reader[order_lists[i][j]+1][5]),
                             "SEGREGATION_CATEGORY": (reader[order_lists[i][j]+1][6])}
                order_queries[i].append(dict_form)
        f.close()
    return order_queries


if __name__ == '__main__':
    t0 = time.time()

    filename = sys.argv[1]
    # Read in all the orders
    orders = read_orders(filename)

    # print("Time to t1:", time.time() - t0)
    t1 = time.time()

    # Keep track of the total number of orders
    no_orders = int(orders[len(orders) - 1][1]['ORDER_ID'])
    # This will be a list of lists
    # Each element is a list of the product IDs of the indexed order (+1)
    index_dict = {}
    reverse_index_dict = {}
    cur_index = 0
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

    # print("Time to t2:", time.time() - t1)
    t2 = time.time()

    order_queries = []

    order_queries = fast_load(order_lists)

    # print("Time to t3:", time.time() - t2)
    t3 = time.time()

    # at this stage we have order_queries containing a list
    #   of lists of dictionaries containing information about a single
    #   product
    offset = 0
    with open("spotify_dot_exe_stopped_working.rule_10.csv", "w") as o:
        writer = csv.writer(o)
        writer.writerow(['ORDER_ID', 'CONTAINER_ID', 'SKU_ID'])
        for i in range(len(order_queries)):
            result = ocado_solve.process_order(order_queries[i], offset)
            if len(result) > 0:
                offset = result[len(result) - 1][0]

            for r in result:
                writer.writerow(list(map(str, [reverse_index_dict[i], r[0], r[1]])))

        o.close()

    print("Time to finish:", str(time.time() - t0)[:6] + "s")
