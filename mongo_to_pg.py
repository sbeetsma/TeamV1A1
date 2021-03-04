import PostgresDAO
import MongodbDAO


def retrieve_from_dict(dict: dict, key):
    """Tries to retrieve a value from a dictionairy with a certain key, and catches the KeyError if it doesn't exist.

    Args:
        dict: the dictionairy to retrieve the value from.
        key: the key associated with the desired data.

    Returns:
        if the key exists in the dictionairy, returns the value associated with the key.
        if it doesn't exist, returns None"""
    try:
        return dict[key]
    except KeyError:
        return None


def retrieve_from_dict_depths_recursively(input: dict, keys: list):
    """Function to return value associated with certain key in dictionairy.
    Also able to recursively search any depth of dictionairiy-in-dictionairy construction.

    Will catch KeyError if given a key that doesn't exist, and return None.
    Will also return None if given anything other then an iterable.

    Args:
        input: the dictionairy to access.
        keys: list containing keys, starting from the top level dict going down. One key is also valid.

    Returns:
        Retrieved value if every key in keys was valid.
        None if not.
    """
    if type(input) != dict:
        return None
    if len(keys) == 1:
        return retrieve_from_dict(input, keys[0])
    try:
        return retrieve_from_dict_depths_recursively(input[keys[0]], keys[1:])
    except KeyError:
        return None


def construct_insert_query(table_name: str, var_names: list[str]) -> str:
    """Constructs an SQL insert query, formatted to use %s in place of actual values to allow PsycoPG2 to properly format them.

    Args:
        table_name: the name of the table to insert to insert into.
        var_names: a list containing all the attributes to insert.

    Returns:
        A properly formatted SQL query as string.
    """
    q = f"INSERT INTO {table_name} ("
    q += var_names[0]
    for var in var_names[1:]:
        q += ", " + var
    q += f") VALUES (%s{(len(var_names) - 1) * ', %s'});"
    return q


def simple_mongo_to_sql(mongo_collectie_naam: str, #TODO: write docstring when computer is not dying
                        postgres_db: PostgresDAO.PostgreSQLdb,
                        postgres_table_name: str,
                        mongo_attribute_list: list[str or list[str]],
                        postgres_attribute_list: list[str],
                        reject_if_null_amount: int = 0):
    collection = MongodbDAO.getDocuments(mongo_collectie_naam)
    data_list = []
    for item in collection:
        value_list = []
        for key in mongo_attribute_list:
            if type(key) == list:
                value = retrieve_from_dict_depths_recursively(item, key)
            else:
                value = retrieve_from_dict(item, key)
            value_list.append(value)
        if not (None in value_list[0:reject_if_null_amount]):
            data_list.append(tuple(value_list))
    q = construct_insert_query(postgres_table_name, postgres_attribute_list)
    postgres_db.many_update_queries(q, data_list)

#refresh DB
PostgresDAO.db.regenerate_db("DDL1.txt")
print("DB CLEANED")

#port products
a = "products"
b = PostgresDAO.db
c = "Products"
d = ["_id", "name", ["price", "selling_price"]]
e = ["product_id", "product_name", "selling_price"]
f = 2
simple_mongo_to_sql(a, b, c, d, e, f)


print("PRODUCTS PORTED")
#port session
a = "sessions"
b = PostgresDAO.db
c = "Sessions"
d = ["_id", "segment"]
e = ["session_id", "segment"]
f = 1
simple_mongo_to_sql(a, b, c, d, e, f)
print("SESSIONS PORTED")
