# n8n Workflow Blueprint: [Project Name]

**Prepared By:** [Name]  
**Date:** [YYYY-MM-DD]  
**Version:** 1.0

---

## Introduction 🧭

_Use this blueprint to kick off the standalone n8n workflow project "[Project Name]" to be delivered by our full-service agency for the client. This document serves as the foundation for our Product Management team to create a detailed Project Brief, which will then guide our Engineering team to create an Implementation Plan for building the specified production-ready workflow. Sections 1-4 are Q → A prompts for the Agency Lead. Sections 5-7 are research and investigation prompts for Product Managers. Sections 8-10 are collaborative logs for PM & Engineering._

---

## 1. Project Overview 🎯

- **1.1 Project Name:** 🏷️
- **1.2 Type of Work:** (New / Modify / Upgrade)
- **1.3 One-Sentence Purpose:**

---

## 2. Business Context & Objectives 📈

- **2.1 Why are we doing this?** ❓
  - ❓ Q: _What business problem or opportunity does this workflow address?_
  - ✅ A:
- **2.2 Desired KPI / Outcome:** ❓
  - ✅ A:
- **2.3 Stakeholders & End-Users:** ❓
  - ❓ Q: _Who benefits from this workflow? Internal teams, external users, or system-to-system only?_
  - ✅ A:

---

## 3. Current State (skip if new) 🏗️

- **3.1 Existing Workflow Name / ID:**
- **3.2 Pain Points / Limitations:**
- **3.3 Known Node Versions & Custom Nodes:**

---

## 4. High-Level Scope 🧩

- **4.1 Trigger(s):**
  - ❓ Q: _Describe the event(s) that starts the workflow (e.g., webhook hit, cron time, db change)._
  - ✅ A:
- **4.2 Key Inputs:**
  - ❓ Q: _List the data or parameters the workflow receives immediately after the trigger fires (payload fields, env vars, files, IDs to fetch, etc.)_
  - ✅ A:
- **4.3 Main Steps / Logic (bullet list):**
  - ❓ Q: _Outline the major actions the workflow performs, in order._
  - ✅ A:
- **4.4 Intended Outputs:**
  - ❓ Q: _Specify what the workflow produces or where it hands things off (records created, emails sent, files uploaded, API responses)._
  - ✅ A:
- **4.5 External Services / APIs:**
  - ❓ Q: _List third-party or internal APIs the workflow will call (Slack, Stripe, internal REST API, etc.)._
  - ✅ A:
- **4.6 Edge Cases & Error Scenarios:**
  - ❓ Q: _List any unusual inputs or failure conditions that must be handled gracefully (empty payloads, API rate-limit errors, malformed attachments, auth token expiry)._
  - ✅ A:
- **4.7 Workflow Diagram:**
  - _Visual guide for Engineering. Use as first-pass architecture; deviations allowed with justification._

```mermaid
<!-- paste your diagram here -->
```

_Note for Engineering when populating Section 9:_

- If you discover a better design pattern, call out changes.
- If any node or path is ambibiguous, raise a clarifying question.

---

## 5. Constraints, Assumptions & Risks ⚠️

- **5.1 Technical / Security Constraints:**
- **5.2 Rate Limits or Quotas:**
- **5.3 Must-Use Libraries / Auth Methods:**
- **5.4 Known Unknowns or Open Risks:**

---

## 6. MVP Definition 🚀

- **6.1 Must-Have Features for v1:**
- **6.2 Nice-to-Have (Deferred) Features:**
- **6.3 Explicit Non-Goals:**

---

## 7. Future-Proofing Ideas 🔭

_Think 6-24 months ahead; capture ideas so engineers can design with them in mind._

- **7.1 Scaling & Load:** ❓ _How might volume or concurrency grow over time?_
  - ✅ A:
- **7.2 Modularity & Reuse:** ❓ _Could parts of this workflow be converted to reusable sub-workflows or parameterised?_
  - ✅ A:
- **7.3 Version Upgrades:** ❓ _Are any APIs, nodes, or auth methods likely to deprecate soon?_
  - ✅ A:
- **7.4 Resilience & Failover:** ❓ _What fallback paths or redundancy could improve uptime?_
  - ✅ A:

---

## 8. Non-Functional Requirements (Engineering-Owned) 🔒

| #   | NFR Category          | Quantitative Target (or “TBD”) | Test Method | Owner | Status |
| --- | --------------------- | ------------------------------ | ----------- | ----- | ------ |
| 1   | Performance           |                                |             | ENG   | Open   |
| 2   | Reliability           |                                |             | ENG   | Open   |
| 3   | Security / Compliance |                                |             | ENG   | Open   |
| 4   | Observability         |                                |             | ENG   | Open   |
| 5   | CI/CD & Git           |                                |             | ENG   | Open   |
| 6   | Documentation         |                                |             | ENG   | Open   |

---

## 9. Dependency & Engineering Question Log 🤔

| #   | Topic / Dependency         | Question / Risk                         | Owner | Resolution / Link | Status |
| --- | -------------------------- | --------------------------------------- | ----- | ----------------- | ------ |
| 1   | Node Version Compatibility | Validate nodes on latest stable version | ENG   |                   | Open   |
| 2   | Sequence / Race Condition  |                                         | ENG   |                   | Open   |
| 3   | Edge-Case Handling         |                                         | PM    |                   | Open   |
| …   |                            |                                         |       |                   |        |

_Definition of Done: all rows “Closed” or migrated to Project Brief / Implementation Plan._

---

## 10. Success Metrics 📊

- ✅ All MVP features (Sec 6.1) implemented and tested.
- 🧪 Workflow passes QA including recovering gracefully in edge-case tests.
- 🔒 Meets NFR targets (Sec 8).
- 🛰️ Dependency & risk items closed (Sec 9).
- 🚚 Deployed via CI/CD to self-hosted environment; tagged in Git.
- 📄 Documentation (README + diagram) delivered.

---

## 11. Next Steps & Owners 🧾

- [ ] 📋 Blueprint completed (Sections 1-7).
- [ ] 🧐 Engineering reviews blueprint & fills Sections 8-9.
- [ ] 🔄 PM updates open questions (Sections 8-9).
- [ ] 📝 PM drafts Project Brief.
- [ ] ✅ Agency lead approves Project Brief.
- [ ] 📘 Eng drafts Implementation Plan.

---

## 12. How to Use ✍️

1. 🖊️ **Fill Sections 1-4** with current knowledge; use “TBD” for gaps.
2. 👥 **PMs review** this blueprint thoroughly and complete Sections 5-7.
3. 🛠️ **Engineering populates Sections 8-9**, confirming node compatibility, CI/CD, observability, and edge-case coverage.
4. 🔁 **Close open items** in Section 9; transfer final answers into the Project Brief & Implementation Plan.
5. 📌 **Tick through Section 11 checklist** until every item is complete.
