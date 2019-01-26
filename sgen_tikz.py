import sys
from psplibconverter import sm_to_object

from rectangles_to_tikz import rects_to_pdf
from schedule_to_rectangles import y_positions_min_overlap, rects_for_jobs

'''
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
'''


def parse_schedule(fn):
    with open(fn, 'r') as fp:
        parts = fp.readlines()[1].split(';')
        return [int(p) for p in parts[:-4]]


def draw_schedule_rects_for_res(proj_obj, sts, res_ix=0):
    schedule_data = {
        'njobs': proj_obj['numjobs'],
        # widths
        'durations': proj_obj['durations'],
        # heights
        'demands': proj_obj['demands'][res_ix],
        # total height
        'capacity': proj_obj['capacities'][res_ix] + int(proj_obj['zmax'][res_ix]) * 0,
        # x positions
        'starting_times': sts
    }

    y_positions = y_positions_min_overlap(schedule_data, stop_on_feas=True, fixed_positions={9: 0})
    return rects_for_jobs(schedule_data, y_positions)


def main(args):
    if len(args) != 3:
        print('Usage: python sgen_tikz.py project.sm schedule.txt')
        return

    proj_fn, sched_fn = args[1:3]
    out_fn_base = sched_fn.replace('.txt', '')

    proj_obj = sm_to_object(proj_fn)
    sts = parse_schedule(sched_fn)

    for res_ix in range(proj_obj['numresources']):
        rects = draw_schedule_rects_for_res(proj_obj, sts, res_ix)
        rects_to_pdf(rects, out_fn_base+f'_res{res_ix}.pdf')


if __name__ == '__main__':
    main(sys.argv)
