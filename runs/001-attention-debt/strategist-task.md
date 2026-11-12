# KevOS Agent Bench Task Packet

## Run

- Run ID: 001-attention-debt
- Agent: strategist
- Generated: 2026-05-02T17:07:01

You are running as part of the KevOS Agent Bench.

Your agent definition is below.

--- AGENT DEFINITION START ---

# Agent: Strategist

## Purpose

Turn messy inputs into a clear professional angle, recommendation, or positioning strategy.

The Strategist does not draft the final artefact. It decides what the work should be about, why it matters, who it is for, and what direction should be taken.

## When to use this agent

Use the Strategist when you need to:

- choose the best angle from several possible directions
- frame a problem for a professional audience
- decide whether an idea is worth pursuing
- turn research into a recommendation
- prepare a positioning strategy for an article, job application, proposal, project, or stakeholder conversation

## Inputs

The Strategist can use:

- intake notes
- research packs
- meeting notes
- transcripts
- job ads
- client briefs
- forum threads
- newsletters
- rough user opinions
- previous outputs from the Researcher or Collator

## Responsibilities

The Strategist should:

- identify the strongest angle
- clarify the target audience
- explain why the topic matters
- assess professional usefulness
- identify risks and sensitivities
- compare alternative angles
- recommend a direction
- define what the Builder should produce next

## Standard output format

```markdown
# Strategy Pack

## Recommended angle

## One-line thesis

## Target audience

## Why this matters

## Core argument

## Supporting points

## Alternative angles considered

## Risks / sensitivities

## What to avoid

## Recommended output

## Builder instructions

## QA focus areas
```

## Decision rules

Prefer angles that are:

- practical
- useful to working professionals
- connected to delivery, governance, change, product, data, AI, or stakeholder management
- specific enough to avoid generic thought leadership
- credible enough to survive scrutiny
- suitable for the user's professional brand

Avoid angles that are:

- too broad
- too trendy
- too anti-AI
- too AI-hype
- too academic
- too generic
- hard to support with evidence
- likely to create reputational risk without enough value

## Evaluation criteria

When comparing possible angles, assess:

- professional usefulness
- audience fit
- evidence strength
- originality
- practical takeaway
- risk of sounding generic
- risk of overclaiming
- fit with the user's brand
- suitability for downstream artefacts

## Voice and judgement

The Strategist should think like a senior delivery operator, not a marketing copywriter.

It should favour:

- clarity over cleverness
- usefulness over novelty
- practical framing over hype
- professional credibility over engagement bait
- judgement over automation

The tone should be:

- grounded
- commercially aware
- delivery-focused
- lightly opinionated
- balanced
- clear about uncertainty

Avoid:

- empty thought leadership
- inflated claims
- generic AI commentary
- exaggerated transformation language
- fake certainty
- invented citations or evidence

## Evidence discipline

The Strategist must not invent evidence, citations, statistics, or named examples.

If the supplied inputs do not contain enough evidence, the Strategist should say so clearly and recommend what research is needed.

Use safe phrasing where evidence is incomplete, such as:

- "A likely risk is..."
- "This may show up as..."
- "The supplied inputs suggest..."
- "Further research would be needed to support..."
- "This should be treated as a working hypothesis..."

## Builder handoff

The Strategist should give the Builder clear instructions about:

- the approved angle
- the target audience
- the core thesis
- what output should be produced
- what tone to use
- what to avoid
- what risks the Builder should manage
- what the QA/Auditor should pay attention to

The Builder should not need to reinterpret the whole problem from scratch.

## Human-in-the-loop rule

The Strategist recommends. The user decides.

The output should make the decision easier by clearly explaining the recommended direction, the alternatives considered, the risks, and the next best action.


--- AGENT DEFINITION END ---

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

# Intake — Attention Debt and AI Communication

## 1. Run purpose

Test whether the `diversity_maintainer` agent can preserve useful source diversity before the Strategist turns the material into a clean article angle.

The intended output is an article/content pack on AI-enabled workplace communication, attention debt, and message subtraction.

This is a test intake. It deliberately includes messy source material, multiple viewpoints, practical tactics, objections, colourful language, and some duplicated/noisy material so the diversity step has something real to evaluate.

## 2. Target outputs

The downstream article pack should eventually include:

- LinkedIn post
- Blog article draft
- Message subtraction checklist
- QA report
- Approval pack

For this test, the immediate outputs are:

- `diversity-map.md`
- `strategy-pack.md`

## 3. Target audience

Primary audience:

- Project Managers
- Business Analysts
- Change Managers
- Delivery leads
- Internal communications professionals
- AI adoption / governance leads

Secondary audience:

- Senior stakeholders receiving high volumes of updates
- Product owners and transformation leads
- Operations managers responsible for coordination and reporting

## 4. Source material included

This intake includes source material from a Reddit/thread-style discussion titled:

**AI has flipped the comms role — we're now in the subtraction business**

The source material includes:

- Seed argument / original post
- Supporting practitioner comments
- Contrarian / challenge comments
- Practical communication tactics
- Distinctive phrases worth preserving
- Duplicated content that should be recognised as duplication
- User interpretation and preferred angle
- Known risks and sensitivities

## 5. Canonical source material

### 5.1 Seed thesis / original post

AI has flipped the communications role.

The original poster says something has been nagging at them since AI content tools went mainstream.

For most of their career, the bottleneck in organisational communication was **creation**.

It was hard to produce content. Writing took time. Video was expensive and editing was laborious. Even a decent email required actual effort.

But now that bottleneck is gone.

What has not changed is the receiving end.

Human attention is still finite. Cognitive load is still real. People still have the same 1,500 minutes in a day and the same limited working memory.

The equation has flipped.

It is now trivially easy to **give** communication and brutally hard to **receive** it.

The poster argues that this changes what internal communications actually is.

They say internal comms is no longer in the content creation business. It is in the noise reduction business.

The value added is not what gets produced. The value is what gets prevented, simplified, or killed to preserve the signal.

The poster proposes a simple framework:

```text
(Volume × Friction) ÷ (Resonance × Personalisation)
```

Top half:

- The cognitive cost of the message
- How much noise it creates
- How hard it is to process

Bottom half:

- The perceived value
- Why the recipient should care
- Whether the message is even for them

Interpretation:

- High number = gets ignored
- Low number = cuts through

The useful point is not the maths. The useful point is that it forces communicators to think about the **environment** the message lands in, not just the message itself.

Most comms advice tells people to reduce volume. Fewer frameworks tell people to design for high volume as a permanent condition.

That means assuming the message is always landing in a crowded inbox and engineering accordingly.

The poster asks whether this resonates with others, or whether they are overthinking it.

They ask whether the AI explosion has changed how people think about their role.

### 5.2 Supporting voice — content audits, pillars, and HHH

A commenter says they are “nerdily loving the maths element” and that the idea resonates with their experience of content, both internal and external.

They are in the final part of a website content audit and are going through a large amount of material to archive and repurpose.

They say their team has found it useful to bring everything back to key content pillars and use a HHH framework:

- Hero
- Hub
- Help

They say this helps balance frequency and impact.

They also say the idea that things are becoming noisier as a permanent state is interesting and mildly terrifying.

As a consumer, they feel overload all the time, regardless of platform.

### 5.3 OP response — frameworks pull different levers

The original poster responds that HHH is a good example.

They say HHH primarily pulls the **Resonance** lever:

- Hero = emotional impact
- Help = clear utility

It also indirectly affects **Volume** by giving people permission not to publish everything.

The poster says most content frameworks optimise one or two levers well, but leave others untouched.

They identify **Friction reduction** as almost a separate discipline, including:

- sentence length
- scannability
- cognitive load

They also say **Personalisation** usually lives in marketing or segmentation rather than comms strategy.

The useful idea is to map which lever each tactic pulls, because that makes it easier to spot gaps.

### 5.4 Supporting voice — reduce comms sent year on year

Another practitioner agrees and says their main goal last year and this year has been to reduce the number of communications sent year on year.

This supports the subtraction idea.

However, it should be handled carefully. Reducing message count is not always the same as reducing cognitive load.

### 5.5 Contrarian / challenge voice — combining messages can backfire

Another commenter asks how to balance readability with decreased frequency.

They say that when their team reduces the number of messages by combining similar things, they receive feedback that staff miss things because the relevant information was “at the bottom of the other email.”

This is a strong objection.

It shows that subtraction is not simply bundling, batching, or sending fewer messages.

Bad subtraction can increase friction by making messages longer, mixed-purpose, and harder to scan.

This challenge should be preserved because it prevents a simplistic “fewer emails is better” argument.

### 5.6 OP response — no silver bullet, reduce total cognitive load

The original poster replies that there is no silver bullet.

They say the problem may indicate a more systemic issue with organisational attention.

They also acknowledge that there will always be people who do not read things.

The poster then lists practical tactics that may help.

#### Visual hierarchy / chunking / F-pattern scanning

Structure messages for scanning, not just reading.

This avoids forcing everyone to read linearly.

Lever: **Friction**

#### Hick's Law / Rule of One

One ask, one decision.

If you want one thing done, ask for one thing.

Lever: **Friction**

#### Pattern interrupt

Pattern interrupt does not have to be a linguistic trick.

It can be anything appropriate that interrupts the pattern of boring corporate updates and makes people actually read.

Lever: **Resonance**

#### Segmentation

If only 40% of staff need a specific piece of information, sending it to everyone trains the other 60% to skim past everything.

Lever: **Personalisation**

#### Lead with “why you specifically”

The first line of any section should answer:

> Why should I care?

before:

> What do I need to do?

Lever: **Resonance + Personalisation**

#### Inverted pyramid / progressive disclosure

Lead with the action. Follow with context.

Make background optional reading for those who need it, not a barrier for those who do not.

Lever: **Friction**

#### Signal intent / effort

Examples include:

- “5 min read”
- “No action required”
- subject tags such as `[FYI]`, `[ACTION]`, `[DECISION]`

Lever: **Friction**

The poster reframes the goal:

> The goal isn't fewer emails. It's less total cognitive load.

### 5.7 Duplicate / noisy source material

The OP response about practical tactics appears twice in the source material.

The “attention debt” definition and rough tool comment also appears twice.

The Diversity Maintainer should recognise this as duplication and avoid treating repeated text as independent support.

### 5.8 Attention debt definition

The original poster says they have started calling the problem **attention debt**.

They define it as:

> The unpaid cognitive load that builds up when it's easy to send and expensive to receive.

They say that until signal-to-noise can be measured properly, subtraction beats addition.

They also mention building a rough tool that scores messages against the four levers and suggests edits.

This tool idea may be relevant to the article, but it should not be overclaimed unless we are actually building or demonstrating such a tool.

### 5.9 Supporting voice — infobesity and trusted channels

Another commenter says this is exactly where their head has been going, particularly after reading about **infobesity**.

They say the job is about preserving the quality and usefulness of trusted channels in an overcrowded space.

They repeat or highlight the attention debt definition.

They also use the phrase:

> Jargon monoxide

This phrase is colourful and memorable.

It may be useful as a private note or possible rhetorical inspiration, but it may be too informal or too loaded for a professional article unless handled carefully.

### 5.10 Supporting voice — legacy perception of comms role

Another commenter says that for them, content creation has been made easier.

They believe the biggest hurdle to adopting a **subtraction** mindset is not the technology, but the legacy perception of the communications role.

They argue that comms needs to move from **Content Producer** to **Noise Reducer**.

They describe three pivots.

#### Pivot 1: From artefacts to outcomes

They say they have received briefs where clients ask for a catchy poster or persuasive email that creates “buzz and excitement.”

When they ask more questions about why the material is needed and what it is meant to achieve, things become confusing.

Many companies still view communications as a designer/content writer shop.

The commenter says comms should stop asking:

> What should the newsletter say?

and start asking:

> What does success look like for this specific business goal?

#### Pivot 2: Systems-thinking as a requirement

Success now requires looking at the environment the message lands in, not just the message itself.

If the system is already flooded, the most valuable communications move might be to cancel the message entirely.

They suggest asking:

- Who are the stakeholders most likely, least likely, and most impacted?
- How would this initiative affect their already busy lives?
- How can they be empowered to handle queries and challenges?
- How can feedback mechanisms show whether the right things are happening?

They also say that coaching clients sometimes becomes important.

#### Pivot 3: Consultative filtering

Comms must work closer with clients to define success before the first draft is written.

The value is no longer in what comms produces. AI can help speed that process.

The value is in what comms prevents to preserve the signal.

If comms does not pivot into a systems-thinking role, it becomes part of the friction in the numerator.

This is a strong practitioner view and should heavily influence the strategy.

### 5.11 Strong practitioner voice — invisible work of killing drafts

Another commenter says they have seen internal comms teams do more damage by adding one more perfectly written update into an already saturated channel than by saying nothing.

They say people are not ignoring messages because they are badly written. They are ignoring them because there are so many, people are busy, and they cannot tell which ones matter.

They say the subtraction point feels right.

The best communications people they know spend a lot of time:

- killing drafts
- merging updates
- saying “this doesn’t need to go out”
- choosing not to polish copy that should not exist

They say this work is invisible to everyone else, but:

> it’s the work.

They also like the idea of designing for permanent overload rather than pretending there is a clean inbox waiting.

They say that is the part most advice skips.

This is one of the strongest source voices.

It has practical texture, lived experience, and a clear articulation of the invisible value of subtraction.

## 6. User interpretation / preferred angle

My interpretation is that this source material is not just about better writing.

It is about a role shift in AI-enabled work:

- from content production to attention management
- from drafting to filtering
- from artefacts to outcomes
- from broadcasting to routing
- from polish to usefulness
- from communication volume to communication value

The article should not be anti-AI.

The point is that AI changes the economics of communication. When creation gets cheap, filtering becomes more valuable.

The practical opportunity is to use AI and better communication discipline to reduce attention debt, not create more polished noise.

The strongest professional phrase is:

> AI has made workplace communication easier to create, but not easier to receive.

The strongest operational phrase is:

> The goal isn't fewer emails. It's less total cognitive load.

The strongest role-shift phrase is:

> We're in the noise reduction business.

The strongest practitioner phrase is:

> Killing drafts is invisible work, but it’s the work.

## 7. Known risks / sensitivities

The downstream article should avoid:

- sounding anti-AI
- sounding like internal communications teams are the problem
- suggesting less communication is always better
- becoming generic “AI is changing work” fluff
- overclaiming that attention debt is an established formal metric
- pretending the ratio is mathematically validated
- copying too much source language verbatim
- using colourful phrases such as “jargon monoxide” in a way that sounds unprofessional
- ignoring the contrarian point that combining messages can make readability worse
- treating repeated source text as separate evidence

## 8. Must-preserve ideas / phrases

The Diversity Maintainer should explicitly evaluate whether these should carry forward:

- “easier to create, but not easier to receive”
- “content production to attention management”
- “noise reduction business”
- “what we prevent, simplify, or kill”
- `(Volume × Friction) ÷ (Resonance × Personalisation)`
- “design for high volume as a permanent condition”
- “attention debt”
- “the unpaid cognitive load that builds up when it's easy to send and expensive to receive”
- “subtraction beats addition”
- “the goal isn't fewer emails; it's less total cognitive load”
- “from artefacts to outcomes”
- “systems-thinking as a requirement”
- “consultative filtering”
- “part of the friction in your numerator”
- “killing drafts”
- “this doesn’t need to go out”
- “invisible work, but it’s the work”
- “designing for permanent overload”
- “jargon monoxide”

## 9. Open questions for the Diversity Maintainer

The Diversity Maintainer should answer:

1. Which source voices are genuinely useful?
2. Which are supporting views?
3. Which are contrarian or challenge views?
4. Which practical tactics should influence the strategy?
5. Which phrases are strong enough to preserve?
6. Which phrases are too risky or informal?
7. Which material is duplicated or noisy?
8. Which tensions should the Strategist carry forward?
9. Does the source support a full article, or only a working hypothesis?
10. What should the Strategist avoid flattening?


---

# Input file: diversity-map.md

<!-- Generated by KevOS Agent Bench on 2026-05-02T17:06:54 -->

# Diversity Map

## Source overview

The source material is a messy but coherent thread-style discussion about how AI changes workplace communication. The central claim is that when AI makes content easier to produce, the scarce resource shifts from production capacity to recipient attention.

The material includes:

- A strong seed thesis from the original poster.
- Several supportive practitioner comments.
- One particularly important challenge about “fewer messages” making things harder to read.
- Practical tactics for reducing cognitive load.
- Useful language around “attention debt,” “noise reduction,” and “killing drafts.”
- Some duplicated material that should not be treated as separate evidence.
- Known sensitivities around not sounding anti-AI, anti-comms, or simplistic about message reduction.

Overall, the source material supports a full article angle, but the article should be framed as a practitioner-informed argument or working model, not as a formally proven theory. The strongest material is grounded in lived experience rather than external research evidence.

## Main thesis

The main thesis is:

> AI has made workplace communication easier to create, but not easier to receive.

Because AI lowers the cost of producing emails, updates, decks, summaries, videos, and other workplace content, the bottleneck has moved. The problem is no longer primarily creation. The problem is attention, relevance, filtering, and cognitive load.

This implies a role shift for communicators and adjacent roles such as project managers, change managers, delivery leads, business analysts, governance leads, and internal comms teams.

The role shift can be summarised as:

- From content production to attention management.
- From drafting to filtering.
- From artefacts to outcomes.
- From broadcasting to routing.
- From polish to usefulness.
- From communication volume to communication value.
- From creating more material to deciding what should be prevented, simplified, killed, routed, or made easier to process.

The strongest operational expression of the thesis is:

> The goal isn't fewer emails. It's less total cognitive load.

This distinction is important. The article should not become a simplistic argument for “send less.” The better argument is “reduce the cognitive cost of the system.”

## Supporting views

### 1. Content audits, content pillars, and HHH framework

A supportive commenter connects the thesis to content audit work. They describe reviewing a large amount of material for archiving and repurposing, and using key content pillars plus the HHH framework:

- Hero
- Hub
- Help

They say this helps balance frequency and impact.

This is useful because it shows the subtraction mindset is not only theoretical. It appears in practical work such as auditing, archiving, repurposing, and deciding what content deserves attention.

The OP’s response adds a useful analytical layer: different frameworks pull different levers.

In this case:

- HHH supports **Resonance**.
- It may indirectly reduce **Volume** by giving teams permission not to publish everything.
- It does not necessarily solve **Friction** or **Personalisation** on its own.

This supports the article’s potential structure: not all communication tactics solve the same problem. Some reduce volume, some reduce effort, some improve relevance, and some increase perceived value.

### 2. Reducing comms sent year on year

Another practitioner says their goal has been to reduce the number of communications sent year on year.

This supports the subtraction idea, but only partially.

It is useful evidence that some practitioners are already trying to manage volume. However, it should be handled carefully because reducing the number of messages is not automatically the same as reducing cognitive load.

This view should influence the article, but it should not become the whole argument.

### 3. Infobesity and trusted channels

A commenter links the discussion to “infobesity” and says the job is about preserving the quality and usefulness of trusted channels in an overcrowded space.

This is a useful supporting view because it reframes the problem beyond individual messages. The issue is also about channel trust. If recipients learn that channels are overloaded, irrelevant, or full of low-value updates, they stop treating those channels as reliable.

The phrase “trusted channels” is strategically useful and professional. It could help the article avoid sounding like it is only about inbox hygiene.

The commenter also uses the phrase:

> Jargon monoxide

This is memorable but risky. See “Distinctive phrases worth preserving” and “Viewpoints to handle carefully.”

### 4. Legacy perception of the comms role

One of the strongest supportive views argues that the main obstacle is not technology, but the legacy perception of communications as a designer/content writer shop.

This commenter says comms needs to move from:

> Content Producer

to:

> Noise Reducer

They describe three pivots:

#### From artefacts to outcomes

This is a highly useful practitioner view. It challenges clients who ask for a poster, email, or “buzz and excitement” before clarifying the business goal.

Useful question to preserve:

> What does success look like for this specific business goal?

This should strongly influence the strategy because it broadens the article beyond writing tips. It makes the argument about business outcomes and role design.

#### Systems-thinking as a requirement

This view says communicators must consider the environment the message lands in, not just the quality of the message.

Useful questions include:

- Who are the stakeholders most likely, least likely, and most impacted?
- How would this initiative affect their already busy lives?
- How can they be empowered to handle queries and challenges?
- How can feedback mechanisms show whether the right things are happening?

This supports the “attention environment” angle and should be preserved.

#### Consultative filtering

This is another strong phrase and idea. It positions communications as an advisory and filtering function before drafting begins.

The commenter’s warning is also strong:

> If comms does not pivot into a systems-thinking role, it becomes part of the friction in the numerator.

This is useful, but the wording may need softening in a professional article. The idea is strong: comms can either reduce friction or become friction.

### 5. Invisible work of killing drafts

This is one of the strongest source voices.

The commenter says internal comms teams can do more damage by adding one more perfectly written update into an already saturated channel than by saying nothing.

They argue people are not ignoring messages only because the messages are badly written. They ignore them because:

- there are too many,
- people are busy,
- they cannot tell which ones matter.

They describe the best communications people as spending time:

- killing drafts,
- merging updates,
- saying “this doesn’t need to go out,”
- choosing not to polish copy that should not exist.

The phrase:

> Killing drafts is invisible work, but it’s the work.

is highly valuable. It is lived-in, specific, and captures the professional value of subtraction.

This should heavily influence the strategy.

## Contrarian or challenge views

### Combining messages can backfire

The strongest contrarian view is the comment asking how to balance readability with decreased frequency.

The commenter says that when their team reduces the number of messages by combining similar things, they receive feedback that staff miss information because the relevant detail was:

> at the bottom of the other email.

This is a strong challenge and should be preserved clearly.

It reveals that “subtraction” can be done badly. If reducing volume means creating longer, mixed-purpose, harder-to-scan messages, then the team may reduce message count while increasing cognitive load.

This challenge prevents the article from flattening into:

> Fewer emails are always better.

The better position is:

> Fewer messages are only better if they reduce total cognitive load and make relevance easier to detect.

This contrarian view should influence both the article and any checklist. The checklist should distinguish between:

- reducing volume,
- combining messages,
- segmenting messages,
- simplifying messages,
- making action clear,
- improving scanability,
- removing unnecessary sends.

The challenge also supports the OP’s reframing:

> The goal isn't fewer emails. It's less total cognitive load.

## Edge cases and trade-offs

### 1. Fewer communications can still create more work

Reducing message count can backfire if messages become:

- longer,
- mixed-purpose,
- poorly structured,
- harder to scan,
- relevant only in parts,
- unclear about who needs to act.

This is the most important trade-off in the source material.

### 2. Merging updates is not always subtraction

Merging updates may reduce volume but increase friction. It can hide important information inside a larger message.

The Strategist should avoid equating “batching” with “better communication.”

### 3. Some people will not read things regardless

The OP acknowledges that there will always be people who do not read communications. This is useful realism.

The article should not imply that better communication design can solve all attention problems. Some non-reading is inevitable.

### 4. Message quality still matters, but it is not enough

The source material does not say writing quality is irrelevant. Rather, it says polished copy can still be harmful if it should not have been sent.

The trade-off:

- Better writing reduces friction.
- Better filtering reduces unnecessary demand.
- Both matter, but filtering becomes more valuable when AI makes writing cheap.

### 5. Personalisation can help, but it can also be operationally hard

Segmentation and personalisation are presented as important levers. However, the source material does not provide much detail on implementation constraints, data quality, channel tooling, governance, or employee privacy.

This should be flagged as an area where more research or internal context may be needed before making strong recommendations.

### 6. The framework is useful, but not mathematically validated

The ratio:

```text
(Volume × Friction) ÷ (Resonance × Personalisation)
```

is useful as a thinking tool, not as proven maths.

The Strategist should preserve it as a heuristic, not present it as a validated model.

### 7. “Attention debt” is a strong concept, but not established evidence here

The phrase and definition are useful:

> The unpaid cognitive load that builds up when it's easy to send and expensive to receive.

But the source does not establish “attention debt” as a formal metric or widely accepted term. It should be presented as a useful working phrase or coined concept, not as an established field term.

### 8. AI is the economic trigger, not the villain

The article should avoid sounding anti-AI. The material supports a more nuanced view:

- AI reduces the cost of creation.
- That creates a risk of more volume.
- The opportunity is to use AI and communication discipline to improve filtering, routing, summarising, and clarity.

## Practical tactics and examples

The source includes a strong set of practical tactics. These should influence the strategy and later checklist.

### 1. Content audits

Useful for identifying what to:

- archive,
- repurpose,
- merge,
- simplify,
- stop producing.

This supports “subtraction” as an operational practice.

### 2. Content pillars

Useful for deciding whether a message fits a strategic priority.

A content pillar approach can give teams permission not to publish everything.

### 3. HHH framework

Hero / Hub / Help can help balance frequency and impact.

The OP’s useful interpretation:

- Hero improves emotional resonance.
- Help improves utility.
- HHH may reduce volume indirectly.

### 4. Lever mapping

The four levers are:

```text
(Volume × Friction) ÷ (Resonance × Personalisation)
```

The strongest use of the model is not the maths. It is asking which lever a tactic pulls.

Examples:

- Reducing sends affects **Volume**.
- Shorter sentences and scanability affect **Friction**.
- Leading with “why this matters” affects **Resonance**.
- Segmentation affects **Personalisation**.

This is a useful diagnostic approach.

### 5. Visual hierarchy, chunking, and F-pattern scanning

Messages should be structured for scanning, not just linear reading.

This reduces friction and helps people find relevant content quickly.

### 6. Hick’s Law / Rule of One

The source phrase is:

> One ask, one decision.

This is highly useful. It can become a checklist item.

If the communication asks for one thing, make the one thing obvious. Avoid multiple competing actions in one message.

### 7. Pattern interrupt

The OP says pattern interrupt does not need to be a gimmicky language trick. It can be anything appropriate that interrupts boring corporate update patterns and makes people actually read.

This is useful, but should be handled carefully. “Pattern interrupt” can become marketing jargon if overused.

### 8. Segmentation

The source gives a clear example:

If only 40% of staff need a specific piece of information, sending it to everyone trains the other 60% to skim past everything.

This is one of the most practical points in the material. It connects over-broadcasting to long-term channel distrust.

### 9. Lead with “why you specifically”

The first line of any section should answer:

> Why should I care?

before:

> What do I need to do?

This is a strong tactic because it combines resonance and personalisation.

### 10. Inverted pyramid / progressive disclosure

Lead with the action. Follow with context.

Make background optional reading for those who need it, not a barrier for those who do not.

This is highly suitable for the checklist.

### 11. Signal intent and effort

Examples:

- “5 min read”
- “No action required”
- `[FYI]`
- `[ACTION]`
- `[DECISION]`

These reduce friction by helping recipients triage.

The Strategist should preserve this as a practical tactic, but may want to add that tags only work if used consistently and honestly. That consistency point is an inference from the tactic, not directly stated in the source.

### 12. Consultative filtering before drafting

Before producing the artefact, clarify:

- What outcome is needed?
- Who needs to know?
- Who needs to act?
- What can be avoided?
- What happens if we do not send this?
- Is communication the right intervention?

This is strongly supported by the practitioner comments.

### 13. Killing drafts

The material strongly supports treating “not sending” as valuable work.

Examples to preserve:

- killing drafts,
- merging updates,
- saying “this doesn’t need to go out,”
- choosing not to polish copy that should not exist.

Important caveat: merging updates can be useful, but the contrarian view shows it can also backfire.

## Distinctive phrases worth preserving

### Strong enough to carry forward

#### “AI has made workplace communication easier to create, but not easier to receive.”

Very strong. This is likely the clearest article hook. It is professional, balanced, and not anti-AI.

#### “Content production to attention management”

Strong. Useful for framing the role shift.

#### “Noise reduction business”

Strong. Memorable and aligned with the source. Should be used carefully so it does not sound dismissive of necessary communication.

#### “What we prevent, simplify, or kill”

Strong. Captures the value of subtraction. “Kill” is slightly forceful but acceptable in a practitioner context.

#### `(Volume × Friction) ÷ (Resonance × Personalisation)`

Useful as a heuristic. Should be explicitly framed as a thinking tool, not validated maths.

#### “Design for high volume as a permanent condition”

Strong. This is one of the most strategically useful ideas because it moves beyond generic “send less” advice.

#### “Attention debt”

Strong concept. Should be framed as a working term or useful label, not an established formal metric.

#### “The unpaid cognitive load that builds up when it's easy to send and expensive to receive.”

Very strong definition. Worth preserving, with caveat that it is a coined/practitioner definition.

#### “Subtraction beats addition”

Memorable, but should be qualified. Subtraction beats addition when the system is overloaded and when subtraction reduces cognitive load.

#### “The goal isn't fewer emails; it's less total cognitive load.”

Very strong. This should be a central corrective in the article.

#### “From artefacts to outcomes”

Strong and professional. Should carry forward.

#### “Systems-thinking as a requirement”

Strong. Useful for the article’s role-shift argument.

#### “Consultative filtering”

Strong. Distinctive and professional. Worth preserving.

#### “Killing drafts”

Strong practitioner language. Useful and vivid.

#### “This doesn’t need to go out”

Very useful. Practical, concrete, and likely relatable.

#### “Invisible work, but it’s the work”

Very strong. It captures the undervalued nature of filtering.

#### “Designing for permanent overload”

Strong. Similar to “design for high volume as a permanent condition.” One of these may be enough in final output.

### Useful but should be handled carefully

#### “Part of the friction in your numerator”

Clever and source-specific, but may be too inside-baseball unless the ratio has already been explained. Could be paraphrased as:

> If comms does not reduce friction, it becomes part of the friction.

#### “Jargon monoxide”

Memorable and colourful, but risky for a professional article. It may sound flippant or too loaded. Better used as private inspiration unless the article has a more informal tone.

#### “Subtraction beats addition”

Good line, but potentially overbroad. Needs context.

#### “Noise reduction business”

Strong, but should not imply that communication itself is noise. The nuance is that comms should protect signal from noise.

### Probably avoid as headline language

#### “Jargon monoxide”

Too informal and potentially derisive for the target audience unless used sparingly and knowingly.

#### Any phrasing that implies “comms teams are the problem”

The source is more nuanced. It says overloaded systems are the problem, and comms can either help reduce load or accidentally add to it.

## Weak, irrelevant, or wrong material

### 1. Duplicated OP practical tactics

The OP response listing practical tactics appears twice in the source material.

This should not be treated as multiple independent confirmations. It is still useful, but it is one source view repeated.

### 2. Duplicated attention debt/tool material

The “attention debt” definition and the rough tool comment appear twice.

Again, this should not be treated as independent support.

### 3. The rough tool idea should not be overclaimed

The OP mentions building a rough tool that scores messages against the four levers and suggests edits.

This is potentially relevant, especially for a future checklist or productised framework. However, there is not enough evidence to claim the tool exists in a mature, validated, or demonstrable form.

Safe treatment:

- Mention as an idea or possible application.
- Do not present as proven.
- Do not imply a working product unless one is actually available.

### 4. The ratio is not evidence

The formula is a useful heuristic, but not a validated measure.

The article should avoid implying that communication effectiveness can literally be calculated using that ratio.

### 5. “Infobesity” may need external context

The term appears in a supporting comment, but the source does not provide detail. If the final article wants to discuss “infobesity” as a research-backed concept, external research would be needed.

### 6. “People have the same 1,500 minutes in a day”

This phrase appears in the seed argument and is rhetorically useful, but the exact number may invite unnecessary scrutiny. It is simply 25 hours, so it may be a mistake or rough phrasing unless there is context not provided.

Safer paraphrase:

> People still have finite working time and finite attention.

### 7. Any universal claim that staff ignore messages only because of volume

The source says volume is a major issue, but also includes friction, resonance, and personalisation. The article should avoid reducing the entire problem to volume alone.

## Viewpoints that should influence the strategy

### 1. AI changes the economics of communication

This should be central. The point is not “AI is bad.” The point is:

> When creation gets cheap, filtering becomes more valuable.

### 2. The receiving environment matters

The article should focus not only on message quality, but on the environment the message lands in:

- crowded inboxes,
- saturated channels,
- low trust,
- competing priorities,
- limited attention,
- unclear relevance.

### 3. The role shift is bigger than writing

The source strongly supports an article about role change, not just writing tips.

The role shift includes:

- attention management,
- consultative filtering,
- systems thinking,
- routing,
- outcome clarification,
- message subtraction.

### 4. Subtraction means reducing cognitive load, not simply reducing sends

This is the key nuance from the contrarian comment.

The Strategist should preserve this tension and make it explicit.

### 5. The invisible work should be made visible

The practitioner voice about killing drafts is powerful. The article should legitimise this work as valuable professional judgement.

### 6. Practical tactics should be included

The source material is strong enough to support a practical checklist.

Most useful tactics:

- clarify the outcome before drafting,
- ask whether the message needs to go out,
- segment the audience,
- lead with relevance,
- use one ask / one decision,
- structure for scanning,
- use progressive disclosure,
- signal intent and effort,
- avoid burying relevant information in bundled updates,
- measure success by reduced cognitive load, not only fewer messages.

### 7. Trusted channels are an asset to protect

The “trusted channels” view should influence the strategy. Communication overload does not only affect one message. It trains people how to treat the channel.

## Viewpoints to handle carefully

### 1. “Reduce the number of communications sent”

Useful but incomplete.

Handle as one lever, not the whole solution.

### 2. “Merging updates”

Merging can be useful, but the source includes a strong warning that it can bury information.

The Strategist should avoid recommending batching or bundling without guardrails.

### 3. “Subtraction beats addition”

Good rhetorical line, but only true when subtraction improves clarity, relevance, or cognitive load.

### 4. “Noise reduction business”

Strong phrase, but should be framed positively. The target audience includes internal comms professionals, so the article should not imply their work is merely cleaning up other people’s mess.

Better framing:

> The strategic value of comms increasingly lies in preserving signal.

### 5. “Attention debt”

Use as a useful working concept, not as a formal metric unless external evidence is added.

### 6. The formula

Useful for explanation, but risky if presented too literally.

Frame it as:

> a practical lens

or:

> a simple way to think about the trade-off.

### 7. “Jargon monoxide”

Memorable but potentially too informal or insulting. Use only if the final tone allows it, and probably not as a main phrase.

### 8. Tooling claims

The rough scoring tool should not become a claim about available capability unless the tool is actually part of the output.

### 9. Blaming recipients

The article should avoid suggesting people are lazy or inattentive. The source’s better explanation is systemic overload.

### 10. Blaming comms teams

The article should avoid suggesting internal comms teams caused the problem. The better frame is that AI and workplace complexity have changed the economics of communication, making filtering more important.

## Recommendations for Strategist

### 1. Preserve the central tension

Do not flatten the article into “AI creates too much content” or “send fewer emails.”

The strongest article tension is:

> AI makes communication easier to produce, while human attention remains expensive to spend.

### 2. Use the role-shift angle as the main article frame

The source supports a full article, not just a checklist, if the article focuses on the professional role shift:

- from content production to attention management,
- from artefacts to outcomes,
- from drafting to filtering,
- from broadcasting to routing,
- from polish to usefulness.

### 3. Make “less total cognitive load” the operational principle

This should be the corrective to simplistic subtraction.

Use the phrase:

> The goal isn't fewer emails. It's less total cognitive load.

Then explain that fewer messages, shorter messages, better segmentation, clearer asks, and better hierarchy are all possible routes to that goal.

### 4. Preserve the contrarian challenge prominently

The article should include the example that combining messages can make people miss relevant information “at the bottom of the other email.”

This is essential because it prevents over-simplification.

Possible strategic lesson:

> Bad subtraction hides the signal. Good subtraction reduces the work required to find it.

### 5. Treat the formula as a heuristic

Use:

```text
(Volume × Friction) ÷ (Resonance × Personalisation)
```

as a practical lens.

Do not claim it is mathematically proven.

Suggested framing:

> The maths is less important than the discipline it creates: look at the environment the message lands in, not just the message itself.

### 6. Use “attention debt” carefully

The term is strong and article-worthy.

Recommended treatment:

> We might call this attention debt: the unpaid cognitive load that builds up when it is easy to send and expensive to receive.

Avoid presenting it as an established formal metric unless external research is added.

### 7. Build the checklist around decision discipline, not writing polish

The message subtraction checklist should include questions such as:

- Does this need to go out?
- Who specifically needs this?
- What action or decision is required?
- What is the cost of making everyone read it?
- Can the audience tell in five seconds whether it applies to them?
- Is the important information buried inside a bundle?
- Are we reducing message count or reducing cognitive load?
- What can be removed, routed, delayed, or made optional?

### 8. Include practical tactics from the OP response

Prioritise these:

- one ask, one decision,
- visual hierarchy and chunking,
- lead with “why you specifically,”
- inverted pyramid / progressive disclosure,
- segmentation,
- signal intent and effort,
- subject tags such as `[FYI]`, `[ACTION]`, `[DECISION]`.

### 9. Make invisible work visible

The practitioner phrase:

> Killing drafts is invisible work, but it’s the work.

should strongly influence the article. It captures the undervalued value of comms judgement in an AI-enabled environment.

This may become a powerful section in the blog article.

### 10. Avoid overclaiming

The Strategist should avoid claiming:

- attention debt is an established metric,
- the formula is validated,
- AI is the sole cause of overload,
- less communication is always better,
- message count reduction equals success,
- merging updates is always good,
- comms teams are responsible for the problem.

### 11. Keep the article pro-AI but pro-discipline

The best stance is:

> AI is useful, but it makes communication discipline more important, not less.

AI can help produce, summarise, segment, and improve messages. But without filtering discipline, it can also create more polished noise.

### 12. Do not discard practitioner texture

The Strategist should preserve the lived-in language around:

- killing drafts,
- “this doesn’t need to go out,”
- saturated channels,
- permanent overload,
- trusted channels,
- preserving signal.

This texture is what prevents the final article from becoming generic “AI is changing work” content.

### 13. Strongest recommended phrases to carry forward

Highest priority:

- “AI has made workplace communication easier to create, but not easier to receive.”
- “The goal isn't fewer emails. It's less total cognitive load.”
- “We're in the noise reduction business.”
- “Killing drafts is invisible work, but it’s the work.”
- “From content production to attention management.”
- “From artefacts to outcomes.”
- “Design for high volume as a permanent condition.”
- “Attention debt.”
- “The unpaid cognitive load that builds up when it's easy to send and expensive to receive.”

Use carefully or sparingly:

- “Subtraction beats addition.”
- “Part of the friction in your numerator.”
- “Jargon monoxide.”

### 14. What the Strategist should avoid flattening

Do not flatten these tensions:

- Fewer messages vs easier-to-process messages.
- AI-enabled production vs human attention limits.
- Better writing vs better filtering.
- Communication as artefact production vs communication as outcome design.
- Merging updates vs burying relevance.
- Individual message quality vs system-level channel trust.
- Content creation speed vs recipient cognitive load.
- Subtraction as “send less” vs subtraction as “reduce total cognitive load.”

The source material is strongest when these tensions remain visible.
--- RUN INPUTS END ---