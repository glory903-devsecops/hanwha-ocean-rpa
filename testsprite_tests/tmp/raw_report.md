
# TestSprite AI Testing Report(MCP)

---

## 1️⃣ Document Metadata
- **Project Name:** hanwha-ocean-rpa
- **Date:** 2026-03-27
- **Prepared by:** TestSprite AI Team

---

## 2️⃣ Requirement Validation Summary

#### Test TC001 post api v1 update dock with valid payload
- **Test Code:** [TC001_post_api_v1_update_dock_with_valid_payload.py](./TC001_post_api_v1_update_dock_with_valid_payload.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 53, in <module>
  File "<string>", line 46, in test_post_api_v1_update_dock_with_valid_payload
AssertionError: Safety issue mismatch in dashboard-status

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/ccdf6ff4-e925-4928-88d7-ff04e83cab8b/eef439c8-b03d-4773-a18a-d9e7b2063c3e
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC002 post api v1 update dock with missing required fields
- **Test Code:** [TC002_post_api_v1_update_dock_with_missing_required_fields.py](./TC002_post_api_v1_update_dock_with_missing_required_fields.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 83, in <module>
  File "<string>", line 28, in test_post_api_v1_update_dock_missing_required_fields
AssertionError: Setup failed: Expected 200, got 422

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/ccdf6ff4-e925-4928-88d7-ff04e83cab8b/38667f65-6e8d-4296-b92d-d6ac675e2fc9
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC003 get api v1 dashboard status returns updated dock record
- **Test Code:** [TC003_get_api_v1_dashboard_status_returns_updated_dock_record.py](./TC003_get_api_v1_dashboard_status_returns_updated_dock_record.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 56, in <module>
  File "<string>", line 46, in test_get_api_v1_dashboard_status_returns_updated_dock_record
AssertionError: Safety issue value mismatch

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/ccdf6ff4-e925-4928-88d7-ff04e83cab8b/7254ee28-f5cf-42bb-a004-37735c80ce94
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC004 get dashboard serves updated tailwind html
- **Test Code:** [TC004_get_dashboard_serves_updated_tailwind_html.py](./TC004_get_dashboard_serves_updated_tailwind_html.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 79, in <module>
  File "<string>", line 46, in test_get_dashboard_serves_updated_tailwind_html
AssertionError: Dashboard fetch failed, status code 404

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/ccdf6ff4-e925-4928-88d7-ff04e83cab8b/02160047-b080-4d8d-bbbe-3d4720df6f40
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC005 get dashboard handles generation failure and logs error
- **Test Code:** [TC005_get_dashboard_handles_generation_failure_and_logs_error.py](./TC005_get_dashboard_handles_generation_failure_and_logs_error.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 82, in <module>
  File "<string>", line 47, in test_get_dashboard_generation_failure_and_log_error
AssertionError: Expected 500 Internal Server Error but got 404

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/ccdf6ff4-e925-4928-88d7-ff04e83cab8b/b7b5e6e2-8c28-4fd1-ba35-6a34fd464197
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC006 get api v1 analytics returns d day prediction and recommendations
- **Test Code:** [TC006_get_api_v1_analytics_returns_d_day_prediction_and_recommendations.py](./TC006_get_api_v1_analytics_returns_d_day_prediction_and_recommendations.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 63, in <module>
  File "<string>", line 46, in test_get_api_v1_analytics_returns_d_day_prediction_and_recommendations
AssertionError

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/ccdf6ff4-e925-4928-88d7-ff04e83cab8b/4f635e7a-a07e-4c5c-bf98-1dcba1a0e8b4
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC007 get api v1 analytics explain returns model explanation
- **Test Code:** [TC007_get_api_v1_analytics_explain_returns_model_explanation.py](./TC007_get_api_v1_analytics_explain_returns_model_explanation.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 77, in <module>
  File "<string>", line 47, in test_get_api_v1_analytics_explain_returns_model_explanation
AssertionError: Analytics explain failed: {"detail":"Not Found"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/ccdf6ff4-e925-4928-88d7-ff04e83cab8b/c6260a9a-99f5-47ee-a2b3-418398dca7a1
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC008 get api v1 analytics returns 404 for unknown dock id
- **Test Code:** [TC008_get_api_v1_analytics_returns_404_for_unknown_dock_id.py](./TC008_get_api_v1_analytics_returns_404_for_unknown_dock_id.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 31, in <module>
  File "<string>", line 20, in test_get_api_v1_analytics_returns_404_for_unknown_dock_id
AssertionError: Expected status code 404, got 200

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/ccdf6ff4-e925-4928-88d7-ff04e83cab8b/f4a4ef68-3b91-4bdd-abdf-951093fe726e
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC009 get api v1 export report returns csv data
- **Test Code:** [TC009_get_api_v1_export_report_returns_csv_data.py](./TC009_get_api_v1_export_report_returns_csv_data.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 32, in <module>
  File "<string>", line 23, in test_get_api_v1_export_report_returns_csv_data
AssertionError: Expected Content-Type text/csv but got application/json

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/ccdf6ff4-e925-4928-88d7-ff04e83cab8b/914cf681-311f-4d36-af67-9698240b68b7
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC010 get api v1 export report handles unsupported format and no content
- **Test Code:** [TC010_get_api_v1_export_report_handles_unsupported_format_and_no_content.py](./TC010_get_api_v1_export_report_handles_unsupported_format_and_no_content.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 41, in <module>
  File "<string>", line 18, in test_get_api_v1_export_report_unsupported_format_and_no_content
AssertionError: Expected 400 Bad Request for unsupported format but got 200

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/ccdf6ff4-e925-4928-88d7-ff04e83cab8b/ada14773-8754-49f8-af1e-4670ed6a90e9
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---


## 3️⃣ Coverage & Matching Metrics

- **0.00** of tests passed

| Requirement        | Total Tests | ✅ Passed | ❌ Failed  |
|--------------------|-------------|-----------|------------|
| ...                | ...         | ...       | ...        |
---


## 4️⃣ Key Gaps / Risks
{AI_GNERATED_KET_GAPS_AND_RISKS}
---