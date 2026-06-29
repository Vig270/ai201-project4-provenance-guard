# ai201-project4-provenance-guard

Project Overview

Provenance Guard is a lightweight text attribution system that classifies submitted text as likely human-written or AI-generated. It uses a multi-signal detection pipeline to compute a confidence score and assigns a transparency label based on that score.

The system also supports:

  - structured audit logging
  - an appeals workflow for users
  - rate limiting to prevent abuse

The goal of this project is to demonstrate how multiple weak signals can be combined into a simple but interpretable classification system.



System Architecture

The system consists of four main components:

    - Flask API server
    - Multi-signal detection pipeline
    - Confidence scoring + labeling system
    - In-memory audit log with appeal support

Flow:
User Input → /submit → Signal 1 + Signal 2 → Confidence Score → Label → Audit Log
                                                   ↓
                                             /appeal updates entry



Detection Signals
Signal 1: Lexical Uniformity Signal

This signal measures the average word length in the input text.

  - Higher average word length → more structured / formal writing
  - Normalized into a 0–1 score
  - Captures stylistic uniformity often seen in AI-generated text

Limitation:
It cannot understand meaning or context, and may misclassify formal human writing as AI-generated.

Signal 2: Sentence Structure Variance Signal

This signal measures variance in sentence lengths.

  - Low variance → more uniform structure (often AI-like)
  - High variance → more natural human variation
  - Uses statistical dispersion of sentence token counts

Limitation:
Formal academic writing often has low variance, which can falsely increase AI likelihood


Confidence Scoring

The final confidence score is computed using a weighted combination:
confidence = 0.45 * signal_1 + 0.55 * signal_2


Why this design?
  - Signal 2 is slightly more important because sentence structure provides stronger stylistic signals than word length alone.
  - The weighting balances lexical and structural patterns.

Interpretation:
    - 0.0 – 0.35 → Likely Human
    - 0.35 – 0.65 → Uncertain
    - 0.65 – 1.0 → Likely AI


Example Results
Example 1 — High AI Confidence

Input:
Formal structured paragraph (AI-like text)

Output:
signal_1: 0.357
signal_2: 1.0
confidence: 0.7107
label: Likely AI


This result is high because:

  - sentence structure is extremely uniform
  - lexical features are consistent


Example 2 — Lower Confidence Case

Input:
Mixed or less structured writing

Output:
signal_1: 0.42
signal_2: 0.48
confidence: 0.46
label: Uncertain


This falls into the uncertain range because:

  - signals disagree moderately
  - writing style is mixed




Transparency Labels

The system uses three user-facing transparency labels:

🟢 Likely Human

“This writing appears informal, irregular, and stylistically varied. It is likely written by a human author.”

🟡 Uncertain

“The system cannot confidently determine whether this text was written by a human or AI due to mixed writing signals.”

🔴 Likely AI

“This text appears highly structured and consistent, which is commonly seen in AI-generated writing.”



Thus these labels are intentionally:

    - plain language
    - non-technical
    - designed for general users


Known Limitations

This system may misclassify:

Formal academic writing

Because:

  - structured sentences resemble AI output
  - low variance increases AI-like scoring

This shows a key limitation are stylistic signals alone cannot distinguish “formal human writing” from AI-generated text.





Spec Reflection
What the spec helped with:

The specification defined:

    - a multi-signal architecture
    - a 3-tier confidence labeling system
    - an audit log requirement

This helped structure the system into clear, modular components.

What I changed during implementation:

During testing, I adjusted signal weighting because Signal 2 initially dominated confidence scores too strongly, leading to overconfident classifications.





AI Usage
Example 1 — Detection Signal Design
  - Prompt: “Generate a second stylometric detection signal”
  - AI output: sentence-length variance heuristic
  - My modification: normalized output to ensure score stays in [0,1] range

Example 2 — Appeals Endpoint
  - Prompt: “Create Flask endpoint for content appeals”
  - AI output: basic POST route structure
  - My modification:
    - added audit log updates
    - added status tracking (under_review)
    - ensured entry lookup by content_id

Example 3 — Confidence Scoring Logic
  - Prompt: “Combine two signals into weighted confidence score”
  - AI output: simple averaging
  - My modification: introduced weighted scoring (0.45 / 0.55 split) for better signal balance




Audit Log Evidence

Example /log output:

{
  "entries": [
    {
      "content_id": "c1e421ed-e1cb-41d6-a294-0562386f249b",
      "confidence": 0.7107,
      "label": "Likely AI",
      "signal_1": 0.357,
      "signal_2": 1.0,
      "status": "under_review",
      "appeal_reasoning": "I wrote this myself",
      "timestamp": "2026-06-27T18:08:36"
    }
  ]
}


Rate Limiting Evidence

The system uses:
@limiter.limit("10 per minute;100 per day")


When exceeded:
429 Too Many Requests
10 per 1 minute


This prevents abuse while allowing normal usage patterns.

Portfolio Walkthrough (Suggested Script)
  - Open /submit and show a request
  - Show returned confidence + label
  - Open /log and explain audit trail
  - Show /appeal updating an entry
  - Mention signal design and weighting





General Summary

Provenance Guard demonstrates:

  - multi-signal classification
  - interpretable confidence scoring
  - user-facing transparency labels
  - appeal-based correction flow
  - structured audit logging
  - rate-limited API protection

