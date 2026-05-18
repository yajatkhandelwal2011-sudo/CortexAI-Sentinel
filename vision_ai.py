from transformers import pipeline
from PIL import Image

# -----------------------------------
# LOAD IMAGE CLASSIFIER
# -----------------------------------
classifier = pipeline(
    "image-classification",
    model="google/vit-base-patch16-224"
)

# -----------------------------------
# ANALYZE IMAGE
# -----------------------------------
def analyze_disaster_image(image):

    results = classifier(image)

    top_result = results[0]

    label = top_result['label'].lower()

    score = round(top_result['score'] * 100, 2)

    # -----------------------------------
    # FLOOD
    # -----------------------------------
    if "water" in label or "ocean" in label or "river" in label:

        return f"""
⚠️ Flood or Water Disaster Detected

🧠 AI Confidence: {score}%

✅ Safety Instructions:
- Move to higher ground
- Avoid flood water
- Disconnect electricity
- Follow evacuation routes
"""

    # -----------------------------------
    # FIRE
    # -----------------------------------
    elif "fire" in label or "smoke" in label:

        return f"""
🔥 Fire Hazard Detected

🧠 AI Confidence: {score}%

✅ Safety Instructions:
- Evacuate immediately
- Avoid smoke inhalation
- Use stairs instead of elevators
- Contact emergency services
"""

    # -----------------------------------
    # BUILDING DAMAGE
    # -----------------------------------
    elif "building" in label or "house" in label:

        return f"""
🏚️ Structural Damage Possible

🧠 AI Confidence: {score}%

✅ Safety Instructions:
- Avoid unstable structures
- Move to open areas
- Watch for falling debris
- Await rescue instructions
"""

    # -----------------------------------
    # DEFAULT
    # -----------------------------------
    else:

        return f"""
🧠 Object Detected: {top_result['label']}

AI Confidence: {score}%

⚠️ No major disaster detected.

✅ General Safety:
- Stay alert
- Follow emergency updates
- Keep supplies ready
"""