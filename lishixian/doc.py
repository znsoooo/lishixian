import os
import csv

import docx
import xlrd
import xlwt
from xlutils.filter import process, XLRDReader, XLWTWriter
from win32com import client


# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------


def WriteTxt(data, file, encoding='utf-8-sig'):
    with open(file, 'w', encoding=encoding) as f:
        f.write('\n'.join(','.join(str(cell) for cell in row) for row in data))


def OpenCsv(file, encoding='utf-8-sig'):
    with open(file, encoding=encoding) as f:
        return list(csv.reader(f))


def WriteCsv(data, file, errors='ignore', encoding='utf-8-sig'):
    with open(file, 'w', newline='', encoding=encoding, errors=errors) as f:
        writer = csv.writer(f)
        writer.writerows(data)


# ---------------------------------------------------------------------------
# Excel
# ---------------------------------------------------------------------------


def OpenExcel(file):
    rb = xlrd.open_workbook(file, formatting_info=True)

    # 参考xlutils.copy库内的用法 参考xlutils.filter内的参数定义style_list
    w = XLWTWriter()
    process(XLRDReader(rb, 'unknown.xls'), w)
    wb = w.output[0][1]
    style_list = w.style_list

    return wb, style_list

    # for n, sheet in enumerate(rb.sheets()):
    #     sheet2 = wb.get_sheet(n)
    #     for r in range(sheet.nrows):
    #         for c, cell in enumerate(sheet.row_values(r)):
    #             style = style_list[sheet.cell_xf_index(r, c)]
    #             sheet2.write(r, c, sheet.cell_xf_index(r, c), style)
    #
    # wb.save('save.xls')


def MergeCell(data, merge):
    data2 = []
    for sheet_data, sheet_merge in zip(data, merge):
        # only merge vertical
        for r1, r2, c1, c2 in sheet_merge:
            for r in range(r1, r2):
                sheet_data[r][c1] = sheet_data[r1][c1]
                for c in range(c1 + 1, c2):
                    sheet_data[r][c] = None
        # remove merge horizontal
        sheet_data2 = [[cell for cell in row if cell is not None] for row in sheet_data]
        # remove blanks in tail
        for row in sheet_data2:
            while len(row) and row[-1] == '':  # Good!
                row.pop()
        data2.append(sheet_data2)

    return data2


def ReadExcel(file, merge_x=False, merge_y=False):
    try:
        xls = xlrd.open_workbook(file, formatting_info=True)
    except:
        xls = xlrd.open_workbook(file)

    data = []
    for sheet in xls.sheets():
        sheet_name = sheet.name
        sheet_data = []
        for row in range(sheet.nrows):
            rows = [sheet_name] + sheet.row_values(row)
            for c, cell in enumerate(rows):
                if isinstance(cell, float):
                    if cell.is_integer():
                        rows[c] = str(int(cell))
                    else:
                        rows[c] = str(cell)
            sheet_data.append(rows)
        data.append(sheet_data)

    # only ".xls" type contain merge_info
    merge = [sheet.merged_cells for sheet in xls.sheets()]

    return data, merge


def ReadExcels(files):
    data = []
    success = []
    for file in files:
        path, filename = os.path.split(file)
        data += [[path, filename] + row for row in ReadExcel(file)]
        success.append(file)
    return data


def WriteExcel(data, file, new_sheet='sheet1'):
    xls = xlwt.Workbook('u8')
    sheet = xls.add_sheet(new_sheet, True)
    for r, row in enumerate(data):
        for c, cell in enumerate(row):
            sheet.write(r, c, cell)
    xls.save(file)


def Excel2Csv(file):
    root, ext = os.path.splitext(file)
    if ext == '.xlsx':
        file2 = root + '.xls'  # only ".xls" type contain merge_info
        ...
        file = file2
    data = MergeCell(*ReadExcel(file))
    WriteTxt(data, root + '.csv')
    return data


# ---------------------------------------------------------------------------
# Word
# ---------------------------------------------------------------------------


def Doc2Docx(file, overwrite=False):
    root, ext = os.path.splitext(file)
    file2 = root + '.docx.temp'
    if overwrite or not os.path.exists(file2):
        word = client.Dispatch('Word.Application')
        doc = word.Documents.Open(file)
        doc.SaveAs(file2, 16)
        doc.Close()
    return file2


def ReadWordTexts(file):
    if file.endswith('.doc'):
        file = Doc2Docx(file)

    doc = docx.Document(file)
    return [p.text for p in doc.paragraphs]


def ReadWord(file):
    doc = docx.Document(file)
    data = []
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_cells = row.cells
            # unique list
            # row_cells_nui = sorted(list(set(row_cells)), key=row_cells.index) # Good!
            row_cells = [item.text for i, item in enumerate(row_cells) if row_cells.index(item) == i]  # Slower but Good!
            table_data.append(row_cells)
        data.append(table_data)
    return data


def ReadWord(file):
    if file.endswith('.doc'):
        file = Doc2Docx(file)

    doc = docx.Document(file)
    data = []
    for table in doc.tables:
        sheet_data = []
        for r, row in enumerate(table.rows):
            # sheet_data.append([cell.text for cell in row.cells])
            row_cells = row.cells
            index = Unique(row_cells)  # 去重
            sheet_data.append([row_cells[id].text for id in index])
        data.append(sheet_data)
    return data


def OpenDocx(file):
    doc = docx.Document(file)
    data = []
    for table in doc.tables:
        for row in table.rows:
            data.append([cell.text for cell in row.cells])
    return data


def OpenDocx(file): # todo ?这是在干嘛？
    doc = docx.Document(file)
    data = []
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            table_data.append([cell.text for cell in row.cells])
        data.append(table_data)

        for r, row in enumerate(table.rows):
            for c, cell in enumerate(row.cells):
                cell.text = '%d,%d' % (r, c)

    return data


def Word2Csv(file):
    root, ext = os.path.splitext(file)
    if file.endswith('.doc'):
        file = Doc2Docx(file)
    data = ReadWord(file)
    WriteTxt(data, root + '.csv')
    return data


def Unique(arr):
    return [i for i, item in enumerate(arr) if arr.index(item) == i] # todo 再次仔细检查一下
    arr2 = []
    index = []
    for i, one in enumerate(arr):
        if one not in arr2:
            arr2.append(one)
            index.append(i)
    return index


# for test
# print(ReadWord('../test_docx.docx'))
