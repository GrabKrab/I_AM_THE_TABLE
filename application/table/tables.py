import pandas as pd
import numpy as np
import datetime

TablesDict = {}


class Table(object):
    """
        Po zaimportowaniuz nowej tabeli z pliku Excel, index 0 jest opisem kolumn, zostaje usuniętyz dataframe
        i przechodzi do Col_descr_List. Col_descr_list będie zmieniało pozycję wraz z przesuwaniem kolumn
        Utworzenie nowej tabeli (dataframe), automatycznie Col_descr_list w __init__
    """
    def __init__(self, name):
        self.name = name
        self.tableDescr = "Table description string"  # opis tabeli
        self.datafr = pd.DataFrame(data=[["Task1", "Working on it", "High", str(datetime.datetime.now().date()), 1]],
                                   columns=["Text", "Status", "Priority", "Date", "Number"])  # creates a default table
        """ poniższe DataFrame opisuje głowny datatframe, jest kopią kolumn,
            lecz nie zawiera danych, a jedynie opisy i parametry
            Nazwy kolumn pokrywają się z głownym dataframe.
            Podczas gdy głowny jest tabela zawierajaca tylko dane (w xls bedzie to 'Arkusz1),
            tak datafr_descr bedzie tabela zawierajacą kolejno:
            index 0: - opis typu kolumny
            index 1: - description
            index 2: - opis parametrów (ustawianych z preferencji), dla typu:
                        - Text: ['short_text', 'long_text']
                        - Status: 'Which label means assignments are done'
                        - Priority: Właściwosci nie są wymagane potrzebne
                        - Number: [float, integer, ...]
                        - Date: 
            index 3: column permissions: ['Restrict column Edit', 'Restrict column view'] for multiusers
                
        """
        self.datafr_descr = pd.DataFrame(data=[["Text", "Status", "Priority", "Date", "Number"],
                                               ["", "", "", "", ""],
                                               ["short_text", "Done", "", "Date", "int"],
                                               [np.NaN, np.NaN, np.NaN, np.NaN, np.NaN]],
                                         columns=["Text", "Status", "Priority", "Date", "Number"])
        self.datafr_descr = pd.DataFrame(columns=[col for col in self.datafr.columns],
                                         data=[[col for col in self.datafr.columns],
                                               ["" for x in range(len(self.datafr.columns))]])
        self.col_descr_list = ["Text", "Status", "Priority", "Date", "Number"]
        # All available type description ["Text", "Number", "Status", "Priority", "Date", "Timeline"]
        self.priority_types = {"Critical": "bg-danger text-white",
                               "High": "bg-warning text-dark",
                               "Medium": "bg-primary text-white",
                               "Low": "bg-success text-white",
                               "Empty1": "bg-secondary text-white",
                               "Empty2": "bg-info text-white",
                               "Empty3": "bg-white text-dark",
                               "Empty4": "bg-dark text-white",
                               }
        self.status_types = {"Working on it": "bg-warning text-dark",
                             "Waiting for review": "bg-primary text-white",
                             "Approved": "bg-info text-white",
                             "Done": "bg-success text-white",
                             "Stuck": "bg-danger text-white",
                             "Empty1": "bg-secondary text-white",
                             "Empty2": "bg-white text-dark",
                             "Empty3": "bg-dark text-white",
                             }
        self.col_default_content_dict = {"Text": " ",
                                         "Number": 0.0,
                                         "Status": "Working on it",
                                         "Priority": "Low",
                                         "Date": str(datetime.datetime.now().date()),
                                         "Timeline": "Timeline"
                                         }




    # def load_data(self, file):
    #
    #     if request.method == 'POST':
    #         print(request.form)
    #         if request.form.get('csvfile'):
    #             print("sraaaaaaaaaaaa")
    #             if request.form['csvfile']:
    #                 url = 'D:\\Projects\\Python\\CPDZTM\\csv_in_flask\\'
    #                 file = request.form['csvfile']
    #                 print(file)
    #                 datafr = pd.read_csv(url + file)
    #                 return table_view()
    #         else:
    #             return redirect(url_for('home'))
    #     else:
    #         return table_view()

    def new_name(self, new_name):
        self.name = new_name
        return self.name

    def add_new_column(self, col_name, dtype):  # do uzupełnienia

        col_content = self.col_default_content_dict[dtype]
        print("z diktu", col_content)
        print(dtype)

        loc = len(self.datafr.columns)
        try:
            self.datafr.insert(loc=loc, column=col_name, value=col_content)
            self.datafr_descr.insert(loc=loc, column=col_name, value=[dtype, "", "", ""])
            print(self.datafr_descr)
        except ValueError:
            print("Terefere nie da sie")

        return self.datafr

    def delete_column(self, column):
        self.datafr_descr.drop(columns=column, inplace=True)
        return self.datafr.drop(columns=column, inplace=True)

    def edit_column_title(self, old_column_name, new_column_name):
        return self.datafr.rename(columns={old_column_name: new_column_name}, inplace=True)

    def move_columns(self, column, direction):
        index_no = self.datafr.columns.get_loc(column)  # column index
        print(index_no)
        dfpoped = self.datafr.pop(column)
        dfdpoped = self.datafr_descr.pop(column)
        index_no += direction
        if index_no < 0:
            index_no = 0
        elif index_no > len(self.datafr.columns):
            index_no -= 1

        self.datafr_descr.insert(loc=index_no, column=dfdpoped.name, value=dfdpoped.values)
        print("DataFrameDescr")
        print(self.datafr_descr)
        return self.datafr.insert(loc=index_no, column=dfpoped.name, value=dfpoped.values)

    def add_row(self):
        print(list(self.datafr.columns))
        to_append = []
        print(self.datafr_descr.loc[1])
        for i in self.datafr_descr.loc[0]:
            to_append.append(self.col_default_content_dict[i])
        df_to_append = pd.DataFrame([to_append], columns=list(self.datafr.columns))
        print(to_append)
        print(df_to_append)
        self.datafr = self.datafr.append(df_to_append, ignore_index=True)
        return self.datafr

    def edit_cell_value(self, col, ind, new_val):
        self.datafr.loc[ind, col] = new_val
        return self.datafr

    def rename_priority_type(self, old_key, new_key):
        self.priority_types[new_key] = self.priority_types.pop(old_key)
        return self.priority_types

    def newcolor_priority_types(self, key, newcolor):
        self.priority_types[key] = newcolor

    def rename_status_type(self, old_key, new_key):
        self.status_types[new_key] = self.status_types.pop(old_key)
        return self.status_types

    def newcolor_status_types(self, key, newcolor):
        self.status_types[key] = newcolor
        pass
