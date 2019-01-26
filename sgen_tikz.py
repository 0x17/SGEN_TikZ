import sys
from psplibconverter import sm_to_object

from rectangles_to_tikz import rects_to_tikz_picture, tikz_pics_to_pdf
from schedule_to_rectangles import y_positions_min_overlap, rects_for_jobs


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
        'capacity': proj_obj['capacities'][res_ix],
        'zmax': proj_obj['zmax'][res_ix],
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

    tikz_pics = [ rects_to_tikz_picture(proj_obj, draw_schedule_rects_for_res(proj_obj, sts, res_ix), res_name=f'$r{res_ix + 1}$', res_ix=res_ix) for res_ix in range(proj_obj['numresources']) ]
    tikz_pics_to_pdf(tikz_pics, out_fn_base)



if __name__ == '__main__':
    main(sys.argv)
