# ⚓ Hanwha Ocean AX: Enterprise Design System (v25.1.0)

본 문서는 현재 가동 중인 **Isometric Digital Twin Dashboard**를 Figma에서 정교하게 재현하고 편집하기 위한 디자인 사양서입니다.

---

## 🎨 Color Palette (Atomic Tokens)

| Token | HSL / Hex | Usage |
| :--- | :--- | :--- |
| **Enterprise Orange** | `#FF6B00` | Primary Call-to-Action, Progress Bars, Brand Logo |
| **Blueprint Cyan** | `#00F2FF` | Technical Accents, Active State, Data Twin Sync Labels |
| **Deep Space Navy** | `#020617` | Base Background (Overlay Layer) |
| **Glass Surface** | `rgba(30, 41, 59, 0.6)` | Card Backgrounds (Backdrop-filter: blur(40px)) |
| **Critical Red** | `#EF4444` | Danger Status, High-Risk Alerts |
| **Caution Amber** | `#F59E0B` | Warning Status, Yard Maintenance Alerts |
| **Optimal Green** | `#10B981` | Safe Status, Normal Operation |

---

## 📐 Typography (Modern Industrial)

- **Primary Font**: `Outfit` (Google Fonts) - Geometric, high-tech feel.
- **Support Font**: `Noto Sans KR` - High readability for Korean field taskers.

| Level | Size | Weight | Tracking |
| :--- | :--- | :--- | :--- |
| **Headline XL** | `8xl (8rem)` | 900 (Black) | `-0.05em` (Tighter) |
| **HUD Subtitle** | `xl (1.25rem)` | 900 (Black) | `1em` (Monospaced style) |
| **Metric Value** | `6xl` | 900 (Black) | `Tight` |
| **Metadata** | `10px` | 900 (Black) | `2em` (Spaced) |

---

## 🏗 Component Geometry (HUD Widgets)

1.  **GlassHUD Card**:
    - **Corner Radius**: `2.5rem (40px)`
    - **Border**: `1px solid rgba(255, 255, 255, 0.05)`
    - **Shadow**: `0 30px 60px -15px rgba(0, 0, 0, 0.6)`
2.  **Progress Bar**:
    - **Height**: `6px`
    - **Indicator Shadow**: `0 0 10px #FF6B00`
3.  **Left Sidebar (Tactical Panel)**:
    - **Width**: `25%` of Workspace
    - **Padding**: `40px (10 units)`

---

## 💡 Figma Workflow Tips

1.  **HTML-to-Design**: Figma 플러그인 `html.to.design`을 사용하고 URL에 `https://glory903-devsecops.github.io/hanwha-ocean-rpa/`를 입력하면 모든 요소가 레이어 형태로 임포트됩니다.
2.  **Background Replacement**: 배경 이미지인 `docs/images/final_dashboard_sample.png`를 최하단 레이어로 배치하고 투명도를 100%로 설정한 뒤, 그 위에 Glass 레이어들을 얹어 편집하십시오.
3.  **Design Handoff**: 수정한 Figma 디자인의 **스크린샷**을 본 채팅창에 보내주시면, 해당 공간 구성과 그리드를 즉시 코드로 구현해 드리겠습니다.

---
© 2026 Hanwha Ocean AX Team. Enterprise UI Spec.
