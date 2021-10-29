import os
import csv

import docx
import xlrd
import xlwt
import xlutils


def ReadWordText(file):
    pass


def ReadWordTables(file):
    pass


def CopyExcel(file):
    pass # TODO


def ReadExcel(file):
    xls = xlrd.open_workbook(file)
    data = []
    for sheet in xls.sheets():
        sheet_name = sheet.name
        for row in range(sheet.nrows):
            rows = [sheet_name] + sheet.row_values(row)
            for c, cell in enumerate(rows):
                if isinstance(cell, float):
                    if cell.is_integer():
                        rows[c] = str(int(cell))
                    else:
                        rows[c] = str(cell)
            data.append(rows)
    return data


def ReadExcels(files):
    data = []
    success = []
    for file in files:
        path, filename = os.path.split(file)
        data += [[path, filename] + row for row in ReadExcel(file)]
        success.append(file)
    return data


def WriteXls(data, file):
    xls = xlwt.Workbook('u8')
    sheet = xls.add_sheet('sheet1', True)
    for r, row in enumerate(data):
        for c, cell in enumerate(row):
            sheet.write(r, c, cell)
    xls.save(file)


def OpenCsv(file):
    with open(file) as f:
        return list(csv.reader(f))


def WriteCsv(data, file):
    with open(file, 'w', newline='', errors='ignore') as f: # TODO Error的处理方式?
        writer = csv.writer(f)
        writer.writerows(data)


def input_wait(msg):
    while input(msg + '[y/n]: ').lower() != 'y':
        pass


input_default = lambda msg, default: input('input <%s>, keep <%s> press enter: ' % (msg, default)) or default



