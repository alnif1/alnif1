import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def render(output_path="contrib-heatmap.svg"):
    with open("data/contributions.json", "r", encoding="utf-8") as f:
        days = json.load(f)

    box_size, gap = 10, 3
    pad_x, pad_y = 20, 20
    cols = 53
    width = pad_x * 2 + (cols * (box_size + gap))
    height = 140

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>',
        '  .box { opacity: 0; animation: pop 0.25s forwards; }',
        '  @keyframes pop { to { opacity: 1; } }',
        '</style>',
        '<rect width="100%" height="100%" fill="#0d1117" rx="6" stroke="#30363d"/>',
    ]

    last_year = days[-371:] if len(days) >= 371 else days
    for i, item in enumerate(last_year):
        col = i // 7
        row = i % 7
        x = pad_x + col * (box_size + gap)
        y = pad_y + row * (box_size + gap)
        color = PALETTE[min(item["level"], 4)]
        delay = (col * 0.015) + (row * 0.005)

        svg.append(
            f'<rect class="box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" '
            f'fill="{color}" rx="2" style="animation-delay: {delay:.3f}s;"/>'
        )

    svg.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[+] Heatmap generated: {output_path}")

if __name__ == "__main__":
    render()
