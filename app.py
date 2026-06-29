from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import uuid

from signals import signal_1, signal_2

app = Flask(__name__)

# ----------------------------
# RATE LIMITER (Milestone 5)
# ----------------------------
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)

# ----------------------------
# IN-MEMORY AUDIT LOG
# ----------------------------
audit_log = []


# ----------------------------
# CONFIDENCE SCORING
# ----------------------------
def compute_confidence(s1, s2):
    return (0.45 * s1) + (0.55 * s2)


def generate_label(confidence):
    if confidence < 0.35:
        return "Likely Human"
    elif confidence < 0.65:
        return "Uncertain"
    else:
        return "Likely AI"


# ----------------------------
# HOME ROUTE
# ----------------------------
@app.route("/")
def home():
    return "Provenance Guard is running"


# ----------------------------
# SUBMISSION ENDPOINT
# ----------------------------
@app.route("/submit", methods=["POST"])
@limiter.limit("10 per minute;100 per day")
def submit():
    data = request.get_json()

    text = data.get("text", "")
    creator_id = data.get("creator_id", "unknown")

    content_id = str(uuid.uuid4())

    # run signals
    s1 = signal_1(text)
    s2 = signal_2(text)

    confidence = compute_confidence(s1, s2)
    label = generate_label(confidence)

    entry = {
        "content_id": content_id,
        "creator_id": creator_id,
        "timestamp": datetime.utcnow().isoformat(),
        "signal_1": s1,
        "signal_2": s2,
        "confidence": confidence,
        "label": label,
        "text": text,
        "status": "classified"
    }

    audit_log.append(entry)

    return jsonify({
        "content_id": content_id,
        "signal_1": s1,
        "signal_2": s2,
        "confidence": confidence,
        "label": label
    })


# ----------------------------
# APPEAL ENDPOINT (Milestone 5)
# ----------------------------
@app.route("/appeal", methods=["POST"])
def appeal():
    data = request.get_json()

    content_id = data.get("content_id")
    reasoning = data.get("creator_reasoning", "")

    for entry in audit_log:
        if entry["content_id"] == content_id:

            entry["status"] = "under_review"
            entry["appeal_reasoning"] = reasoning
            entry["appeal_timestamp"] = datetime.utcnow().isoformat()

            return jsonify({
                "status": "received",
                "content_id": content_id,
                "message": "Appeal submitted successfully"
            })

    return jsonify({
        "status": "error",
        "message": "content_id not found"
    }), 404


# ----------------------------
# LOG ENDPOINT
# ----------------------------
@app.route("/log", methods=["GET"])
def log():
    return jsonify({"entries": audit_log})


# ----------------------------
# RUN SERVER
# ----------------------------
if __name__ == "__main__":
    app.run(debug=False)