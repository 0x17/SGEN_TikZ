import itertools
from rect import Rect


def rect_for_job(data, y_pos, j):
    x = data['starting_times'][j]
    y = y_pos
    w = data['durations'][j]
    h = data['demands'][j]
    return Rect(x, y, w, h)


def rects_for_jobs(data, y_positions):
    return [rect_for_job(data, y_positions[j], j) for j in range(data['njobs'])]


def num_overlaps(data, y_positions):
    rects = rects_for_jobs(data, y_positions)
    ctr = 0
    for i, ra in enumerate(rects):
        for j, rb in enumerate(rects):
            if i < j and ra.overlaps(rb):
                ctr += 1
    return ctr


def possible_y_positions(data):
    return itertools.product(*[[y_pos for y_pos in range(data['capacity'] - data['demands'][j] + 1)] for j in range(data['njobs'])])


def num_zeroes(lst):
    return sum([1 if entry == 0 else 0 for entry in lst])


def y_positions_min_overlap(data, stop_on_feas=False, fixed_positions=None):
    all_positions = possible_y_positions(data)
    best_count = data['njobs'] * data['njobs']
    best_candidate = None

    lpositions = list(all_positions)

    if fixed_positions is not None:
        lpositions = [pvec for pvec in lpositions if all(pvec[j] == fixed_pos for j, fixed_pos in fixed_positions.items())]

    tcount = len(lpositions)
    ctr = 0

    for candidate in lpositions:
        candidate_overlap_count = num_overlaps(data, candidate)
        if candidate_overlap_count < best_count:
            best_count = candidate_overlap_count
            best_candidate = candidate
            if best_count == 0 and stop_on_feas:
                return best_candidate
        elif candidate_overlap_count == best_count and num_zeroes(candidate) > num_zeroes(best_candidate):
            best_candidate = candidate
        print(f'\rProgress: {ctr / tcount * 100.0}, Best count: {best_count}', end='')
        ctr += 1

    return best_candidate
