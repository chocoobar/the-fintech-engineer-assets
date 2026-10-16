---
title: Eventual Consistency Is Fine—Until You're Moving Money
status: draft
channel: substack
topic: fintech / distributed systems
created: 2026-09-27
---

Distributed systems have taught us an important lesson: you can't always have everything.

You want low latency.
You want high availability.
You want horizontal scalability.
You want independent services.
And, somewhere along the way, someone tells you:

*"It's okay. The system is eventually consistent."*

And most of the time, it is.

If your product catalog takes two seconds to reflect a price change, nobody loses sleep.

If an analytics dashboard is thirty seconds behind, that's usually acceptable.

If a notification arrives a few seconds late, it's rarely a production incident.

But now replace the product catalog with a bank balance.

Replace the analytics dashboard with an available credit limit.

Replace the notification with a ledger entry.

Suddenly, "eventually" becomes a much more complicated word.

Because when you're moving money, the problem isn't that different services may temporarily disagree. The problem is deciding what they are allowed to disagree about.

## The Distributed Systems Reality

Consider a simple payment flow:

```
Client
   |
   v
Payment Service
   |
   v
Ledger Service
   |
   v
Payment Gateway
```

In a monolithic system with a single database transaction, we might be tempted to think of this as one operation:

```
Debit money
+
Update transaction
+
Update balance
+
Record ledger
=
One transaction
```

Distributed systems don't give us that luxury.

As systems grow, we naturally separate responsibilities:

```
Payment Service
       |
       +----> Ledger Service
       |
       +----> Notification Service
       |
       +----> Analytics
       |
       +----> Reconciliation
```

Now each component may have its own database, its own transaction boundary, and its own failure modes.

We introduce messaging.

We introduce Kafka.

We introduce asynchronous processing.

We introduce retries.

And eventually, we introduce eventual consistency.

That's not inherently bad.

In fact, it's often exactly what allows a system to scale.

The mistake is assuming that eventual consistency should apply equally to every piece of financial state.

It shouldn't.

## A $7,000 Problem

Imagine a customer has:

**Available Balance = $10,000**

They send two withdrawal requests almost simultaneously:

- Request A → $7,000
- Request B → $7,000

Suppose these requests reach two different instances of the payment service.

Both read:

**Available Balance = $10,000**

Both perform the same check:

$10,000 >= $7,000

Both approve.

Now:

- Transaction A = SUCCESS
- Transaction B = SUCCESS

Total approved: **$14,000**

Available funds: **$10,000**

Your system may eventually converge.

Maybe the balance projection catches up.

Maybe the ledger consumer processes the events.

Maybe reconciliation detects the discrepancy.

But there is a fundamental problem: the system violated a financial invariant before it had a chance to become consistent again.

This is the distinction that matters.

## Consistency Is Not One Thing

When engineers say:

*"This service is eventually consistent."*

The immediate question should be:

*Eventually consistent with respect to what?*

There are several different things that can become inconsistent:

- Transaction state
- Account balance
- Ledger entries
- Notifications
- Analytics
- Search indexes
- Reporting
- Risk calculations
- Available credit
- Settlement status

They don't all need the same consistency guarantees.

For example:

| Component | Can tolerate eventual consistency? |
|---|---|
| Analytics dashboard | Usually |
| Email notification | Usually |
| Search index | Usually |
| Reporting | Usually |
| Customer activity feed | Usually |
| Ledger | Much less |
| Available balance | Depends on the business model, but often requires strict controls |
| Transaction state | Strong guarantees around allowed transitions |
| Double-spend prevention | No |

The important architectural decision isn't:

*"Should we use eventual consistency?"*

It is:

*"Where is eventual consistency acceptable, and where must we protect an invariant immediately?"*

## Think in Invariants, Not Services

This is one of the most useful ways to think about financial systems.

Instead of starting with:

*"We have a Payment Service, Balance Service and Ledger Service."*

Start with:

*"What must never become false?"*

For example:

- Available balance must not become negative.
- Every successful financial transaction must have a corresponding ledger record.
- A transaction cannot move from SUCCESS back to PROCESSING.
- The same business transaction cannot debit the customer twice.
- Total debits must be explainable by corresponding ledger entries.

These are business invariants.

Services are implementation boundaries.

Invariants are business boundaries.

That's an important difference.

## Strong Consistency Where It Matters

Suppose we have:

```
Account
---------
id
balance
version
```

A naïve implementation might do:

```sql
SELECT balance
FROM account
WHERE id = ?;
```

Then:

```
if balance >= amount:
    balance = balance - amount
```

The problem is that the read and write are separate operations.

Two requests can both observe the same balance.

Instead, we might use an atomic update:

```sql
UPDATE account
SET balance = balance - :amount
WHERE id = :accountId
  AND balance >= :amount;
```

Then verify the affected row count.

If `rows_updated = 1`, the debit succeeded.

If `rows_updated = 0`, the debit was not allowed.

The database is now protecting the invariant directly.

This is a much stronger design than *read → decide → write* when the decision depends on mutable financial state.

## But Strong Consistency Everywhere Doesn't Scale Either

There is another trap.

Once engineers understand the danger of inconsistency, they may try to make everything synchronous:

```
Payment
  |
  +--> Ledger
  |
  +--> Notification
  |
  +--> Analytics
  |
  +--> Reporting
  |
  +--> Fraud
  |
  +--> Customer timeline
```

The payment waits for all of them.

Now your payment latency is determined by the slowest dependency.

Worse, the availability of your payment system becomes coupled to every downstream service.

Analytics is down? Payments fail.

Notification service is slow? Payments become slow.

Reporting database is unavailable? Payments fail.

That is not a consistency strategy.

That's distributed coupling.

## Define a Consistency Boundary

A better architecture separates the things that must be correct immediately from things that can catch up later.

For example:

```
                 Payment Request
                       |
                       v
              +------------------+
              | Payment Boundary |
              |                  |
              | Transaction      |
              | State            |
              | Financial        |
              | Invariants       |
              +--------+---------+
                       |
                       v
                  Source of Truth
                       |
              +--------+---------+
              |                  |
              v                  v
          Event/Outbox       Ledger
              |
       +------+------+------+
       |      |      |      |
       v      v      v      v
    Notify Analytics Search Reporting
```

The critical path protects correctness.

Everything that doesn't need to participate in that correctness decision can consume events asynchronously.

This gives us an important principle:

**Make the smallest possible boundary strongly consistent. Let everything outside that boundary be eventually consistent where appropriate.**

## The Ledger Changes the Conversation

In many financial systems, the ledger is more important than a mutable balance column.

Consider:

```
Opening Balance      $10,000
Debit                -$2,000
Credit               +$500
Debit                -$1,000
--------------------------------
Closing Balance       $7,500
```

A balance is a projection.

The ledger provides the explanation.

This matters enormously during failures.

Suppose the balance says $7,500 but the customer claims:

*"I never made the $1,000 transaction."*

You need to answer:

- Which transaction caused it?
- When was it created?
- What was the previous state?
- What was the source?
- Was it authorized?
- Was it settled?
- Was it reversed?
- Was there a retry?
- Was it reconciled?

A single mutable balance cannot answer all of those questions.

A well-designed ledger can.

This is why financial systems often treat the ledger as a source of truth and build other representations from it.

## Eventual Consistency Actually Becomes Useful Here

Suppose the ledger records:

```
Transaction ID: TX123
Amount: $1,000
Type: DEBIT
Status: SUCCESS
```

From that event, we can asynchronously update:

- Balance Projection
- Customer Timeline
- Analytics
- Notifications
- Reporting
- Search

Now imagine the notification service is down.

The customer may not receive: *"$1,000 debited from your account."*

But the financial transaction itself doesn't need to fail just because the notification service is unavailable.

The notification can be delivered later.

That is a healthy use of eventual consistency.

## Kafka Doesn't Magically Make Money Consistent

This is another common misconception.

You may have:

```
Payment Service
      |
      v
    Kafka
      |
      +----> Ledger Consumer
      |
      +----> Notification Consumer
      |
      +----> Analytics Consumer
```

It looks beautifully decoupled.

But now ask: what happens if the payment database commits successfully but the Kafka publish fails?

You could end up with:

```
Database = SUCCESS
Kafka = no event
```

Now downstream systems never learn about the transaction.

The opposite can also happen:

```
Kafka = event published
Database = transaction rolled back
```

Now consumers believe something happened that the source transaction doesn't contain.

Messaging gives you asynchronous communication.

It does not automatically give you atomicity between your database and the message broker.

## The Outbox Pattern

One common solution is the transactional outbox.

Instead of:

```
DB transaction
     +
Kafka publish
```

we do:

```
Database Transaction
       |
       +--> Business State
       |
       +--> Outbox Event
```

Both are committed together.

For example:

```
Payment
---------
TX123
SUCCESS
$1,000
```

and:

```
Outbox
---------
Event: PAYMENT_SUCCESS
Transaction: TX123
Published: false
```

A separate publisher reads the outbox and sends the event to Kafka.

Now the system can retry publishing without losing the business event.

This doesn't eliminate every distributed-system problem.

But it creates a much more controlled failure model.

## What About Reconciliation?

Here's where financial systems differ from many ordinary applications.

Even with:

- transactions
- idempotency
- Kafka
- retries
- outbox
- locks

you should still assume something can go wrong.

Because eventually, two systems will disagree.

Maybe:

```
Our system:
PAYMENT = PROCESSING
```

while:

```
Gateway:
PAYMENT = SUCCESS
```

Or:

```
Our ledger:
$10,000
```

while:

```
External settlement:
$9,000
```

You need reconciliation.

Reconciliation isn't just a reporting exercise.

It is part of the correctness model.

A mature financial system should be able to answer:

*"If two systems disagree, how do we detect it, investigate it and bring them back into a known state?"*

That is a fundamentally different mindset from:

*"Hopefully the events eventually arrive."*

## The Transaction State Machine Matters

One of the easiest ways to introduce financial bugs is to model a transaction as:

```
SUCCESS / FAILED
```

Real transactions often have more meaningful states:

```
INITIATED
    |
    v
PROCESSING
    |
    +------> SUCCESS
    |
    +------> FAILED
    |
    +------> UNKNOWN
```

And later:

```
SUCCESS
    |
    v
SETTLED
    |
    v
RECONCILED
```

The `UNKNOWN` state is particularly important.

Imagine:

```
Payment request sent
        |
        v
Gateway processes it
        |
        v
Network timeout
```

Your application does not know whether the payment succeeded.

Calling it `FAILED` simply because you timed out can be dangerous.

The correct state may be `UNKNOWN`.

Then the system can resolve it through:

- gateway status inquiry
- asynchronous callback
- retry with idempotency
- reconciliation

A timeout is a network event.

It isn't necessarily a business outcome.

## Eventual Consistency Doesn't Mean Eventual Correctness

This distinction is worth emphasizing.

An eventually consistent system should eventually converge toward the correct state.

It should not mean: *"We'll figure it out later."*

Consider:

```
Transaction = SUCCESS
Ledger = SUCCESS
Balance = stale
Notification = pending
Analytics = stale
```

That's acceptable if the architecture guarantees that:

- Balance → eventually updated
- Notification → eventually delivered
- Analytics → eventually updated

But consider:

```
Transaction = SUCCESS
Ledger = missing
```

That's fundamentally different.

You now have a financial event without its accounting representation.

The question isn't how quickly the system becomes consistent.

The question is whether the system can prove that it will converge correctly.

## A Practical Consistency Matrix

When designing a fintech system, I like thinking about consistency as a matrix rather than a single architecture-wide setting.

| Data | Consistency | Why |
|---|---|---|
| Financial transaction state | Strongly controlled | Prevent invalid state transitions |
| Ledger entry | Strongly controlled | Financial correctness |
| Balance/debit authorization | Strongly controlled | Prevent overspending/double debit |
| Idempotency record | Strongly controlled | Prevent duplicate business operations |
| Notifications | Eventual | User communication can be delayed |
| Analytics | Eventual | Historical analysis doesn't need synchronous updates |
| Search index | Eventual | Query convenience |
| Customer activity feed | Eventual | Read experience |
| Reporting | Eventual | Can tolerate processing delay |
| Reconciliation | Asynchronous but authoritative | Detect and resolve discrepancies |

The exact boundaries will vary by product.

But the exercise itself is valuable.

## The Three Questions I Ask

Whenever I see eventual consistency in a financial workflow, I ask three questions.

### 1. What is the source of truth?

If two systems disagree, which one wins?

If the answer is *"It depends,"* that's usually a warning sign.

### 2. What invariant must never be violated?

For example:

- Money cannot be created accidentally.
- Money cannot disappear without an explainable entry.
- A transaction cannot be processed twice.
- A successful transaction must be represented in the ledger.

Write these down.

Then design around them.

### 3. How does the system recover from disagreement?

Don't just design the happy path.

Design for: success, failure, timeout, duplicate, retry, partial failure, message loss, consumer failure, database failure, gateway failure, reconciliation.

A financial system isn't reliable because nothing fails.

It's reliable because failure is expected and recoverable.

## The Architecture Principle

This leads to a broader architectural principle:

**Strong consistency should protect financial invariants. Eventual consistency should connect everything that doesn't need to participate in those invariants.**

You don't need every service to know about a transaction immediately.

You need the systems that determine whether money can move to agree on the critical facts.

Everything else can catch up.

That distinction allows you to build systems that are both financially safe and operationally scalable.

Instead of choosing between consistency and scalability, you define where each one belongs.

## Final Thought

Eventual consistency isn't the enemy of fintech.

In fact, it's one of the reasons large financial platforms can scale.

The real danger is using eventual consistency without defining what must never be eventually correct.

A notification can arrive later.

A dashboard can be stale.

An analytics pipeline can lag.

A search index can catch up.

But when $10,000 moves from one account to another, the system needs more than eventual convergence.

It needs an invariant.

It needs a source of truth.

It needs an auditable state transition.

And, when things inevitably go wrong, it needs a way to reconcile reality with what the system believes happened.

Because in fintech, the most important question isn't:

*"Will all our services eventually agree?"*

It's:

*"When they disagree, can we guarantee that money remains correct?"*

That's where distributed systems engineering becomes financial engineering.
