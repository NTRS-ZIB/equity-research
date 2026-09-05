"""Generate the site icons from one set of coordinates.

WHY THE LETTERFORMS ARE PATHS AND NOT TEXT. A favicon SVG is rendered in
isolation by the browser and cannot load a webfont, so a <text> element would
fall back to whatever monospace the viewer happens to have installed, and the
vector and raster versions would then disagree. N and Z are both straight-line
forms, so drawing them as explicit polygons costs nothing and makes the mark
identical everywhere with no font dependency.

WHY THERE IS NO BRASS RULE AROUND THE EDGE, UNLIKE THE HEADER MARK. It was
drawn with one first. At 16px, which is where a favicon actually lives, a 1px
frame costs a pixel on every side and the two letters then blur into each
other. Rendered side by side at true size, the borderless form was the only one
in which NZ read unambiguously. The rule is what the icon gives up in order to
be legible at the size it is actually used.

WHY THIS FILE IS TRACKED. The mark is generated, not drawn by hand in an
editor. Without the generator the only way to change it would be to redraw it,
and the next person would be guessing at the geometry. scripts/ is excluded
from the deploy, so keeping it here costs the published set nothing.

Run: python scripts/make_icons.py
"""

from PIL import Image, ImageDraw

BRASS = (184, 149, 74, 255)
NAVY = (11, 28, 44, 255)

GRID = 64          # the coordinate system every shape below is expressed in
BORDER = 0         # see the note above; 0 means no rule is drawn at all
SS = 8             # supersample factor, downsampled with LANCZOS afterwards

# N occupies x 5..30, Z occupies x 34..59, both y 12..52, stroke 8. The pair is
# centred: 5 units of margin each side. Each diagonal is a parallelogram so that
# both renderers draw exactly the same edges rather than approximating a stroke.
N_LEFT = (5, 12, 13, 52)
N_RIGHT = (22, 12, 30, 52)
N_DIAG = [(13, 12), (13, 26), (22, 52), (22, 38)]

Z_TOP = (34, 12, 59, 20)
Z_BOTTOM = (34, 44, 59, 52)
Z_DIAG = [(46, 20), (59, 20), (47, 44), (34, 44)]


def render(size):
    """Draw the mark at size*SS, then downsample to size."""
    big = size * SS
    k = big / float(GRID)
    img = Image.new("RGBA", (big, big), NAVY)
    d = ImageDraw.Draw(img)

    def rect(box):
        x0, y0, x1, y1 = box
        d.rectangle([x0 * k, y0 * k, x1 * k - 1, y1 * k - 1], fill=BRASS)

    def poly(points):
        d.polygon([(x * k, y * k) for x, y in points], fill=BRASS)

    if BORDER:
        d.rectangle([0, 0, big - 1, big - 1], outline=BRASS, width=int(round(BORDER * k)))
    rect(N_LEFT)
    rect(N_RIGHT)
    poly(N_DIAG)
    rect(Z_TOP)
    rect(Z_BOTTOM)
    poly(Z_DIAG)
    return img.resize((size, size), Image.LANCZOS)


def svg():
    def r(box):
        x0, y0, x1, y1 = box
        return '  <rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (
            x0, y0, x1 - x0, y1 - y0, "#B8954A")

    def p(points):
        pts = " ".join("%d,%d" % (x, y) for x, y in points)
        return '  <polygon points="%s" fill="#B8954A"/>' % pts

    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="NTRS_ZIB Research">' % (GRID, GRID),
        "  <title>NTRS_ZIB Research</title>",
        '  <rect width="%d" height="%d" fill="#0B1C2C"/>' % (GRID, GRID),
        r(N_LEFT), r(N_RIGHT), p(N_DIAG),
        r(Z_TOP), r(Z_BOTTOM), p(Z_DIAG),
        "</svg>",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    master = render(256)
    master.save("favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    master.resize((180, 180), Image.LANCZOS).convert("RGB").save(
        "apple-touch-icon.png", format="PNG", optimize=True)
    fh = open("icon.svg", "w", encoding="utf-8", newline="\n")
    fh.write(svg())
    fh.close()
    render(16).resize((160, 160), Image.NEAREST).save("scratch/icon_16_preview.png")
    render(32).resize((160, 160), Image.NEAREST).save("scratch/icon_32_preview.png")
    print("wrote favicon.ico, apple-touch-icon.png, icon.svg")
