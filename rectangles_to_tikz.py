import os


def rect_to_tikz(j, rect, origin_x=0.0, origin_y=0.0, scale=2.0):
    text = '{'+str(j)+'}'
    return f'\draw [draw=black,fill=lightgray] ({rect.x * scale + origin_x},{rect.y * scale + origin_y}) rectangle ({(rect.x+rect.w)*scale+origin_x},{(rect.y+rect.h)*scale+origin_y}) node[pos=.5] {text};'


def rects_to_tikz(rects, origin_x=0.0, origin_y=0.0, scale=2.0):
    return '\n'.join([rect_to_tikz(ix, rect, origin_x, origin_y, scale) for ix, rect in enumerate(rects) if rect.w > 0 and rect.h > 0])


TIKZ_PREFIX = '\n\\begin{tikzpicture}\n'
TIKZ_SUFFIX = '\n\\end{tikzpicture}\n'
TEX_PREFIX = """
\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage{tikz}
\\title{TikZ - Playground}
\\author{Andre Schnabel}
\\date{}
\\begin{document}
\\maketitle
"""
TEX_SUFFIX = '\n\\end{document}'


def try_del(fns):
    for fn in fns:
        if os.path.exists(fn): os.remove(fn)


def rects_to_pdf(rects, out_filename):
    tex_filename = out_filename.replace('.pdf', '.tex')
    try_del([out_filename, tex_filename])
    with open(tex_filename, 'w') as fp:
        fp.write(TEX_PREFIX + TIKZ_PREFIX + rects_to_tikz(rects, scale=1.0) + TIKZ_SUFFIX + TEX_SUFFIX)
    os.system('pdflatex ' + tex_filename)
