import itertools


# categorize into a list of lists of products(dicts)
def get_categories(order):
    categories = [[] for x in range(8)]

    for product in order:
        if int(product["SEGREGATION_CATEGORY"]) == 1:
            categories[0].append(product)
        if int(product["SEGREGATION_CATEGORY"]) == 2:
            categories[0].append(product)
        if int(product["SEGREGATION_CATEGORY"]) == 3:
            categories[1].append(product)
        if int(product["SEGREGATION_CATEGORY"]) == 4:
            categories[2].append(product)
            #categories[5].append(product)
        if int(product["SEGREGATION_CATEGORY"]) == 5:
            categories[3].append(product)
        if int(product["SEGREGATION_CATEGORY"]) == 6:
            categories[4].append(product)
        if int(product["SEGREGATION_CATEGORY"]) == 7:
            #categories[5].append(product)
            categories[6].append(product)
        if int(product["SEGREGATION_CATEGORY"]) == 8:
            #categories[6].append(product)
            categories[7].append(product)

    return categories


def normalize(inp):
    for d in inp:
        length, width, height = d["EACH_LENGTH"], d["EACH_WIDTH"], d["EACH_HEIGHT"]
        ordered = [length, width, height]
        ordered.sort()
        d["EACH_LENGTH"], d["EACH_WIDTH"], d["EACH_HEIGHT"] = ordered[2], ordered[1], ordered[0]


# product keys - SKU_ID, EACH_HEIGHT, EACH_WIDTH, EACH_LENGTH, EACH_WEIGHT, EACH_VOLUME
def package(products):
    # return [[0,0],[1,1]]
    # box info:
    #   max weight - 16kg
    #   max length - 55cm
    #   max width  - 36cm
    #   max height - 33cm
    #   max volume - 65340cm^3

    result_list = []
    current_id = 1
    current_x = 0.0
    current_lower_z = 0.0
    current_upper_z = 0.0
    current_weight = 0.0
    while len(products) > 0:
        max_weight_reached = True
        max_height_reached = True

        for prod in products:

            if prod["EACH_LENGTH"] > 55.0:
                products.remove(prod)
                pass
            elif prod["EACH_WIDTH"] > 36.0:
                products.remove(prod)
                pass
            elif prod["EACH_HEIGHT"] > 33.0:
                products.remove(prod)
                pass
            elif prod["EACH_WEIGHT"] > 16.0:
                products.remove(prod)
                pass


            elif current_x + prod["EACH_WIDTH"] <= 55.0:
                if current_lower_z + prod["EACH_HEIGHT"] <= 33.0:
                    if current_weight + prod["EACH_WEIGHT"] <= 16.0:
                        result_list.append([current_id, int(prod["SKU_ID"])])
                        products.remove(prod)
                        # update box x val
                        current_x += prod["EACH_WIDTH"]
                        # check if max_height should be updated
                        if current_upper_z + prod["EACH_HEIGHT"] > current_upper_z:
                            current_upper_z += prod["EACH_HEIGHT"]
                elif current_weight + prod["EACH_WEIGHT"] <= 16.0:
                    max_weight_reached = False
            elif current_lower_z + prod["EACH_HEIGHT"] <= 33.0:
                max_height_reached = False
            elif current_weight + prod["EACH_WEIGHT"] <= 16.0:
                max_weight_reached = False

        if max_height_reached or max_weight_reached:
            current_x = 0
            current_lower_z = 0
            current_upper_z = 0
            current_weight = 0
            current_id += 1
        else:
            current_lower_z = current_upper_z
            current_x = 0
        # print(current_id, current_x, current_lower_z, current_upper_z, max_height_reached)

    return result_list


def process_order(order, offset):
    # categories to be processed together:
    #   [1,2] ; [3] ; [4] ; [5] ; [6] ; [4,7] ; [7,8] ; [8]

    categories = get_categories(order)
    for cat in categories:
        normalize(cat)

    boxed_products = list(map(package, categories))

    boxed_products = [x for x in boxed_products if x != []]

    # coab : corresponding <i forgot the rest of the acronym>
    coab = []
    for boxed_category in boxed_products:
        coab.append(boxed_category[len(boxed_category) - 1][0])

    #print(coab)

    # late night tired magic don't touch
    for j in range(len(boxed_products[0])):
        boxed_products[0][j][0] = boxed_products[0][j][0] + offset
    for i in range(1, len(boxed_products)):
        for j in range(len(boxed_products[i])):
            boxed_products[i][j][0] = boxed_products[i][j][0] + sum(coab[:i]) + offset

    return list(itertools.chain(*boxed_products))
