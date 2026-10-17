---
title: Ready pods are not a healthy deploy
status: draft
channel: linkedin
topic: fintech / platform engineering
created: 2026-10-17
---

🚦 Your pods can be 100% Ready and your deploy can still be a payments outage.

🔍 Here's the trace:

🚀 You ship a payment-service change. A standard rolling update swaps pods one by one. Every new pod passes its readiness probe, so Kubernetes keeps going. Four minutes later, v2 is on 100% of traffic ✅

🧨 But v2 has a subtle bug: a rounding change makes ~8% of card authorizations come back HTTP 200 with DECLINED. No 5xx. No crash loop. No failed health check. Every error-rate dashboard stays green.

📉 Illustrative math: 1,000 auths/min x 8% = ~80 customers a minute staring at "card declined." Someone spots the approval-rate dip ~10 minutes later. That's ~800 wrongly declined payments, before the rollback even starts.

⚠️ Kubernetes asked "is this pod alive?" Nobody asked "is this version still approving payments?"

🛠️ What Argo Rollouts changes (a Rollout resource in place of your Deployment, deployed through Argo CD):

1️⃣ Canary in weighted steps. 5% → pause → 25% → pause → 100%. The same bug now touches ~50 auths/min, not 1,000.

2️⃣ Gate promotion on business metrics, not infra health. An AnalysisTemplate queries Prometheus for approval rate, decline-reason mix, p99 and ledger write failures. Miss the threshold and the rollout aborts itself, with traffic back on stable and no human in the loop. Here: ~3 minutes, ~12 wrongly declined payments 🎯

3️⃣ Guard against thin data. 5% of 3am traffic might be 10 requests, too few to trust. Use an inconclusiveCondition on sample size so the rollout pauses instead of waving a build through on silence.

4️⃣ Split by cohort, not coin flip. A random 5% can put a customer on v2 for the first attempt and v1 for the retry. Route by header or cohort where your traffic router allows it, and canary internal users or low-value merchants first.

5️⃣ Two versions run at once, so your contracts must too. Expand/contract DB migrations, backward-compatible event schemas, idempotency keys that mean the same thing in v1 and v2. A canary is a live test of every compatibility assumption you made.

6️⃣ An abort is not a revert. Traffic is back on v1, but Git still declares v2 and Argo CD shows the app Degraded. Revert the commit so the source of truth matches what's live.

💡 Progressive delivery turns a deploy from a bet on 100% of your customers into an experiment on 5%, with the blast radius decided before the release, not after the incident.

👇 What's the one metric you'd trust to auto-abort a payments deploy: approval rate, p99, or something sneakier?

#fintech #kubernetes #argocd #devops #platformengineering
