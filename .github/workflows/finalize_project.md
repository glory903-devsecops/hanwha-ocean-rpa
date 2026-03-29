---
description: Finalize Hanwha Ocean RPA Project (5-hour sprint)
---

1. **Sync Repository**
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Create Working Branch**
   ```bash
   git checkout -b finalization-$(date +%Y%m%d%H%M)
   ```
3. **Activate Virtual Environment & Install Dependencies**
   ```powershell
   .\\venv\\Scripts\\Activate.ps1
   pip install -r requirements.txt
   ```
4. **Run Security & Style Linters**
   ```bash
   flake8 src
   bandit -r src
   ```
5. **Execute Unit Tests**
   ```bash
   pytest -q
   ```
6. **Start Local HTTP Server**
   ```bash
   python -m http.server 8000
   ```
7. **Record Demo Video** (30‑seconds) using browser subagent:
   - Open `http://localhost:8000/smart_yard_dashboard.html`
   - Navigate to admin portal `http://localhost:8000/src/viz/admin_guidance.html`
   - Capture interactions and save as `demo.mp4`
8. **Update README**
   - Add polished project overview, architecture diagram, demo video embed, CI badge, and detailed usage guide.
9. **Commit & Push**
   ```bash
   git add .
   git commit -m "Finalize project: refactor, tests, docs, demo"
   git push origin HEAD
   ```
10. **Open Pull Request** on GitHub (optional manual step).

**Notes**
- Steps 3‑5 are safe‑to‑auto‑run after user approval.
- Step 7 will generate a video artifact stored in the artifacts folder.
- Ensure Windows PowerShell execution policy allows script activation.
