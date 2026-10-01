import html

USERNAME = "alnif1"
DETAILS = [
    ("OS", "Linux / Cloud-Native"),
    ("Host", "alnif1-box"),
    ("Role", "Cloud & DevOps Engineer"),
    ("Stack", "Python, Docker, K8s, CI/CD, Azure/OCI"),
    ("Interests", "DevSecOps, Platform Eng, AI Automation"),
    ("Status", "Building scalable cloud infra"),
]

def generate_card(output_path="info-card.svg"):
    width, height = 480, 240
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>',
        '  .t { font-family: ui-monospace, monospace; font-size: 13px; }',
        '  .user { fill: #58a6ff; font-weight: bold; }',
        '  .key { fill: #7ee787; font-weight: bold; }',
        '  .val { fill: #c9d1d9; }',
        '  .fade { opacity: 0; animation: f 0.4s ease-out forwards; }',
        '  @keyframes f { to { opacity: 1; } }',
        '</style>',
        '<rect width="100%" height="100%" fill="#0d1117" rx="6" stroke="#30363d"/>',
        '<g class="fade" style="animation-delay: 0.1s;">',
        f'  <text x="20" y="32" class="t user">{html.escape(USERNAME)}@github</text>',
        '  <text x="20" y="48" class="t val">-----------------------------</text>',
        '</g>'
    ]

    y, delay = 72, 0.25
    for k, v in DETAILS:
        lines.append(f'<g class="fade" style="animation-delay: {round(delay, 2)}s;">')
        lines.append(f'  <text x="20" y="{y}" class="t key">{k}:</text>')
        lines.append(f'  <text x="110" y="{y}" class="t val">{html.escape(v)}</text>')
        lines.append('</g>')
        y += 24
        delay += 0.1

    lines.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[+] Info card generated: {output_path}")

if __name__ == "__main__":
    generate_card()
