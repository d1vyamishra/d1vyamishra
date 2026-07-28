# Generates an animated "typing terminal" SVG header for the GitHub profile README
# Theme: matches the "Arise Core" purple/violet-pink dev aesthetic from the user's brand images

W, H = 900, 460
CYCLE = 15.0  # total loop duration in seconds

lines = [
    [("kw", "const "), ("var", "divya"), ("pl", ": "), ("type", "Developer"), ("pl", " = {")],
    [("pl", "  name: "), ("str", '"Divya Prakash Mishra"'), ("pl", ",")],
    [("pl", "  role: "), ("str", '"Full Stack Developer"'), ("pl", ",")],
    [("pl", "  location: "), ("str", '"India"'), ("pl", ",")],
    [("pl", "  stack: ["), ("str", '"React"'), ("pl", ", "), ("str", '"Vue.js"'), ("pl", ", "), ("str", '"TypeScript"'), ("pl", ", "), ("str", '"Node.js"'), ("pl", "],")],
    [("pl", "  currentFocus: "), ("str", '"Building fast, scalable web products end-to-end"'), ("pl", ",")],
    [("pl", "  funFact: "), ("str", '"I turn caffeine into code. ☕"'), ("pl", ",")],
    [("pl", "};")],
]

colors = {
    "kw": "#ff3fa3",
    "var": "#e8d5ff",
    "pl": "#c4b5fd",
    "type": "#a855f7",
    "str": "#7dd3fc",
}

char_w = 10.6
line_h = 34
start_x = 40
start_y = 108
font_size = 19

n = len(lines)
slot = 1.0  # seconds allotted to start each successive line
reveal_frac_of_slot = 0.85

svg_parts = []
svg_parts.append(f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#0d0221"/>
    <stop offset="45%" stop-color="#1a0630"/>
    <stop offset="100%" stop-color="#12081f"/>
    <animate attributeName="x1" values="0%;20%;0%" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#ff3fa3"/>
    <stop offset="50%" stop-color="#a855f7"/>
    <stop offset="100%" stop-color="#8b5cf6"/>
    <animate attributeName="x1" values="0%;100%;0%" dur="6s" repeatCount="indefinite"/>
    <animate attributeName="x2" values="100%;200%;100%" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <radialGradient id="glow" cx="50%" cy="0%" r="80%">
    <stop offset="0%" stop-color="#a855f7" stop-opacity="0.35"/>
    <stop offset="100%" stop-color="#a855f7" stop-opacity="0"/>
  </radialGradient>
  <style>
    .mono {{ font-family: 'SFMono-Regular', 'Fira Code', Consolas, 'Courier New', monospace; font-size: {font_size}px; }}
    .title {{ font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; }}
    .blink {{ animation: blink 1s steps(2, start) infinite; }}
    @keyframes blink {{ to {{ opacity: 0; }} }}
</style>
</defs>

<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="url(#bgGrad)"/>
<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="url(#glow)"/>
<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="16.5" fill="none" stroke="url(#borderGrad)" stroke-width="2"/>

<!-- title bar -->
<rect x="0" y="0" width="{W}" height="52" rx="18" fill="#150a29"/>
<rect x="0" y="34" width="{W}" height="18" fill="#150a29"/>
<circle cx="30" cy="26" r="7" fill="#ff5f57"/>
<circle cx="54" cy="26" r="7" fill="#febc2e"/>
<circle cx="78" cy="26" r="7" fill="#28c840"/>
<text x="{W/2}" y="31" text-anchor="middle" class="mono title" fill="#c4b5fd" font-size="14">divya.dev — ~/arise-core</text>
<line x1="0" y1="52" x2="{W}" y2="52" stroke="#2d1b4e" stroke-width="1"/>
''')

# animated title text (name + role) top-right ribbon removed - keeping it code focused

for i, line in enumerate(lines):
    y = start_y + i * line_h
    start_t = i * slot
    reveal_dur = slot * reveal_frac_of_slot
    end_reveal_t = start_t + reveal_dur
    hold_end_t = (n) * slot + 2.5          # everything holds until here
    fade_end_t = hold_end_t + 1.0          # fade out ends here
    # keyframe percentages (relative to CYCLE)
    p_start = round((start_t / CYCLE) * 100, 2)
    p_end = round((end_reveal_t / CYCLE) * 100, 2)
    p_hold = round((hold_end_t / CYCLE) * 100, 2)
    p_fade = round((fade_end_t / CYCLE) * 100, 2)

    # total rendered width of this line (approx monospace)
    total_chars = sum(len(t) for _, t in line)
    full_w = total_chars * char_w + 20

    clip_id = f"clip{i}"
    anim_id = f"reveal{i}"

    svg_parts.append(f'''
<style>
  @keyframes {anim_id} {{
    0% {{ width: 0px; }}
    {p_start}% {{ width: 0px; }}
    {p_end}% {{ width: {full_w:.1f}px; }}
    {p_hold}% {{ width: {full_w:.1f}px; }}
    {p_fade}%, 100% {{ width: 0px; }}
  }}
  #{clip_id} rect {{ animation: {anim_id} {CYCLE}s ease-in-out infinite; }}
</style>
<clipPath id="{clip_id}"><rect x="{start_x-4}" y="{y-22}" width="0" height="28"/></clipPath>
<g clip-path="url(#{clip_id})">
<text x="{start_x}" y="{y}" class="mono">''')

    cx = start_x
    tspans = []
    for kind, text in line:
        esc = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        tspans.append(f'<tspan fill="{colors[kind]}">{esc}</tspan>')
    svg_parts.append("".join(tspans))
    svg_parts.append('</text>\n')

    # cursor block on the last line only, sits right after the text, blinks once revealed
    if i == n - 1:
        cursor_x = start_x + full_w - 16
        svg_parts.append(f'<rect x="{cursor_x:.1f}" y="{y-16}" width="10" height="20" fill="#ff3fa3" class="blink"/>\n')

    svg_parts.append('</g>\n')

svg_parts.append('</svg>')

with open('/home/claude/build/assets/header.svg', 'w') as f:
    f.write("".join(svg_parts))

print("done, size:", len("".join(svg_parts)))
