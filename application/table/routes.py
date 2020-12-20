from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import current_user, login_required
import pandas as pd
import sys
path = sys.path[0]  # current path
import os
from application.table.functions import sort_ascending_switch
from application.table.tables import Table, TablesDict


#  initialling a default table
# dodac - if there is no user (or new user)
global table, TablesDict
# set default tableDictionary
TablesDict = {"New Table": Table("New Table")}
# getting defaulf table from default table dict
table = TablesDict.get("New Table")
print('table name',table.name)
print(table.datafr)

# t = table.datafr
# conn = sql.connect(path+'\\database\\tabledatabase.db')
# t.to_sql('tabledatabase', conn, if_exists='replace')


table_bp = Blueprint(
    'table_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

sort_asc = True
sorted_trigger = ""


@table_bp.route("/")
@table_bp.route("/home")
def home():
    return render_template("home.html", tabledict=TablesDict.keys())


@table_bp.route("/table_view/<tablename>")
# @login_required
def table_view(tablename=table.name, row_sel=False):
    print(tablename)
    global table
    table = TablesDict.get(tablename)
    # table.datafr.to_sql('tabledatabase1', conn, if_exists='replace')
    return render_template('table_view.html',
                           tabledict=TablesDict.keys(),
                           tablename=table.name,
                           index=table.datafr.index.values, datafr=table.datafr,
                           column_type=table.datafr_descr.loc[0],
                           column_descr=table.datafr_descr.loc[1],
                           status_types=table.status_types,
                           priority_types=table.priority_types,
                           row_sel=row_sel,
                           tableDesc=table.tableDescr)


@table_bp.route("/table_select", methods=['GET', 'POST'])
def table_select():
    if request.method == 'POST':
        table_request = request.form['tablename']
        return table_view(tablename=table_request)


@table_bp.route("/import_table", methods=['GET', 'POST'])
def import_table():
    global datafr, table
    if request.method == 'POST':
        print(request.files['file'])
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('import.html')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('import.html')
        else:
            filename = file.filename
            url = "C:\\PythonScripts\\data\\"
            # url = 'D:\\Projects\\Python\\CPDZTM\\csv_in_flask\\'
            ext = os.path.splitext(filename)[1]
            if ext == ".csv":
                datafr = pd.read_csv(url + filename, encoding='latin')
                TablesDict[filename] = Table(filename)
                TablesDict[filename].datafr = datafr
            elif ext == ".xls":
                datafr = pd.read_excel(url + filename)
            table = TablesDict.get(filename)
            return table_view(tablename=table.name)
            print(file.filename)
    return render_template('import.html')
    # if request.method == 'POST':
    #     print(request.form)
    #     if request.form.get('filename'):
    #         print("sraaaaaaaaaaaa")
    #         if request.form['filename']:
    #             url = 'D:\\Projects\\Python\\CPDZTM\\csv_in_flask\\'
    #             file = request.form['filename']
    #             print("file", file)
    #             ext = os.path.splitext(file)[1]
    #             if ext == ".csv":
    #                 datafr = pd.read_csv(url+file)
    #                 TablesDict[file] = Table(file)
    #                 TablesDict[file].datafr = datafr
    #             elif ext == ".xls":
    #                 datafr = pd.read_excel(url+file)
    #             table = TablesDict.get(file)
    #             return table_view(tablename=table.name)
    #     else:
    #         return redirect(url_for('home'))
    # else:
    #     return render_template("import.html")

    # if request.method == 'POST':
    #     # check if the post request has the file part
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         return redirect('import.html')
    #     file = request.files['file']
    #     # if user does not select file, browser also
    #     # submit an empty part without filename
    #     if file.filename == '':
    #         flash('No selected file')
    #         return redirect('import.html')
    #     else:
    #         print(file.filename)

    #     if name in TablesDict.keys():
    #         print("taka nazwa juz jest")
    #     else:
    #         TablesDict[name] = Table(name)
    #         print("created new table")
    #         print("Keys ", TablesDict.keys())
    #         print(TablesDict.get(name))
    #         table = TablesDict.get(name)
    #         print(table.name)
    #         print(table.datafr)
    # return table_view(tablename=table.name)


@table_bp.route('/export_table', methods=['GET', 'POST'])
def export_table():
    print(TablesDict.keys())
    if request.method == 'POST':
        print(request.form['to_export'])
        name = request.form['to_export']
        table_to_export = TablesDict[name].datafr
        csv = table_to_export.to_csv()
        return Response(
            csv,
            mimetype="text/csv",
            headers={"Content-disposition": f"attachment; filename={name}.csv"})
    return render_template('export.html', tables=TablesDict.keys())


@table_bp.route("/sort_data", methods=['GET', 'POST'])
def sort_data():
    global datafr, sort_asc, sorted_trigger

    if request.method == 'POST':
        print("Req form", request.form)
        sort_request = request.form['sort']
        print('typu', type(sort_request))
        print("Sort_req: ", sort_request)

        if sorted_trigger == sort_request:
            sort_asc = sort_ascending_switch(sort_asc)
            print("triggered", sort_asc)
        else:
            sort_asc = True

        if sort_request == 'index':
            table.datafr = table.datafr.sort_index(ascending=sort_asc)
            sorted_trigger = sort_request

        else:
            print("rump")
            print(table.datafr[sort_request])
            print(type(table.datafr[sort_request]))
            table.datafr = table.datafr.sort_values(by=[sort_request], ascending=sort_asc)
            print('Posortowalo')
            sorted_trigger = sort_request
        return table_view(tablename=table.name)


@table_bp.route("/add_column", methods=['GET', 'POST'])
def add_column():
    if request.method == 'POST':
        col_name = request.form['col_name']
        dtype = request.form['dtype']
        print(col_name, dtype)
        table.add_new_column(col_name, dtype)
        return table_view()
    return table_view()
    # return render_template('/edit/addcolumn.html', form=form)


@table_bp.route('/del_column', methods=['GET', 'POST'])
def del_column():
    if request.method == 'POST':
        print(request.form)
        column = request.form['delete']
        print(column)
        table.delete_column(column)
        return table_view(tablename=table.name)
    #
    # return render_template('/edit/del_column.html', form=form)


@table_bp.route('/add_row', methods=['GET', 'POST'])
def add_row():
    global datafr
    if request.method == 'POST':
        table.add_row()
    return table_view(tablename=table.name)


@table_bp.route('/del_row', methods=['GET', 'POST'])
def del_row():
    if request.method == 'POST':
        rows = request.form.to_dict()
        # przerabiam na listę integerow
        rows_list = []
        for val in rows.values():
            rows_list.append(int(val))

        print(rows_list)
        table.datafr.drop(labels=rows_list, axis=0, inplace=True)
        return table_view()

    return table_view(tablename=table.name, row_sel=True)


@table_bp.route('/edit_col_title', methods=['GET', 'POST'])
def edit_col_title():
    if request.method == 'POST':
        print(request.form)
        new_column_name = request.form['new_name']
        old_column_name = request.form['old_name']
        print(new_column_name, old_column_name)
        table.datafr.rename(columns={old_column_name: new_column_name}, inplace=True)
        table.datafr_descr.rename(columns={old_column_name: new_column_name}, inplace=True)
    return table_view(tablename=table.name)


@table_bp.route('/add_description', methods=['GET', 'POST'])
def add_description():
    if request.method == 'POST':
        print(request.form)
        col = request.form['column']
        desc = request.form['description']
        table.datafr_descr.loc[1, col] = desc
        print(table.datafr_descr.loc[1][col])
    return table_view(tablename=table.name)


@table_bp.route('/move_column', methods=['GET', 'POST'])
def move_column():
    if request.method == 'POST':
        move_atr = request.form['move']
        direction = int(move_atr.split(",")[0])
        print(direction)
        col_name = str(move_atr.split(",")[1])
        print(col_name)
        table.move_columns(col_name, direction)
    return table_view(tablename=table.name)


@table_bp.route('/edit_cell', methods=['GET', 'POST'])
def edit_cell():
    if request.method == 'POST':
        print("def edit_cell")
        col = request.form['col']
        indx = int(request.form['indx'])
        try:
            new_value = request.form['new_value']
        except KeyError:
            new_value = float(request.form['new_number'])
        except ValueError:
            flash(f'Value must be a Number!', category="warning")
            new_value = None

        print(col, indx, new_value)
        if new_value:
            table.datafr.loc[indx, col] = new_value
    return table_view(tablename=table.name)


@table_bp.route('/edit_status_cell', methods=['GET', 'POST'])
def edit_status_cell():
    if request.method == 'POST':
        print("LOHO")
        new_status = request.form['new_value']
        col = request.form['col']
        indx = int(request.form['indx'])
        print(col, indx, new_status)
        table.datafr.loc[indx, col] = new_status
    return table_view(tablename=table.name)


@table_bp.route('/rename_table', methods=['GET', 'POST'])
def rename_table():
    if request.method == 'POST':
        old_name = request.form['old_name']
        new_name = request.form['new_name']
        TablesDict[new_name] = TablesDict.pop(old_name)
        table.name = new_name
    return table_view(tablename=table.name)


@table_bp.route('/new_table', methods=['GET', 'POST'])
def new_table():
    global table
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        if name in TablesDict.keys():
            print("taka nazwa juz jest")
        else:
            TablesDict[name] = Table(name)
            print("created new table")
            print("Keys ", TablesDict.keys())
            print(TablesDict.get(name))
            table = TablesDict.get(name)
            print(table.name)
            print(table.datafr)
    return table_view(tablename=table.name)


@table_bp.route('/delete_table', methods=['GET', 'POST'])
def delete_table():
    pass


@table_bp.route('/select_table', methods=['GET', 'POST'])
def select_table():
    global table
    if request.method == 'POST':
        print('BRUM')
        name = request.form['select_table']
        print(name)
        table = TablesDict.get(name)
        print(table.name)
        print(table.datafr)
    return table_view(tablename=table.name)


if __name__ == '__main__':
    table_bp.run(debug=True)
