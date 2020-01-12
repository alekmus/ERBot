from boersebot import pdf_reader
from collections import defaultdict
import json
import re
import datetime
import pandas as pd


def lines_to_index_rows(input_string):
    """
    Creates a sparse matrix that has name of each figure as well as the index for start and end of each value cell.
    :param input_string: A String of a table to be converted.
    :return: A dictionary in the format key: (start_index, end_index, value).
    """
    # Matches a string that starts with words followed by at least two spaces.
    title_pattern = r"^((?:\S\s?)+)(?:  )+"
    lines = input_string.split('\n')
    rows = defaultdict(list)

    # Line for first tablelike match
    table_start = None

    # Get index_map for generalizing names of rows
    with open("assets/generalized_index_map.json") as f:
        index_map = json.load(f)

    for j, line in enumerate(lines):
        # Recognise table lines by matching the with pattern
        ind = re.match(title_pattern, line)
        if ind:
            if table_start is None:
                table_start = j
            key = generalize_index(ind.group(1).lower().strip(), index_map)
            # Find the digits on the line
            for i in re.finditer(r"([\-\d\(][\d,]+)", line):
                rows[key].append((i.start(),
                                  i.end(),
                                  i.group().strip()))
    return rows, table_start


def rebuild_table(input_string):
    """
    Rebuilds the string data to a pandas DataFrame
    :param input_string: String of representation of a table
    :return: Pandas DataFrame containing the data from the string.
    """
    rows = []
    row_dict, table_start = lines_to_index_rows(input_string)
    column_idx = fetch_column_idx(row_dict)
    column_names = fetch_column_names(input_string, column_idx, table_start)
    column_names = generalize_column_names(column_names)
    for key in row_dict:
        row = [key]
        digits = iter(row_dict[key])
        digit = next(digits)

        for c in column_idx:
            if digit:
                if digit[0] >= c[0] and digit[1] <= c[1]:
                    row.append(digit[2])
                    digit = next(digits, False)
                else:
                    row.append(None)
            else:
                row.append(None)
        rows.append(row)
    mag_unit = fetch_units(input_string, table_start)
    return pd.DataFrame(rows, columns=column_names).set_index('tunnus'), mag_unit


def fetch_units(input_string, table_start):
    """
    Parses the monetary units from the input string
    :param input_string: A String representing a table
    :param table_start: Integer, line number for first table row.
    :return: A tuple in the form (magnitude, currency) i.e (1000, EUR)
    """
    lines = input_string.lower().split('\n')
    pattern = r"((?:[\d ,])*) ?([m ]?)(?P<tunnus>eur|sek)\s|\s(?P<jtunnus>me)\s"
    for i, line in enumerate(lines):
        if i >= table_start:
            return 1, 'EUR'
        else:
            ind = re.search(pattern, line)
            if ind:
                if ind.group('tunnus'):
                    if ind.group(2) == 'm':
                        return int(1e6), ind.group('tunnus')
                    elif ind.group(1):
                        mag = ind.group(1)
                        return int(re.sub(r'[^\d]', '', mag)), ind.group('tunnus')
                    else:
                        return 1, ind.group('tunnus')
                elif ind.group('jtunnus'):
                    return int(1e6), 'EUR'
    else:
        return 1, 'EUR'


def fetch_column_names(input_string, column_index, table_start):
    """
    Tries to parse column names for given columns. Function gives placeholder names for columns that can be parsed to
    generic names.
    :param input_string: String representation of table.
    :param column_index: List of column indexes
    :param table_start: Line where the table starts.
    :return:
    """
    col_names = [""]*len(column_index)

    for i, line in enumerate(input_string.split('\n')):
        prev = 0
        if i >= table_start:
            break
        else:
            for j, c in enumerate(column_index):
                col_names[j] = " ".join([col_names[j], line[prev:c[1]+1].strip()])
                prev = c[1] + 1
    # Set the index name to 'tunnus'
    col_names.insert(0, 'tunnus')
    return col_names


def generalize_column_names(column_names):
    """
    Replaces parsed column names with generalized versions so they can be looked up later
    :param column_names: List of parsed column names.
    :return: List of generalized column names in the
    set {q1,q2,q3,q4}.
    """
    # TODO add h1, h2 and full year earnings.
    gen_names = []
    last_year = str(datetime.date.today().year-1)
    # Loads json file containing regex patterns for each generalized name
    with open("assets/generalized_column_map.json") as f:
        name_map = json.load(f)
    for name in column_names:
        for key in name_map:
            if re.search(name_map[key], name):
                if last_year in name or last_year[-2:] in name:
                    gen_names.append('prev_' + key)
                else:
                    gen_names.append(key)
                break
        else:
            gen_names.append(name)

    return gen_names


def generalize_index(name, index_map):
    """
    Generalizes name of  the figure so it can be effectively used as an index in the DataFrame. Takes only into account
    names we are interested in as specified in the generalized_index_map asset file.
    :param name: Parsed name for figure.
    :param index_map: Map from different parsed values to generalized ones.
    :return: List of generalized names of the same length.
    """
    if name in index_map:
        return index_map[name]
    else:
        return name


def fetch_column_idx(row_dict):
    """
    Helper function for rebuild_table that recreates the column indices based on indices for values.
    Input can be created by lines_to_index_rows function.
    :param row_dict: A dictionary of start and end indices of table values.
    :return: A list of indices that form columns in a table.
    """
    start_idx = defaultdict(list)
    end_idx = defaultdict(list)

    for key, values in row_dict.items():
        for i, value in enumerate(values):
            start_idx[i].append(value[0])
            end_idx[i].append(value[1])

    column_idx = []

    # Iterate over list of keys instead of dictionary for keeping order. Both idx dictionaries can be assumed to have
    # the same number of indices.
    for i in sorted(start_idx.keys()):
        column_idx.append((min(start_idx[i]), min(end_idx[i])))

    return column_idx


if __name__ == '__main__':
    sample = pdf_reader.pdf_page_to_string('samples/12.pdf', 5)
    print(rebuild_table(sample))
