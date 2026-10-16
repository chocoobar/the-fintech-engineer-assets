---
title: Reconciliation drift
status: draft
channel: linkedin
topic: fintech / system design
created: 2026-09-14
---

🧩 Reconciliation breaks are rarely caused by a bug. They're caused by two systems that are each correct — and still disagree.

🔍 Here's the trace:

💳 A customer pays $10,000 by card. The moment the gateway's webhook says "success," your ledger marks it captured at $10,000, the full charge. Nothing failed. Your ledger is correct. ✅

📅 Two days later, the gateway's settlement batch credits your bank account — not $10,000, but $9,800 🏦, after deducting its ~2% MDR fee. The gateway's file is also correct; it was always going to net the fee before payout, contractually.

⚖️ Neither system is wrong. But unless your reconciliation logic explicitly accounts for the fee, that $200 gap ⚠️ looks unexplained. Multiply this by partial captures, missed refund webhooks, FX timing, and T+2 settlement lag — and you get a drift that compounds daily without ever throwing an error 🚨. "What my ledger says" and "what actually happened to the money" slowly stop matching.

🛠️ What a real EOD recon job needs to catch this:

1️⃣ Three-way matching, not two. Ledger vs. gateway report isn't enough — you need the actual bank statement too. "Ledger and gateway agree" doesn't guarantee the money that landed matches either.

2️⃣ Match on a stable identifier, not amount+date heuristics — two $5,000 same-day transactions will falsely match or mismatch otherwise. Use the gateway's transaction reference, the same id your idempotency key should already track.

3️⃣ A rolling window, not a same-day cutoff. Settlement lag (T+1/T+2) means a transaction won't match today but will tomorrow — the window must reflect the processor's SLA, or you'll flag normal lag as a break daily.

4️⃣ Classify every break explicitly — gateway-only (lost webhook?), ledger-only (normal lag or real problem?), in-tolerance (fee/rounding) vs. out-of-tolerance (something's wrong 🚩). Auto-clear only the explainable ones.

5️⃣ Unresolved breaks post to a suspense account, not just an alert someone dismisses. It keeps the books balanced while investigated, and leaves an audit trail 🧾 instead of a lost Slack message.

6️⃣ Recon itself must be idempotent and replayable 🔁 — re-running it after a fix shouldn't double-count matches or re-raise resolved breaks. Store each run as a versioned snapshot for audit.

💡 Recon isn't a batch job you write once. Add a new payment method, a new PSP, or change a fee structure, and an assumption baked into your matching logic quietly stops holding — the drift returns in a new shape. It's a question your system has to keep re-answering: do these two correct records actually agree?

👇 Has a recon break in your system ever turned out to be a legit settlement-lag or fee difference misclassified as fraud before someone caught it? I'd like to hear the trace.

#fintech #softwareengineering #systemdesign #payments #reconciliation
