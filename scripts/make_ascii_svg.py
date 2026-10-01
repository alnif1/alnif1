from PIL import Image

RAMP = " .`:-=+*cs#%@"

def generate_ascii_svg(image_path="source-prepped.png", output_path="ascii.svg", cols=68):
    img = Image.open(image_path)
    w, h = img.size
    aspect_ratio = h / w
    rows = int(cols * aspect_ratio * 0.55)
    img = img.resize((cols, rows)).convert("L")

    lines = []
    for y in range(rows):
        line = ""
        for x in range(cols):
            pixel = img.getpixel((x, y))
            idx = int((pixel / 255) * (len(RAMP) - 1))
            line += RAMP[idx]
        lines.append(line.rstrip())

    char_w, line_h = 7.2, 12
    svg_w = int(cols * char_w + 20)
    svg_h = int(rows * line_h + 30)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">',
        '<style>',
        '  .term { font-family: "Courier New", monospace; font-size: 11px; fill: #58a6ff; white-space: pre; }',
        '</style>',
        f'<rect width="100%" height="100%" fill="#0d1117" rx="6" stroke="#30363d"/>',
    ]

    stagger = 0.035
    for i, line in enumerate(lines):
        escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        delay = round(i * stagger, 2)
        y_pos = 20 + (i * line_h)
        svg.append(f'<g transform="translate(10, {y_pos})">')
        svg.append(f'  <clipPath id="c{i}"><rect x="0" y="-10" width="0" height="{line_h + 4}">')
        svg.append(f'    <animate attributeName="width" from="0" to="{svg_w}" dur="0.35s" begin="{delay}s" fill="freeze"/>')
        svg.append(f'  </rect></clipPath>')
        svg.append(f'  <text class="term" clip-path="url(#c{i})">{escaped}</text>')
        svg.append('</g>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[+] ASCII SVG generated: {output_path}")

if __name__ == "__main__":
    generate_ascii_svg()
