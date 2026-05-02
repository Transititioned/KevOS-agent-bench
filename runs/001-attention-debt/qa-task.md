# KevOS Agent Bench Task Packet

## Run

- Run ID: 001-attention-debt
- Agent: qa-auditor
- Generated: 2026-05-02T16:08:30

You are running as part of the KevOS Agent Bench.

Your agent definition is below.

--- AGENT DEFINITION START ---

# Agent: QA / Auditor

## Purpose

Protect quality, credibility, usefulness, and professional judgement.

The QA / Auditor does not rewrite the work by default. Its job is to assess the output, identify risks, recommend improvements, and decide whether the work is ready for approval, revision, or rejection.

## Core responsibilities

The QA / Auditor checks:

- clarity of argument
- audience fit
- practical usefulness
- source and claim support
- tone and voice
- reputational risk
- AI-slop risk
- overclaiming
- structure and flow
- completeness against the original work packet
- suitability for approval

## Operating principle

The QA / Auditor is deliberately sceptical but not obstructive.

It should not nitpick for the sake of it. It should focus on issues that would materially affect usefulness, credibility, clarity, or publishability.

## Review stance

Use this stance:

> “Would I be comfortable putting this in front of a smart, busy professional who knows the topic and has limited patience for generic AI content?”

## Output contract

The QA / Auditor must produce:

1. Overall recommendation
2. Executive summary
3. Quality scorecard
4. Key strengths
5. Material issues
6. Suggested fixes
7. Claim and evidence review
8. Voice and tone review
9. Publishability recommendation
10. Final action list

## Recommendation options

Use one of:

- **Publish-ready**
- **Minor revision**
- **Major revision**
- **Park / reject**

## Scoring scale

Use a 1–5 scale:

1. Weak
2. Needs work
3. Acceptable
4. Strong
5. Excellent

## Key dimensions

Assess:

| Dimension | Question |
|---|---|
| Argument clarity | Is the central point clear and easy to follow? |
| Audience value | Would the intended audience find this useful? |
| Evidence strength | Are claims supported or appropriately framed? |
| Practicality | Does it provide usable takeaways? |
| Voice fit | Does it sound like Kev rather than generic AI? |
| Reputational safety | Could this create avoidable credibility or political risk? |
| Structure | Is the flow easy to skim and understand? |
| Distinctiveness | Is there a clear take, or is it generic? |
| Artefact usefulness | Is the supporting artefact usable on its own? |
| Approval readiness | Can this move to final review? |

## Special checks for KevOS Agent Bench

For this project, also check:

- Is the output useful as a reusable professional work packet?
- Are handoffs clear enough for the Operator / Chief of Staff agent?
- Are open questions captured cleanly?
- Does the output show evidence of human judgement rather than automated content production?
- Would this be defensible as a portfolio artefact?


--- AGENT DEFINITION END ---

--- AGENT TASK PROMPT START ---

\# QA Prompt — Attention Debt Article Package



You are the QA / Auditor agent for the KevOS Agent Bench.



Your job is to review the Builder output package for Use Case 001: Research-to-Article Pipeline.



\## Context



The Builder output package includes:



1\. LinkedIn post

2\. Blog article draft

3\. Supporting artefact: Message subtraction checklist

4\. Notes for QA

5\. Open questions



The approved angle is:



> AI has made workplace communication easier to create, but not easier to receive. The next productivity opportunity is reducing attention debt.



The intended audience includes:



\- project managers

\- business analysts

\- change managers

\- AI governance leads

\- internal communications people

\- delivery leaders

\- professionals interested in practical AI adoption



The desired tone is:



\- practical

\- balanced

\- delivery-focused

\- grounded

\- not anti-AI

\- not generic thought leadership

\- not obviously AI-generated

\- useful to a smart, busy professional reader



\## Review stance



Be sceptical but useful.



Do not rewrite the article by default.



Focus on issues that would materially affect:



\- clarity

\- credibility

\- usefulness

\- audience fit

\- publishability

\- reputational safety

\- voice fit



\## Specific checks



Review the package against these dimensions:



1\. Argument clarity

2\. Audience value

3\. Evidence strength

4\. Practical usefulness

5\. Voice fit

6\. AI-slop risk

7\. Structure and readability

8\. Artefact usefulness

9\. Reputational safety

10\. Approval readiness



\## Special instructions



\- Treat “attention debt” as a working concept unless sources are provided.

\- Flag unsupported factual claims.

\- Flag overclaiming.

\- Flag anything that sounds too much like generic LinkedIn content.

\- Check whether the article sounds anti-AI or balanced.

\- Check whether the checklist is practical enough as a standalone asset.

\- Check whether the blog article should be shortened.

\- Check whether the LinkedIn post has enough bite.

\- Check whether the whole package is strong enough to proceed to an approval pack.



\## Output format



Produce the QA report using this structure:



\# QA Report — Use Case 001: Attention Debt



\## Recommendation



Choose one:



\- Publish-ready

\- Minor revision

\- Major revision

\- Park / reject



\## Executive summary



\## Quality scorecard



| Dimension | Score / 5 | Notes |

|---|---:|---|

| Argument clarity |  |  |

| Audience value |  |  |

| Evidence strength |  |  |

| Practicality |  |  |

| Voice fit |  |  |

| Reputational safety |  |  |

| Structure and readability |  |  |

| Distinctiveness |  |  |

| Artefact usefulness |  |  |

| Approval readiness |  |  |



\## Key strengths



\## Material issues



| Issue | Severity | Why it matters | Suggested fix |

|---|---|---|---|



\## Claim and evidence review



| Claim / concept | Status | Notes |

|---|---|---|



\## Voice and tone review



\## Structure review



\### LinkedIn post



\### Blog article



\### Supporting artefact



\## Reputational risk review



\## Recommended edits



\## Handoff to Operator / Chief of Staff



Include:



\- recommended decision

\- final approval risks

\- open questions to resolve

\- what should go into the approval pack



--- AGENT TASK PROMPT END ---

You will now receive the run inputs.

## Execution rules

- Follow your agent definition.
- Follow the agent task prompt if one is supplied.
- Use only the supplied inputs unless you clearly flag that more research is needed.
- Produce the standard output format defined in your agent file or task prompt.
- Be practical, grounded, and useful.
- Do not include fake citations or invented source details.
- If evidence is missing, say so clearly.
- Write in Markdown.

--- RUN INPUTS START ---


---

# Input file: intake.md

\# Intake — Attention Debt and AI Communication



\## Seed idea



AI has made workplace communication easier to create, but not easier to receive.



The bottleneck has shifted from content production to attention management.



\## Source material



\- Reddit/thread seed on AI and internal communication

\- Notes on “attention debt”

\- Existing ChatGPT discussion about article pipeline and agent bench



\## Initial reaction



This is a strong professional angle because it connects AI adoption, change management, internal communications, PM delivery, and executive signal-to-noise.



\## Possible audience



\- Project Managers

\- Business Analysts

\- Change Managers

\- AI governance leads

\- Internal communications teams

\- Delivery leaders



\## Possible angle



The next wave of AI productivity will not come from generating more workplace content. It will come from reducing the cognitive load that workplace content creates.



\## Why this may matter



Organisations are adopting AI tools that make it easier to produce emails, updates, summaries, reports, meeting notes, and presentations.



That creates a new risk: more content, more noise, more review burden, and more decision fatigue.



\## Risks / sensitivities



\- Avoid sounding anti-AI.

\- Avoid sounding like communication teams are the problem.

\- Avoid generic “AI is changing work” fluff.

\- Keep it practical and delivery-focused.



\## Target output



Create an approval-ready article pack containing:



\- LinkedIn post

\- Blog article draft

\- Message subtraction checklist

\- QA report

\- Approval pack



---

# Input file: strategy-pack.md

<!-- Generated by KevOS Agent Bench on 2026-05-02T14:45:17 -->

# Strategy Pack

## Recommended angle

AI has lowered the cost of creating workplace communication, but it has not lowered the cost of consuming it. The strongest angle is that organisations now need to manage “attention debt” as a delivery and governance risk, not just a communication problem.

Position this as a practical piece for delivery, change, AI governance, and internal communications professionals who are trying to use AI productively without flooding stakeholders with more updates, summaries, decks, and messages.

The article should argue that the next productivity gain from AI will not come from producing more communication faster. It will come from using AI and better communication discipline to reduce unnecessary cognitive load.

## One-line thesis

AI makes workplace content easier to produce, but the real productivity opportunity is reducing the attention burden that content creates.

## Target audience

Primary audience:

- Project Managers
- Business Analysts
- Change Managers
- Delivery leads
- AI governance leads
- Internal communications professionals

Secondary audience:

- Senior stakeholders responsible for organisational effectiveness
- Transformation leaders
- Product and operations leaders dealing with cross-functional communication overload

The framing should speak to professionals who are already seeing more AI-generated updates, summaries, meeting notes, reports, and presentations, but who need practical guidance rather than broad commentary about AI.

## Why this matters

The supplied inputs suggest a clear and useful workplace tension:

- AI tools make it easier to generate emails, updates, reports, meeting notes, summaries, and slide content.
- That increases the risk of more communication being produced simply because it is easier to produce.
- The constraint shifts from writing effort to reader attention.
- If unmanaged, this may create more noise, review burden, duplicated messaging, stakeholder fatigue, and decision friction.
- For delivery teams, this becomes a practical issue because projects depend on stakeholder clarity, timely decisions, and shared understanding.

This matters because many AI adoption conversations focus on production efficiency: faster drafting, faster summarising, faster reporting. The more useful professional question is whether communication is making work easier to act on.

## Core argument

The article should make a balanced argument:

AI is useful, but using it mainly to generate more workplace communication risks creating attention debt. Every extra update, summary, deck, or message has a receiving cost. Someone has to read it, interpret it, decide whether it matters, reconcile it with other messages, and possibly act on it.

In delivery environments, this cost is not trivial. Poor signal-to-noise slows decisions, confuses accountabilities, increases stakeholder fatigue, and makes important information easier to miss.

The practical response is not to reject AI. It is to use AI with stronger communication discipline. Teams should treat attention as a limited organisational resource and apply “message subtraction” before adding more content.

## Supporting points

- **AI changes the economics of communication.**  
  Drafting used to be a constraint. AI reduces that constraint, which means more people can produce more polished communication more quickly.

- **The receiving side does not scale in the same way.**  
  Stakeholders still have limited time, attention, context, and decision capacity.

- **More content can reduce clarity rather than improve it.**  
  If every meeting creates a summary, every workstream creates an update, and every stakeholder receives more polished but overlapping messages, the organisation may become better informed on paper but less aligned in practice.

- **Attention debt is a useful concept for delivery teams.**  
  Like technical debt or process debt, it accumulates when teams defer the hard work of prioritising, editing, deciding, and simplifying.

- **The issue is not internal comms quality alone.**  
  This should be framed as a shared operating problem across delivery, change, leadership, governance, and AI adoption.

- **The practical move is message subtraction.**  
  Before sending or generating another piece of content, teams should ask:
  - Who actually needs this?
  - What decision or action should it support?
  - What can be removed?
  - What can be combined?
  - What can be made self-serve?
  - What should not be communicated at all?

- **AI can help solve the problem it contributes to.**  
  Used well, AI can summarise, prioritise, tailor, deduplicate, and test messages for clarity. Used poorly, it can create a flood of plausible but low-value communication.

## Alternative angles considered

### 1. “AI is creating workplace communication overload”

This is close to the recommended angle but slightly weaker.

**Pros:**
- Clear and relatable.
- Easy to understand.
- Strong fit for LinkedIn and blog audiences.

**Cons:**
- Risks sounding anti-AI.
- Could become generic “AI creates noise” commentary.
- Less distinctive than the attention debt framing.

**Decision:** Use as a supporting idea, not the main angle.

---

### 2. “The future of AI productivity is attention management”

This is strong and could work as the headline-level framing.

**Pros:**
- Strategic and forward-looking.
- Connects AI productivity with practical organisational effectiveness.
- Suitable for senior audiences.

**Cons:**
- Could become too abstract unless grounded in delivery examples.
- Needs practical tools to avoid sounding like thought leadership.

**Decision:** Use as the main article frame, anchored through “attention debt” and “message subtraction”.

---

### 3. “Internal communications teams need to change how they use AI”

This is not recommended as the main angle.

**Pros:**
- Specific audience.
- Directly relevant to comms teams.

**Cons:**
- Risks blaming communications professionals.
- Narrows the audience too much.
- Misses the broader delivery and governance relevance.

**Decision:** Avoid making comms teams the centre of responsibility. Position the issue as cross-functional.

---

### 4. “AI governance should include communication governance”

Potentially useful but too specialised for the main article.

**Pros:**
- Strong fit for AI governance leads.
- Opens a useful governance conversation.
- Practical if focused on policies, review standards, and quality controls.

**Cons:**
- May feel too formal or heavy for a LinkedIn/blog article pack.
- Could drift into process design rather than professional commentary.
- Needs more evidence or examples to support properly.

**Decision:** Mention as an implication, but do not make it the main thesis unless further research is gathered.

---

### 5. “Stop generating content and start removing it”

Strong, punchy, and practical.

**Pros:**
- Memorable.
- Supports the checklist idea.
- Good fit for a LinkedIn post or article section.

**Cons:**
- Could sound too absolute if not balanced.
- Needs careful wording to avoid seeming anti-AI or anti-communication.

**Decision:** Use as a practical sub-angle, especially for the message subtraction checklist.

## Risks / sensitivities

- **Anti-AI perception:**  
  The piece must not imply AI communication tools are bad. The argument should be that AI needs better operating discipline.

- **Blaming internal communications:**  
  Avoid framing communications teams as the cause of the problem. The issue is broader: delivery teams, leaders, governance forums, project teams, and AI users all contribute to signal-to-noise.

- **Generic AI commentary:**  
  Avoid broad claims like “AI is transforming work” unless tied directly to the communication burden.

- **Overclaiming productivity impact:**  
  The inputs do not provide data, case studies, or research evidence. Do not make quantified claims about productivity loss, email volume, meeting costs, or cognitive overload.

- **Inventing evidence:**  
  Do not cite studies, companies, statistics, or examples unless additional research is provided.

- **Sounding elitist about communication:**  
  The tone should not suggest that people should communicate less because stakeholders are too busy. The argument is about making communication more useful, not withholding information.

- **Overcomplicating the concept of attention debt:**  
  Explain it simply: the accumulated cost of unnecessary, duplicated, unclear, or low-value communication that stakeholders must process.

## What to avoid

Avoid:

- “AI is ruining workplace communication.”
- “Internal comms teams are flooding people.”
- “Nobody reads anything anymore.”
- “The solution is fewer emails” as a simplistic takeaway.
- Generic AI transformation language.
- Claims that AI has definitively reduced or increased productivity without evidence.
- Excessive focus on individual time management.
- Academic discussion of cognitive load unless kept practical.
- A moralistic tone about people using AI “wrong”.
- A purely tactical listicle with no strategic argument.

The article should not become a rant about communication overload. It should be a practical positioning piece about how mature teams should use AI in communication-heavy environments.

## Recommended output

The Builder should produce an approval-ready article pack based on the recommended angle.

Recommended pack contents:

1. **LinkedIn post**  
   A concise professional post introducing the idea of attention debt and making the case that AI communication needs subtraction, not just generation.

2. **Blog article draft**  
   A structured article aimed at delivery, change, AI governance, and internal communications professionals.

3. **Message subtraction checklist**  
   A practical checklist teams can use before sending AI-assisted updates, summaries, reports, or stakeholder communications.

4. **QA report**  
   A review against tone, claims, risk, audience fit, and practical usefulness.

5. **Approval pack**  
   A short summary of the intended audience, core message, risks managed, and final approval notes.

## Builder instructions

Produce the article pack using the following direction:

### Approved angle

AI has made workplace communication easier to create, but not easier to receive. The next productivity opportunity is reducing attention debt.

### Core thesis

The bottleneck has shifted from content production to attention management. Teams should use AI not only to generate communication but also to reduce, prioritise, clarify, and remove low-value communication.

### Tone

Use a tone that is:

- Professional
- Grounded
- Practical
- Delivery-focused
- Lightly opinionated
- Balanced about AI
- Useful to working professionals

Avoid hype, cynicism, and marketing language.

### Article structure suggestion

For the blog article, use a structure similar to:

1. **Opening:** AI has reduced the effort required to produce workplace communication.
2. **Problem:** The receiving burden has not reduced. Stakeholders now face more polished noise.
3. **Concept:** Define attention debt.
4. **Delivery impact:** Explain how attention debt affects decisions, alignment, governance, and change.
5. **Practical shift:** Move from message generation to message subtraction.
6. **Checklist:** Introduce practical questions teams should ask before sending.
7. **Balanced AI point:** AI can either add to the noise or help reduce it depending on how it is used.
8. **Close:** Mature AI adoption should measure communication by usefulness, not volume.

### LinkedIn post direction

The LinkedIn post should be concise and sharp. It should not try to include every point. It should introduce the central contrast:

- Easier to write does not mean easier to read.
- More communication does not mean more alignment.
- The next AI productivity gain may come from subtracting messages, not generating them.

End with a practical prompt or question, not engagement bait.

### Checklist direction

The message subtraction checklist should be directly usable. It should include questions such as:

- Who needs this?
- What decision or action does it support?
- What is the minimum useful version?
- What can be removed?
- Is this duplicating another message?
- Is this better as a dashboard, decision log, meeting note, or direct conversation?
- What should the reader do after reading it?
- Can AI help shorten, prioritise, or tailor it?
- Is this being sent because it is useful, or because it is easy to generate?

### Evidence handling

Do not include invented statistics, citations, or named examples. If evidence is needed, use cautious phrasing such as:

- “A likely risk is…”
- “In many delivery environments, this can show up as…”
- “The practical concern is…”
- “This is less about AI itself and more about how teams use it.”

### Important framing

Make clear that the recommendation is not “communicate less” in a blanket sense. The recommendation is to communicate with more discipline, clearer purpose, and less unnecessary receiving burden.

## QA focus areas

The QA/Auditor should check:

- Does the output avoid sounding anti-AI?
- Does it avoid blaming internal communications teams?
- Is the concept of attention debt clearly explained?
- Is the piece practical enough for delivery, change, governance, and comms professionals?
- Are there any unsupported claims, statistics, or invented examples?
- Does the article avoid generic AI thought leadership?
- Does the LinkedIn post have a clear professional point without becoming engagement bait?
- Does the checklist provide actionable message subtraction questions?
- Does the blog article connect AI communication to delivery outcomes such as decision quality, alignment, and stakeholder load?
- Is the tone grounded, credible, and commercially aware?
- Does the final pack make clear that AI can help reduce communication burden when used with discipline?

---

# Input file: draft-output.md

<!-- Generated by KevOS Agent Bench on 2026-05-02T15:09:22 -->

# Draft Output

## Source inputs used

- `intake.md` — seed idea, audience, target outputs, risks/sensitivities.
- `strategy-pack.md` — approved angle, core thesis, target audience, article structure, LinkedIn direction, checklist direction, evidence handling guidance.

Note: The requested QA report and approval pack are downstream outputs for the QA/Auditor and Operator/Chief of Staff. This Builder draft includes the LinkedIn post, blog article draft, and supporting artefact only, with short handoff notes.

## Output package summary

This draft package develops the approved angle:

> AI has made workplace communication easier to create, but not easier to receive. The next productivity opportunity is reducing attention debt.

Included drafts:

1. LinkedIn post introducing the attention debt idea.
2. Blog article draft for delivery, change, AI governance, and internal communications audiences.
3. Message subtraction checklist as a reusable supporting artefact.

The tone is intended to be practical, balanced, delivery-focused, and not anti-AI.

---

## Draft 1: LinkedIn post

AI has made workplace communication easier to create.

It has not made it easier to receive.

That distinction matters.

A project update, meeting summary, stakeholder email, briefing note or slide pack might now take minutes to draft. But someone still has to read it, interpret it, compare it with other messages, decide whether it matters, and work out what to do next.

That receiving cost is where many teams are starting to feel the pressure.

More polished communication does not automatically create more alignment.

In some delivery environments, it can create attention debt: the accumulated cost of unnecessary, duplicated, unclear or low-value messages that stakeholders still have to process.

The answer is not to stop communicating.

It is to apply more discipline before sending.

Before creating another AI-assisted update, it is worth asking:

- Who actually needs this?
- What decision or action does it support?
- What can be removed?
- Is this duplicating something else?
- What is the minimum useful version?

AI can help teams write faster.

Used well, it can also help teams shorten, prioritise, tailor and remove communication that does not need to exist.

The next productivity gain may not come from generating more messages.

It may come from subtracting the ones that make work harder to understand.

A useful test: if this message is easy to produce but hard to act on, should it be sent at all?

---

## Draft 2: Blog article

# AI has made communication easier to create. It has not made it easier to receive.

AI is changing the economics of workplace communication.

Emails, project updates, summaries, reports, briefing notes, meeting notes and slide content are all easier to draft than they used to be. A message that once took half an hour can now be produced in minutes. A rough set of notes can become a polished update quickly. A meeting transcript can become a summary before the next meeting starts.

That can be useful.

But it also creates a new problem.

The effort required to produce workplace communication has dropped. The effort required to consume it has not.

Someone still has to read the update. Someone still has to understand the summary. Someone still has to decide whether the message matters, reconcile it with other information, and work out whether action is required.

The bottleneck has shifted.

It is no longer just content production. It is attention management.

## The hidden cost is on the receiving side

Most workplace communication is created with good intent.

A project manager wants to keep stakeholders informed.  
A change manager wants to support adoption.  
A business analyst wants to clarify decisions.  
A governance lead wants transparency.  
A leader wants their team to understand what is changing.

AI can help all of these people communicate faster and more clearly.

The practical concern is what happens when every team, workstream and forum can now produce more communication with less effort.

Every meeting can generate a summary.  
Every project can generate a status update.  
Every decision can generate a briefing note.  
Every stakeholder group can receive a tailored version.  
Every rough thought can become a polished message.

On paper, the organisation may look better informed.

In practice, people may be carrying more to read, more to filter, and more to interpret.

That is where attention debt starts to build.

## What is attention debt?

Attention debt is the accumulated cost of unnecessary, duplicated, unclear or low-value communication that stakeholders are expected to process.

It is similar in spirit to technical debt or process debt.

It builds when teams defer the hard work of simplifying, prioritising and removing.

Instead of deciding what really matters, another update is sent.  
Instead of clarifying the decision required, a longer summary is produced.  
Instead of combining overlapping messages, each workstream sends its own version.  
Instead of removing low-value detail, AI is used to make the detail sound more polished.

The debt does not always show up immediately.

It shows up when stakeholders miss the important update because it was buried in routine noise.  
It shows up when governance forums spend time re-reading context rather than making decisions.  
It shows up when teams are technically informed but not actually aligned.  
It shows up when people stop trusting that messages are worth their attention.

This is not just a communications issue.

For delivery teams, attention debt can become a delivery risk.

## Why this matters for delivery

Projects and change work depend on attention.

They need stakeholders to notice the right things at the right time. They need decisions to be clear. They need risks to be understood. They need people to know what has changed, what has not changed, and what is expected of them.

Poor signal-to-noise can make that harder.

A likely risk is slower decision-making. If decision-makers are receiving too much background information, they may spend more time sorting the message than making the call.

Another risk is weak alignment. Different groups may receive different updates that are all technically correct but not well connected. The result can be confusion about priorities, accountabilities or next steps.

Stakeholder fatigue is also a practical concern. When people receive too many messages that do not clearly affect them, they may start scanning or ignoring the channel. Once that habit forms, important messages are easier to miss.

None of this means teams should communicate less as a blanket rule.

Some environments need more transparency, not less. Some stakeholders need better context. Some changes fail because communication is too thin or too late.

The point is more specific.

Communication should earn the attention it asks for.

## The shift from message generation to message subtraction

A mature use of AI in workplace communication is not simply:

“How can we draft this faster?”

A better question is:

“Should this message exist in this form?”

That is the move from message generation to message subtraction.

Message subtraction is the discipline of reducing the receiving burden before adding more communication to the system.

It does not mean withholding useful information. It means removing avoidable effort from the reader.

That might include:

- cutting background detail that does not change the decision
- combining overlapping updates
- turning repeated status information into a dashboard
- making reference material self-serve
- replacing a broad email with a direct conversation
- clarifying the action required at the top
- tailoring the message to the people who genuinely need it
- deciding not to send a message that exists only because it was easy to generate

This is where AI can be useful in a different way.

Instead of only asking AI to draft more content, teams can ask it to reduce communication load.

For example:

- “Shorten this to the minimum useful version.”
- “Identify duplicated points.”
- “Separate decision points from background context.”
- “Rewrite this for a stakeholder who only needs the impact and next action.”
- “Turn this into a one-page decision note.”
- “List what can be removed without losing meaning.”
- “Check whether the action required is clear.”

Used poorly, AI can create a flood of plausible, polished, low-value messages.

Used well, it can help teams clarify, prioritise and subtract.

## A simple pre-send test

Before sending an AI-assisted update, summary, report or stakeholder message, teams can ask a few practical questions.

### 1. Who actually needs this?

Not who could receive it.  
Not who might find it mildly interesting.  
Who needs it to make a decision, take action, understand a change, or stay appropriately informed?

If the answer is “everyone”, test that assumption.

Different groups may need different levels of detail. Some may need a decision. Some may need a short impact summary. Some may only need access to the information if they choose to look for it.

### 2. What decision or action does it support?

If the message does not support a decision, action or clear understanding, it may need a different format.

A common issue is sending information because it exists, not because it is useful.

The reader should not have to work hard to understand why they are receiving the message.

### 3. What is the minimum useful version?

AI can make long messages sound better. That does not always make them better messages.

The minimum useful version is the shortest version that still gives the reader what they need.

That might be three bullets, a decision table, a short summary with a link to detail, or a clear “no action required” note.

### 4. What can be removed or combined?

Attention debt often builds through duplication.

Two updates cover similar ground.  
A report repeats what was already in the dashboard.  
A meeting summary restates content already captured in a decision log.  
A stakeholder email includes background detail from previous messages.

Before sending, check whether the message can be combined with something else, shortened, or replaced by a reference point that already exists.

### 5. Is this the right channel?

Not every message belongs in an email, chat post, slide deck or meeting note.

Some information is better as a dashboard.  
Some belongs in a decision log.  
Some needs a direct conversation.  
Some should sit in a project site or knowledge base.  
Some needs to be raised in governance, not circulated informally.

AI can help create the content, but the team still needs to choose the right communication method.

### 6. What should the reader do next?

This is one of the simplest tests.

After reading, should the person:

- approve something?
- make a decision?
- provide input?
- prepare for a change?
- note a risk?
- take no action?

If the next step is unclear, the message is not ready.

## This is not anti-AI

The issue is not AI itself.

The issue is operating discipline.

AI is useful when it helps people communicate with more clarity and less friction. It can help draft, summarise, translate, tailor and structure information. For busy teams, that can be valuable.

But if the main use case is producing more communication because production is now cheaper, the organisation may simply move the cost downstream.

Less effort for the sender can become more effort for the reader.

That trade-off matters in communication-heavy environments.

Delivery, change and governance work all rely on shared attention. If that attention is fragmented, even good information can lose its value.

## A better measure of communication quality

A useful question for AI-enabled teams is not:

“How much communication did we produce?”

It is:

“Did this communication make the work easier to understand, decide on or act on?”

That question changes the standard.

It rewards clarity over volume.  
It favours usefulness over polish.  
It treats stakeholder attention as a limited organisational resource.  
It encourages teams to remove noise before adding more content.

The next wave of AI productivity may not come from generating more workplace communication faster.

It may come from reducing the attention burden that communication creates.

That starts with a simple discipline:

Before using AI to create another message, use it to ask what can be removed.

---

## Draft 3: Supporting artefact

# Message subtraction checklist

A practical pre-send checklist for AI-assisted workplace communication.

Use this before sending project updates, stakeholder emails, meeting summaries, reports, briefing notes, governance papers or internal announcements.

## 1. Purpose

Before drafting or sending, answer:

- What is this message for?
- What decision, action or understanding should it support?
- What problem does it solve for the reader?
- Is this communication needed now?
- What happens if we do not send it?

If the purpose is unclear, pause before drafting.

## 2. Audience

Check who genuinely needs the message.

- Who must read this?
- Who only needs access if they want the detail?
- Who does not need this at all?
- Are different audiences being given the same level of detail unnecessarily?
- Is the message being sent widely because that is useful, or because it is easier?

Practical test: remove every audience group that does not need to decide, act, prepare, approve, understand an impact, or stay formally informed.

## 3. Reader action

Make the expected response clear.

After reading, should the reader:

- approve?
- decide?
- provide input?
- note a risk?
- prepare for a change?
- cascade the message?
- attend a session?
- update a plan?
- take no action?

If no action is required, say so clearly.

Example:

> No action required this week. This update is for awareness before the May governance discussion.

## 4. Minimum useful version

Ask:

- What is the shortest version that still does the job?
- Can the key message be understood in the first 30 seconds?
- Can background detail move to an appendix, link or reference page?
- Can this be a decision table, short summary or dashboard entry instead of a long message?
- Are we using AI to make the message clearer, or just longer and more polished?

Practical test: write the one-sentence version first. Then add only what the reader needs.

## 5. Duplication check

Before sending, check for overlap.

- Has this already been communicated elsewhere?
- Is another team or workstream sending a similar update?
- Does this repeat content from a dashboard, meeting note, decision log or previous email?
- Can this be combined with another message?
- Can we link to the existing source instead of restating it?

If the message duplicates existing content, either remove it, combine it, or explain why a separate message is needed.

## 6. Channel choice

Choose the format that creates the least receiving burden.

| Need | Better format may be |
|---|---|
| Quick decision | Decision note or direct request |
| Status visibility | Dashboard or short update |
| Formal governance | Governance paper or decision log |
| Behaviour change | Change communication plus manager support |
| Detailed reference | Knowledge base, project site or appendix |
| Sensitive issue | Direct conversation before written follow-up |
| Routine meeting record | Short meeting note with decisions and actions only |

Ask:

- Is this better as a dashboard?
- Is this better as a decision log entry?
- Is this better handled in a meeting?
- Is this better as a direct conversation?
- Is this better as self-serve reference material?

## 7. Clarity check

Before sending, check whether the reader can quickly see:

- why they are receiving it
- what has changed
- what matters most
- what decision or action is needed
- by when
- who owns the next step
- where to find more detail

If any of these are missing, revise before sending.

## 8. AI use check

Use AI to reduce load, not just create more content.

Useful prompts:

- “Shorten this to the minimum useful version.”
- “Remove duplicated points.”
- “Separate decision points from background context.”
- “Rewrite this for a senior stakeholder who needs the impact, decision required and deadline.”
- “Identify anything that is unclear or unnecessary.”
- “Turn this into a short decision note.”
- “Create a version for people who only need the key change and next action.”
- “List what can be removed without losing meaning.”

Avoid using AI only to make a low-value message sound more polished.

## 9. Final subtraction test

Before sending, ask:

- Is this useful, or just easy to generate?
- Will this reduce confusion or add another item to process?
- Would the reader know what to do after reading it?
- Can any part be removed?
- Can any audience be removed?
- Can any detail be moved elsewhere?
- Is this the right moment to send it?

If the message does not pass this test, revise, combine, defer or do not send.

## 10. Simple pre-send template

Use this short structure when a message is still needed.

```markdown
Subject / heading:
[Clear topic and action if required]

Why you are receiving this:
[One sentence]

Key message:
[One to three bullets]

Decision or action required:
[Decision/action/owner/date, or “No action required”]

What has changed:
[Only if relevant]

Detail:
[Minimum useful context, or link to source]

Contact / owner:
[Name or role]
```

---

## Alternative options

### Alternative LinkedIn opening 1

AI has made it cheaper to create workplace communication.

That does not mean the organisation has more attention to spend.

Every extra update, summary, deck or briefing note still creates work for someone else.

The question is no longer just “Can we generate this?”

It is “Should anyone have to read this?”

### Alternative LinkedIn opening 2

The next AI productivity gain may be less glamorous than faster content generation.

It may be better message subtraction.

Shorter updates.  
Clearer asks.  
Less duplication.  
Fewer unnecessary summaries.  
More useful decision notes.

### Alternative blog titles

- The next AI productivity problem is attention debt
- AI communication needs more subtraction, not just faster drafting
- Easier to write, harder to receive: AI and workplace attention debt
- Why AI-enabled teams need to manage attention debt
- Stop measuring AI communication by volume

### Alternative names for the checklist

- Communication subtraction checklist
- Attention debt pre-send check
- AI communication discipline checklist
- Minimum useful message checklist
- Stakeholder attention checklist

---

## Notes for QA

- No statistics, external research, named examples or citations have been included because none were supplied.
- The “attention debt” concept is explained as a practical working concept, not as an established research term.
- Please check that the article remains balanced and does not sound anti-AI.
- Please check whether “message subtraction” is clear enough for the intended audience or needs a shorter definition earlier.
- The blog article is moderately long; QA may want to test whether it should be tightened for the intended publishing channel.
- The checklist is designed as a standalone artefact and may be reusable as a Workfriend-style asset later.
- Please check whether the delivery impact section is concrete enough without overclaiming.

## Open questions

1. Is “attention debt” the preferred term, or should it be softened to “stakeholder attention debt” or “communication attention debt”?
2. Where will the blog article be published — personal website, LinkedIn article, company blog, newsletter, or internal platform?
3. Should the article use Australian spelling consistently for the final channel? This draft uses Australian workplace phrasing and spelling where applicable.
4. Does the user want a stronger AI governance angle, or should governance remain a secondary implication?
5. Should the checklist be branded as a standalone asset, or kept plain for now?
6. Are there any real examples from the user’s delivery experience that can be safely generalised and added without naming clients or organisations?
--- RUN INPUTS END ---