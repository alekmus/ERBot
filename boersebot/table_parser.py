from boersebot import pdf_reader
import string
import re


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

    for line in input_string.split('\n'):
        pattern = r"^((?:\S+\s?)+)(.*)"
        ind = re.match(pattern, line.lower())

        if ind:
            key = ind.group(1).strip()
            print(key)
            if key in synonyms:
                fig_key = synonyms[key]
                figs[fig_key] = ind.group(2).split()
    return figs


def check_line_for_units(line):
    pass


if __name__ == '__main__':
    sample = pdf_reader.pdf_page_to_string('samples/2.pdf', 23)
    print(parse_figures(sample))
    print(sample)
