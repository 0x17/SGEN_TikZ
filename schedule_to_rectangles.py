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
    return itertools.product(*[[y_pos for y_pos in range(data['capacity'] - data['demands'][j])] for j in range(data['njobs'])])


def num_zeroes(lst):
    return sum([1 if entry == 0 else 0 for entry in lst])


def y_positions_min_overlap(data):
    all_positions = possible_y_positions(data)
    best_count = data['njobs'] * data['njobs']
    best_candidate = None

    for candidate in all_positions:
        candidate_overlap_count = num_overlaps(data, candidate)
        if candidate_overlap_count < best_count:
            best_count = candidate_overlap_count
            best_candidate = candidate
        elif candidate_overlap_count == best_count and num_zeroes(candidate) > num_zeroes(best_candidate):
            best_candidate = candidate

    return best_candidate
