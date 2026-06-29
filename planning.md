# Provenance Guard — planning.md (Milestone 2)

---

## 1. System Overview

Provenance Guard is a text provenance detection system that analyzes submitted text and assigns a transparency label indicating whether the text is likely human-written or AI-generated. The system combines two independent detection signals, converts them into a calibrated confidence score, and maps that score to a final transparency label.

The system is designed around two primary workflows:

- **Submission Flow:** text is analyzed → signals computed → confidence score generated → label assigned → audit log stored → response returned  
- **Appeal Flow:** user challenges result → system retrieves audit log → re-evaluates signals → updates label/status → logs changes → response returned  

---

## 2. Detection Signals

### Signal 1: Linguistic Consistency / Structural Entropy

**What it measures:**
- Sentence structure uniformity
- Repetition patterns
- Token predictability / entropy approximation
- Variation in sentence length

**Output:**
- `signal_1_score ∈ [0, 1]`
- 0 = highly human-like variability  
- 1 = highly AI-like structural consistency  

**Why it works:**
- AI-generated text tends to be smoother, more uniform, and statistically consistent
- Human writing tends to include irregular structure, variation, and noise

**Blind spots:**
- Highly edited human writing (essays, academic writing) can appear AI-like  
- Very short text samples are unreliable  
- Advanced AI models can intentionally inject randomness  

---

### Signal 2: Semantic Embedding Similarity

**What it measures:**
- Semantic similarity of text using embedding models
- Distance from human vs AI-like embedding distributions

**Output:**
- `signal_2_score ∈ [0, 1]`
- 0 = semantically human-like distribution  
- 1 = semantically AI-like clustering  

**Why it works:**
- AI-generated text tends to cluster in embedding space due to model priors
- Human writing shows higher semantic diversity and irregularity

**Blind spots:**
- Domain-specific writing (legal, technical, academic) may mimic AI clustering  
- Embedding drift if model changes over time  
- Requires representative dataset for calibration  

---

## 3. Confidence Scoring & Uncertainty Representation

### Signal Combination Formula

Final confidence score:
confidence = (0.45 * signal_1_score) + (0.55 * signal_2_score)



### Confidence Interpretation

- **0.00 – 0.35 → High Confidence Human**
- **0.35 – 0.65 → Uncertain Authorship**
- **0.65 – 1.00 → High Confidence AI Generated**

### Meaning of Confidence Score

- A score of **0.60** means:
  - Mixed evidence from both signals
  - Slight bias toward AI-like characteristics
  - Not reliable enough for strong classification
  - Requires uncertainty-aware labeling

---

## 4. Transparency Label Design

The system returns one of three fixed labels:

### High Confidence AI Result
"High Confidence: AI-Generated Content Detected"

### High Confidence Human Result
"High Confidence: Human-Written Content"

### Uncertain Result
"Uncertain Authorship: Mixed Signal Detected"



Each label is accompanied by:
- confidence score
- brief explanation summary
- contributing signal breakdown

---

## 5. False Positive Handling

### Scenario: Human writing flagged as AI

**Flow:**
1. Signal 1 + Signal 2 both produce high AI-like scores  
2. Confidence engine outputs high score (e.g., 0.80)  
3. System assigns "High Confidence AI" label  

### Risk:
- Legitimate human writing misclassified as AI-generated

### Mitigation:
- System always exposes confidence score (never binary truth)
- Labels explicitly include uncertainty context
- Appeals allow reprocessing with adjusted signal weights
- Audit logs preserve full traceability of decision path  

---

## 6. Appeals Workflow

### Who can appeal:
- Only the original submitter of the text

### Request format:
POST /appeal
{
"submission_id": "...",
"reason": "string explanation"
}


### System behavior:
1. Mark submission status → `under_review`
2. Retrieve original audit log + signals
3. Recompute confidence (optionally adjusted weights)
4. Update label if needed
5. Log all changes in audit trail
6. Return updated status to user

### Reviewer perspective (future system view):
- original text
- signal breakdown
- original vs updated score
- change history
- appeal reason

---

## 7. Edge Cases

### Edge Case 1: Poetic / Repetitive Human Writing
- Poetry with repetition and simple vocabulary may score as AI-generated due to high structural consistency

### Edge Case 2: Formal Academic or Legal Text
- Highly structured, low-variance writing may resemble AI output in both signals

### Edge Case 3: Extremely Short Text Inputs
- Inputs like "Yes", "No", or single sentences produce unreliable signal outputs due to insufficient data

---

## 8. API Design

### POST /submit
Request:
{
"text": "string"
}

Response:
{
"submission_id": "string",
"label": "High Confidence: Human-Written Content | Uncertain Authorship | High Confidence: AI-Generated Content Detected",
"confidence": 0.0,
"explanation": "string"
}


---

### POST /appeal

Request:
{
"submission_id": "string",
"reason": "string"
}


Response:
{
"status": "received | under_review | updated",
"updated_label": "string (optional)"
}


---

### GET /submission/{id}
Response:
{
"text": "string",
"signals": {
"signal_1_score": 0.0,
"signal_2_score": 0.0
},
"confidence": 0.0,
"label": "string",
"audit_log": []
}



---

## 9. Architecture

### Submission Flow

User Input  
→ POST /submit  
→ Validation Layer  
→ Signal 1: Linguistic Consistency  
→ Signal 2: Embedding Similarity  
→ Confidence Scoring Engine  
→ Label Generator  
→ Audit Log Storage  
→ API Response  

---

### Appeal Flow

User Appeal  
→ POST /appeal  
→ Fetch Audit Log  
→ Recompute Signal Scores  
→ Adjust Confidence Score  
→ Update Label  
→ Update Audit Log  
→ Response Returned  

---

### Narrative (2–3 sentences)

A submitted text is independently analyzed by two signals measuring structural and semantic properties. These signals are combined into a weighted confidence score that determines a transparency label. Appeals allow re-evaluation of prior decisions while preserving full audit history for traceability.

---

## 10. AI Tool Plan

### Milestone 3 (Submission Endpoint + Signal 1)

**Provide to AI tool:**
- Detection signals section
- Architecture section

**Ask AI to generate:**
- Flask/FastAPI server skeleton
- `/submit` endpoint
- Signal 1 implementation function

**Verification:**
- Test Signal 1 on:
  - human paragraph
  - AI-generated paragraph
- Ensure score changes meaningfully

---

### Milestone 4 (Signal 2 + Confidence Engine)

**Provide to AI tool:**
- Detection signals
- Confidence scoring section
- Architecture section

**Ask AI to generate:**
- Embedding-based Signal 2 function
- Confidence scoring function
- Threshold-based label mapping

**Verification:**
- Human vs AI text produces different scores
- Confidence varies across uncertainty range (not binary)

---

### Milestone 5 (Production Layer)

**Provide to AI tool:**
- Label design section
- Appeals workflow section
- Architecture section

**Ask AI to generate:**
- Final label generator
- `/appeal` endpoint logic
- Audit log update system

**Verification:**
- All three label states reachable
- Appeal updates stored state correctly
- Audit log reflects changes

---

## END OF SPEC