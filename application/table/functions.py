def sort_ascending_switch(sort_ascending):
    if sort_ascending:
        return False
    else:
        return True


def move_columns(datafr, column, direction):
    index_no = datafr.columns.get_loc(column)
    dfpoped = datafr.pop(column)
    index_no += direction
    if index_no < 0:
        index_no = 0
    elif index_no > len(datafr.columns):
        index_no -= 1
    return datafr.insert(loc=index_no, column=dfpoped.name, value=dfpoped.values)


def add_new_column(datafr, col_name, dtype):
    col_content_dict = {"Text": " ",
                        "Number": 0.0,
                        "Status": "status",
                        "Date": ""
                        }

    col_content = "nic"
    if dtype == 'Text':
        col_content = " "
    elif dtype == 'Number':
        col_content = '0.0'

    datafr[col_name] = col_content

    return datafr

