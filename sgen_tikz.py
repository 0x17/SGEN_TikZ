import sys

from rectangles_to_tikz import rects_to_pdf
from schedule_to_rectangles import y_positions_min_overlap, rects_for_jobs

example_input = {
    'njobs': 8,
    # widths
    'durations': [0, 3, 2, 2, 3, 1, 2, 0],
    # heights
    'demands': [0, 3, 2, 2, 1, 2, 1, 0],
    # total height
    'capacity': 4,
    # x positions
    'starting_times': [0, 0, 3, 3, 5, 5, 8, 10]
}

example_output = {
    # vertical position
    'y_positions': [0, 0, 0, 2, 0, 1, 0, 0]
}


def main(args):
    y_positions = y_positions_min_overlap(example_input)
    rects = rects_for_jobs(example_input, y_positions)
    rects_to_pdf(rects, 'myrectangles.pdf')


if __name__ == '__main__':
    main(sys.argv)
