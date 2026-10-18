---
title: UPI MDR vs credit card MDR
status: draft
channel: linkedin
topic: fintech / payments / India
created: 2026-10-18
---

🚦 UPI is about to stop being free, but only above ~$23. And the fee tops out at ~$3.40. A credit card charges ~2% with no cap.

💸 MDR (Merchant Discount Rate) is the fee a merchant pays on every digital payment, split between the issuing bank, the acquirer and the network. The customer never sees it.

📣 What was announced: an NPCI circular (Sept 15) brings the first MDR on UPI since Jan 2020:
- 0.4% on person-to-merchant payments above ~$23
- Capped at ~$3.40 (the cap bites at ~$850)
- Essentials (rail, telecom, fuel, insurance): flat ~$0.06 above the threshold
- Capital markets: 0.02%, same cap
- P2P stays free. Merchant pays, never the customer.
- 95%+ of UPI merchant volume sits below the threshold, so it stays free
Go-live was Oct 15. On Oct 13 NPCI deferred it to "immediately after Diwali", date to be notified.

💳 The traditional model: credit card MDR runs ~1.5-2.5% of the ticket (premium and corporate cards cost more), with no cap. On an illustrative 2%: ~1.65% to the issuer, ~0.25% acquirer, ~0.10% network. The issuer's cut funds rewards, interest-free float and fraud losses.

🧮 Same payment, two bills (UPI 0.4% vs card ~2%):
$11 → $0 vs ~$0.22
$114 → ~$0.45 vs ~$2.27
$850 → ~$3.40 vs ~$17
$2,270 → ~$3.40 vs ~$45

💡 Why the gap? UPI is a push from a bank account: no credit line, no rewards, no float. And "free" was never free. The govt incentive covers only ~11% of the industry's cost (parliamentary panel), so 0.4% is a first step at closing that gap.

🛠️ What it means if you build payments:

1️⃣ Fee = f(amount, MCC, instrument), not one rate. UPI now needs slabs, category overrides and a cap: min(0.4% x amount, cap).

2️⃣ Test the cliff. At the threshold exactly: $0. One cent over: a fee, and if it applies to the full ticket, it jumps from $0 to ~$0.09. Read the circular for which.

3️⃣ Go-live is "TBD". Make rates and effective dates config, not a deploy.

4️⃣ Settlement turns net. Book MDR as its own ledger line per transaction, or recon drifts. And decide: does a refund return the MDR?

5️⃣ Expect ticket-splitting. Two $20 payments beat one $40. Plan the velocity rules.

👇 When MDR lands on UPI, will merchants absorb it, surcharge it, or push customers back to cash?

#fintech #upi #payments #npci #mdr

---

<!-- NOT FOR PUBLISHING: sources and assumptions, verify before posting

Currency: rule is `$` only. Rupee figures converted at ~Rs 88/$ (approximate,
adjust if you prefer another rate):
  Rs 2,000 (threshold)  ~ $23      Rs 300 (cap)        ~ $3.40
  Rs 75,000 (cap bites) ~ $850     Rs 5 (essentials)   ~ $0.06
  Worked table: Rs 1,000 ~ $11, Rs 10,000 ~ $114, Rs 2,00,000 ~ $2,270

Facts as reported by secondary outlets (primary NPCI circular not opened):
- NPCI circular dated 2026-09-15: 0.4% MDR on specified P2M UPI payments above
  Rs 2,000, capped at Rs 300 for Rs 75,000+; flat Rs 5 for railways/telecom/fuel/
  insurance above Rs 2,000; capital markets 0.02% capped at Rs 300.
- Originally effective 2026-10-15; deferred (NPCI release ~2026-10-13) to
  "immediately post Diwali", exact date to be notified (Diwali 2026-11-08).
- P2P free; merchants pay, not consumers; NPCI: 95%+ of UPI merchant volume by
  count is below Rs 2,000.
- Zero MDR on UPI P2M since Jan 2020 (earlier up to ~0.30%).
- Parliamentary panel: govt incentive covers ~11% of industry cost.
- Credit card MDR ~1.5-2.5% (sources range 1-3%); Deloitte illustrative 2%
  split: issuer ~1.65%, acquirer ~0.25%, network ~0.10%.

Unconfirmed, check the circular before relying on it:
- Whether 0.4% applies to the full ticket or only the amount above Rs 2,000
  (the cap math, 0.4% x Rs 75,000 = Rs 300, implies full ticket).
- Whether MDR is reversed on refunds.
- The reported 40/30/20/10 split (customer bank / PG / UPI app / sponsor bank)
  is from a single outlet and is deliberately left out of the post.
- The Rs 5 and 0.02% rates were described by one outlet as proposals.

Sources:
https://insights.dsij.in/dsijarticledetail/upi-mdr-rollout-deferred-npci-pushes-04-charge-beyond-diwali-id022-59996
https://organiser.org/2026/10/14/386311/bharat/mdr-on-upi-transactions-till-rs-2000-postponed-govts-digital-payments-push-remains-focused-on-accessibility/
https://www.businesstoday.in/latest/economy/story/npci-likely-to-defer-upi-mdr-rollout-announcement-expected-on-friday-report-560537-2026-10-08
https://inc42.com/buzz/parliamentary-panel-calls-for-mdr-on-upi-to-ensure-sustainability/
https://razorpay.com/blog/merchant-discount-rate-mdr
https://www2.deloitte.com/content/dam/Deloitte/in/Documents/financial-services/in-fs-spotlight-on-payments-technology-vol-3-card-oct-23-noexp.pdf
-->
