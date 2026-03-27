# Hanwha Ocean RPA Dashboard Refactoring Plan

Refactor the existing RPA module to use modern web technologies (Tailwind CSS), professionalize the "Mission Control" UI, and enhance data reporting capabilities.

## User Review Required

> [!IMPORTANT]
> **Primary Technology Shift**: We are moving from static HTML template strings in Python to a modern, responsive frontend (Tailwind CSS). The "Mission Control" dashboard will be 100% localized in Korean.

## Proposed Changes

### [Component] RPA Frontend (Tailwind CSS)
- **Modernization**: Replace the current Plotly-based `smart_yard_dashboard.html` with a standalone, responsive dashboard using Tailwind CSS.
- **Data Visualization**: Integrate interactive charts (likely staying with Plotly or moving to ECharts) styled with Tailwind.
- **Report Feature**: Add a "CSV 보고서 다운로드" (Download CSV Report) button to the dashboard.
- **Localization**: Ensure 100% Korean text for all labels and headers.

#### [MODIFY] [dashboard.py](file:///g:/%EB%82%B4%20%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B8%8C/99.Develop/%ED%95%9C%ED%99%94%EC%98%A4%EC%85%98/hanwha-ocean-rpa/src/viz/dashboard.py)
#### [NEW] [rpa_dashboard_v2.html](file:///g:/%EB%82%B4%20%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B8%8C/99.Develop/%ED%95%9C%ED%99%94%EC%98%A4%EC%85%98/hanwha-ocean-rpa/rpa_dashboard_v2.html)

---

### [Component] Data Flow & ERP Integration
- **Flow Visualization**: Create the 3-step visualization flow (ERP Site -> CSV Excel DB -> RPA Dashboard) for the README.
- **CSV Management**: Ensure `server.py` and `generator.py` correctly handle the data hand-off to the new dashboard.

#### [MODIFY] [README.md](file:///g:/%EB%82%B4%20%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B8%8C/99.Develop/%ED%95%9C%ED%99%94%EC%98%A4%EC%85%98/hanwha-ocean-rpa/README.md)
#### [MODIFY] [server.py](file:///g:/%EB%82%B4%20%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B8%8C/99.Develop/%ED%95%9C%ED%99%94%EC%98%A4%EC%85%98/hanwha-ocean-rpa/src/api/server.py)

---

### [Component] Verification & Documentation
- **TestSprite**: Use `TestSprite` to verify the stability of the API and data flow.
- **GitHub Push**: Finalize the repository and push to the remote demo site.

## Verification Plan

### Automated Tests
- **TestSprite Deployment**: Run `testsprite_generate_code_and_execute` on the RPA API server to verify CSV updates.
- **UI Validation**: Use the browser tool to verify the responsiveness of the new Tailwind dashboard.

### Manual Verification
1. **End-to-End Test**: Enter data in `mock_portal.html`, check if `dock_status.csv` updates, and verify the new dashboard reflects changes.
2. **Download Check**: Click the "CSV 다운로드" button and verify the file content.
3. **README Review**: Confirm the 3 flow images accurately represent the project architecture.
