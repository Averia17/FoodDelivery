def filtering(products: list, params: dict):
    for attr in [x for x in params if params[x] is not None]:
        if attr.endswith("__lte"):
            attr_name = attr.split("__")[0]
            i = 0
            while i < len(products):
                if getattr(products[i], attr_name) > params[attr]:
                    products.pop(i)
                else:
                    i += 1

        elif attr.endswith("__gte"):
            attr_name = attr.split("__")[0]
            i = 0
            while i < len(products):
                if getattr(products[i], attr_name) < params[attr]:
                    products.pop(i)
                else:
                    i += 1
        else:
            i = 0
            while i < len(products):
                if getattr(products[i], attr) != params[attr]:
                    products.pop(i)
                else:
                    i += 1
    return products
