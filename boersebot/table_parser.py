from boersebot import pdf_reader
from collections import defaultdict
import re
import pandas as pd


def parse_figures(input_string):
    """
    Parses the relevant figures from an input string representing a earnings release table.
    :param input_string: A string that resembles a table.
    :return: A dictionary that contains keys: 'revenue', 'profit', 'pretax_profit', 'profit_per_share', 'units'
    and 'timeframe'. Most values are lists in the format: [Name of figure, figure1, figure2, etc].
    Units and timeframe only contains a list with a single value.
    """
    figs = dict.fromkeys(['revenue', 'profit', 'pretax_profit', 'profit_per_share', 'units', 'timeframe'])
    synonyms = {'liikevaihto': 'revenue',
                'liiketulos': 'profit',
                'liikevoitto': 'profit',
                'liiketappio': 'profit',
                'tappio': 'profit',
                'voitto': 'profit',
                'tulos ennen veroja': 'pretax_profit',
                'voitto ennen veroja': 'pretax_profit',
                'tappio ennen veroja': 'pretax_profit',
                'osakekohtainen tulos': 'profit_per_share',
                'tulos/osake, euroa': 'profit_per_share'
                }

    return figs


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

    for j, line in enumerate(lines):
        # Recognise table lines by matching the with pattern
        ind = re.match(title_pattern, line)
        if ind:
            if table_start is None:
                table_start = j
            key = ind.group(1)
            # Find the digits on the line
            for i in re.finditer(r"([\-\d][\d,]+)", line):
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
    # TODO need to look up the column headers. Use column indexes to peek above the current table. Add functionality
    # to get the first table row index
    rows = []
    row_dict, table_start = lines_to_index_rows(input_string)
    column_idx = fetch_column_idx(row_dict)
    column_names = fetch_column_names(input_string, column_idx, table_start)

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
    print(column_names)
    return pd.DataFrame(rows, columns=column_names).set_index('tunnus')


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
    sample = pdf_reader.pdf_page_to_string('samples/2.pdf', 23)

    print(rebuild_table(sample))

