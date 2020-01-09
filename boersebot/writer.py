import json
import random


def write_paragraph(company, figure_name, figure, quarter, prev_figure, unit, corpus):
    """
    Writes a finnish paragraph for a single figure.
    :param company: String with the company's name.
    :param figure_name: String with name of the figure.
    :param figure: A figure from the earnings release.
    :param quarter: The quarter the figures are from.
    :param prev_figure: Figure from last year.
    :param unit: Units for the figures
    :param corpus: Corpus for building the sentences.
    :return: String containing a paragraph of text.
    """
    sentences = dict(corpus['core'])
    descriptors = dict(corpus['desc'])
    direction = pick_desc(figure, prev_figure)
    desc = descriptors[direction]
    return sentences['1'].format(company_name=company,
                                 figure=figure_name,
                                 amount = figure,
                                 time=quarter,
                                 desc=desc,
                                 unit=unit,
                                 prev_time="edellisvuonna",
                                 prev_figure=prev_figure)


def pick_desc(fig, prev_fig):
    if fig - prev_fig < 0:
        return "neg"
    else:
        return "pos"


if __name__ == '__main__':
    with open("assets/corpus.json") as f:
        corpus = json.load(f)

    print(write_paragraph('Valmetin', 'liikevaihto', 10000, "neljännellä neljänneksellä", 90000, "miljoonaa euroa",
                          corpus))
