# ERBot

The initial purpose of this project was to parse certain infromation from
earnings releases and write journalistic text based on them.

The project utilizes a naive bayes model that uses the bag of words method
to determine if a given page contains the information we are interested in.
After the correct page is recognised string manipulation is used to extract
relevant fields and those are used as a basis for text creation.

The NB-classifier was able to reach a ~65-70% accuracy which, even though
wasn't enough for actual use without extensive human oversight, was promising
and could have been improved upon.
However a problem arised from using string manipulation to construct
tables as companies use extremely wide range of formats of tables to present
their earnings information. After a few examples it became clear that the chosen
methods were insufficient.

Next stage of development will be to focus on edge detection and other visual
methods but this branch has been effectively reduced to a coding sample.

The mentioned next stage has been explored more in the "Coding Samples" -repo where I've
uploaded a module that recognises the outlines and individual cells of a data table
using computer vision.
