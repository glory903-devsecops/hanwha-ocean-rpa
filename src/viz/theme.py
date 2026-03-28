# Hanwha Ocean AX Unified Design System (v16.0.0)

THEME = {
    # 1. Color Palette (Enterprise Navy & Hanwha Orange)
    "colors": {
        "primary": "#FF6B00",        # Hanwha Core Orange
        "secondary": "#00F2FF",      # Tech Accent Cyan
        "background": "#020617",     # Deep Space Navy
        "surface": "rgba(30, 41, 59, 0.4)", # Glassmorphic Card (Navy-ish)
        "border": "rgba(255, 255, 255, 0.08)",
        "text_main": "#F8FAFC",
        "text_muted": "#94A3B8",
        "critical": "#EF4444",       # 위험 (Serious Risk)
        "warning": "#F59E0B",        # 주의 (Caution)
        "success": "#10B981"         # 정상/안전 (Optimal)
    },

    # 2. Typography Spec (V16: Increased sizing for visibility)
    "typography": {
        "font_family_main": "'Outfit', 'Inter', 'Noto Sans KR', sans-serif",
        "font_family_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "scale": {
            "h1": "5rem",      # Oversized KPIs
            "h2": "2.8rem",    # Section Headers
            "h3": "1.8rem",    # Card Titles (Increased 20%)
            "body": "1.1rem",  # Normal Text (Increased 20%)
            "tiny": "12px"     # Metadata
        }
    },

    # 3. Layout & Geometry (Atomic Spacing)
    "layout": {
        "spacing_base": 10,     # Increased Grid (10px)
        "card_radius": "40px",
        "inner_radius": "20px",
        "gap_large": "50px",
        "gap_main": "30px"
    },

    # 4. Effects (Figma Fidelity)
    "effects": {
        "glass_blur": "blur(50px)",
        "card_shadow": "0 30px 60px -15px rgba(0, 0, 0, 0.6)",
        "primary_glow": "0 0 30px rgba(255, 107, 0, 0.4)",
        "animation_speed": "0.8s"
    }
}

def get_css_vars():
    """Convert theme dictionary to CSS :root variables for HTML injection."""
    vars_list = []
    vars_list.append(f"--h-primary: {THEME['colors']['primary']};")
    vars_list.append(f"--h-secondary: {THEME['colors']['secondary']};")
    vars_list.append(f"--h-bg: {THEME['colors']['background']};")
    vars_list.append(f"--h-surface: {THEME['colors']['surface']};")
    vars_list.append(f"--h-border: {THEME['colors']['border']};")
    vars_list.append(f"--h-font-main: {THEME['typography']['font_family_main']};")
    vars_list.append(f"--h-glass-blur: {THEME['effects']['glass_blur']};")
    vars_list.append(f"--h-radius: {THEME['layout']['card_radius']};")
    # v16 font size injection
    vars_list.append(f"--h-size-h3: {THEME['typography']['scale']['h3']};")
    vars_list.append(f"--h-size-body: {THEME['typography']['scale']['body']};")
    return "\n        ".join(vars_list)
