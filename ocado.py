import csv, sys, ocado_solve


def read_orders():
    with open('orderBoi.csv') as f:
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


if __name__ == '__main__':
    # Read in all the orders
    orders = read_orders()
    # Keep track of the total number of orders
    no_orders = int(orders[len(orders) - 1][1]['ORDER_ID'])
    # This will be a list of lists
    # Each element is a list of the product IDs of the indexed order (+1)
    order_lists = []
    for i in range(0, no_orders):
        order_lists.append([])
    for i in range(0, len(orders)):
        index = int(orders[i][1]['ORDER_ID']) - 1
        order_lists[index].append(int(orders[i][1]['SKU_ID']))

    order_queries = []
    # Now we want to return a dictionary for every product in a particular order
    with open('product.csv') as f:
        r = csv.DictReader(f)
        for i in range(0, len(order_lists)):
            current_order_list = []
            for line_number, line in read_my_lines(r, order_lists[i]):
                # print (line_number, line)
                for key in line:
                    line[key] = float(line[key])
                current_order_list.append(line)

            # [dict([a, float(x)] for a, x in b.items()) for b in current_order_list]
            order_queries.append(current_order_list)
        f.close()

    # at this stage we have order_queries containing a list
    #   of lists of dictionaries containing information about a single
    #   product



    print (ocado_solve.process_order(order_queries[0]))



    # end
