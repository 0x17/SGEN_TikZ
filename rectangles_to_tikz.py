import os
import numpy as np


def draw_rect(upper_left, bottom_right, label=None, options=None):
    text = '{' + label + '}' if label is not None else ''
    s_uppper_left = f'({upper_left[0]},{upper_left[1]})'
    s_bottom_right = f'({bottom_right[0]},{bottom_right[1]})'
    opts_str = '[' + ','.join(f'{opt_name}={opt_val}' for opt_name, opt_val in options.items()) + ']' if options is not None else ''
    return '\draw ' + opts_str + ' ' + s_uppper_left + ' rectangle ' + s_bottom_right + (f' node[pos=.5] {text};' if label is not None else '')


def rect_to_tikz(j, rect, origin_x=0.0, origin_y=0.0, scale=2.0):
    ul = (rect.x * scale + origin_x, rect.y * scale + origin_y)
    br = ((rect.x + rect.w) * scale + origin_x, (rect.y + rect.h) * scale + origin_y)
    options = {'draw': 'black', 'fill': 'lightgray'}
    return draw_rect(ul, br, str(j), options)


def rects_to_tikz(rects, origin_x=0.0, origin_y=0.0, scale=2.0):
    return '\n'.join([rect_to_tikz(ix, rect, origin_x, origin_y, scale) for ix, rect in enumerate(rects) if rect.w > 0 and rect.h > 0])


TIKZ_PREFIX = '\n\\begin{tikzpicture}\n'  # [font=\sffamily\small]\n'
TIKZ_SUFFIX = '\n\\end{tikzpicture}\n'
TEX_PREFIX = """
\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage{tikz}
\\begin{document}
"""
TEX_SUFFIX = '\n\\end{document}'


def axis_for_rects(proj_obj, rects, origin_x=0.0, origin_y=0.0, scale=2.0, res_name='$r$', res_ix=0):
    xmax = max([rect.x + rect.w for rect in rects]) + 1
    ymax = max([rect.y + rect.h for rect in rects]) + 1
    ymax_regular = proj_obj['capacities'][res_ix]
    ymax_with_oc = ymax_regular + proj_obj['zmax'][res_ix]
    ostr = f'\draw[->,thick] ({origin_x},{origin_y})--({origin_x + xmax * scale},{origin_y}) ' + 'node[right]{$t$};\n'
    ostr += f'\draw[->,thick] ({origin_x},{origin_y})--({origin_x},{origin_y + (ymax_with_oc + 1) * scale}) ' + 'node[above]{' + res_name + '};\n'
    ctr = 1
    bbox_opts = {'fill': 'none', 'draw': 'none'}
    for x in np.arange(origin_x, origin_x + xmax * scale, scale):
        bar_top = (x, origin_y)
        bar_bottom = (x, origin_y - scale)
        ostr += f'\draw[-,thick] ({bar_top[0]},{bar_top[1]})--({bar_bottom[0]},{bar_bottom[1]});\n'
        if x + scale < xmax:
            ostr += draw_rect(bar_top, (x + scale, origin_y - scale), str(ctr), bbox_opts)
        ctr += 1
    ctr = 1
    for y in np.arange(origin_y, origin_y + (ymax_with_oc + 1) * scale, scale):
        bar_right = (origin_x, y)
        bar_left = (origin_x - scale * 0.5, y)
        ostr += f'\draw[-,thick] ({bar_right[0]},{bar_right[1]})--({bar_left[0]},{bar_left[1]});\n'
        ostr += draw_rect((bar_left[0] - scale * 0.5, bar_left[1] - scale * 0.5), (bar_left[0], bar_left[1] + scale * 0.5), str(ctr), bbox_opts)
        ctr += 1
    ostr += f'\draw[-,thick,color=red,dotted] ({origin_x},{origin_y + ymax_regular * scale})--({xmax - scale},{origin_y + ymax_regular * scale});\n'
    ostr += f'\draw[-,thick,color=red,dotted] ({origin_x},{origin_y + ymax_with_oc * scale})--({xmax - scale},{origin_y + ymax_with_oc * scale});\n'
    return ostr


def try_del(fns):
    for fn in fns:
        if os.path.exists(fn): os.remove(fn)


def cleanup_tempfiles(tex_filename):
    base_fn = tex_filename.replace('.tex', '')
    del_extensions = ['log', 'aux', 'tex']
    try_del([base_fn + '.' + dext for dext in del_extensions])


def rects_to_pdf(proj_obj, rects, out_filename, res_name='$r$', res_ix=0):
    tex_filename = out_filename.replace('.pdf', '.tex')
    try_del([out_filename, tex_filename])
    with open(tex_filename, 'w') as fp:
        fp.write(TEX_PREFIX + rects_to_tikz_picture(proj_obj, rects, res_name, res_ix) + TEX_SUFFIX)
    os.system('pdflatex ' + tex_filename)
    cleanup_tempfiles(tex_filename)


def rects_to_tikz_picture(proj_obj, rects, res_name='$r$', res_ix=0):
    return TIKZ_PREFIX + rects_to_tikz(rects, scale=1.0) + axis_for_rects(proj_obj, rects, scale=1.0, res_name=res_name, res_ix=res_ix) + TIKZ_SUFFIX


def tikz_pics_to_pdf(tikz_pics, out_fn_base):
    tex_filename = out_fn_base + '.tex'
    try_del([out_fn_base + '.pdf', tex_filename])
    with open(tex_filename, 'w') as fp:
        fp.write(TEX_PREFIX + '\n\\pagebreak\n'.join(tikz_pics) + TEX_SUFFIX)
    os.system('pdflatex ' + tex_filename)
    cleanup_tempfiles(tex_filename)
