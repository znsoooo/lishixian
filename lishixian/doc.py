import os
import csv

import docx
import xlrd
import xlwt
import xlutils.filter
# from xlutils.filter import process, XLRDReader, XLWTWriter
from win32com import client

__all__ = list(globals())

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
    w = xlutils.filter.XLWTWriter()
    xlutils.filter.process(xlutils.filter.XLRDReader(rb, 'unknown.xls'), w)
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


def MergeCell(data, merge, merge_x=True, merge_y=True, strip_x=False):
    data2 = []
    for sheet_data, sheet_merge in zip(data, merge):
        # merge cell
        for r1, r2, c1, c2 in sheet_merge:
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    if (not merge_x and c > c1) or (not merge_y and r > r1):
                        sheet_data[r][c] = None if strip_x else ''
                    else:
                        sheet_data[r][c] = sheet_data[r1][c1]
        # strip x
        if strip_x:
            sheet_data = [[cell for cell in row if cell is not None] for row in sheet_data]
        data2.append(sheet_data)
        # remove blanks in tail
        # for row in sheet_data:
        #     while len(row) and row[-1] == '':  # Good!
        #         row.pop()
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


def ReadWord(file, merge_x, merge_y, strip_x):
    if file.endswith('.doc'):
        file = Doc2Docx(file)

    data = []
    merge = []
    doc = docx.Document(file)
    for table in doc.tables:
        cells  = table._cells  # see usage at `docx.table.Table._cells`
        cols   = table._column_count
        length = len(cells)

        data.append([])
        for i, cell in enumerate(cells):
            r, c = divmod(i, cols)
            if c == 0:  # create new row
                data[-1].append([])
            data[-1][-1].append(cell.text)

        merge.append([])
        for i, cell in enumerate(cells):
            if cell in cells[:i]:  # only find first repeated cell
                continue
            for j in range(length - 1, 0, -1):  # find last repeated cell
                if cell is cells[j]:  # always can be found
                    break
            if i != j:  # first != last -> merged cells
                r1, c1 = divmod(i, cols)
                r2, c2 = divmod(j, cols)
                merge[-1].append((r1, r2, c1, c2))

    data2 = MergeCell(data, merge, merge_x, merge_y, strip_x)

    return data2


def OpenDocx(file):
    doc = docx.Document(file)
    data = []
    for table in doc.tables:
        for row in table.rows:
            data.append([cell.text for cell in row.cells])
    return data


def Word2Csv(file):
    root, ext = os.path.splitext(file)
    if file.endswith('.doc'):
        file = Doc2Docx(file)
    data = ReadWord(file)
    WriteTxt(data, root + '.csv')
    return data


def Unique(arr):
    return [i for i, item in enumerate(arr) if arr.index(item) == i]


__all__ = [k for k in globals() if k not in __all__]


if __name__ == '__main__':
    from pprint import pprint

    # data, merge = ReadExcel('../test.xls')
    # pprint(merge)
    # pprint(data)

    pprint(ReadWord('../test.docx', 0, 0, 0))
    pprint(ReadWord('../test.docx', 0, 1, 0))
    pprint(ReadWord('../test.docx', 1, 0, 0))
    pprint(ReadWord('../test.docx', 1, 1, 0))

    # for table in data:
    #     for row in table:
    #         row.pop(0)
    # data2 = MergeCell(data, merge)
    # pprint(data2)
