def generate_response(prompt):

    text = prompt.lower()

    if "earthquake" in text:
        return """
⚠️ Earthquake Emergency Detected

✅ Safety Instructions:
- Drop, cover, and hold immediately
- Stay away from windows and heavy objects
- Do not use elevators
- Move to open ground after shaking stops
- Expect aftershocks

🚨 Evacuation:
Move away from buildings, electric poles, bridges, and damaged structures.
"""

    elif "flood" in text:
        return """
⚠️ Flood Emergency Detected

✅ Safety Instructions:
- Move to higher ground immediately
- Avoid walking or driving through flood water
- Disconnect electrical appliances
- Carry clean drinking water
- Follow evacuation routes

🚨 Evacuation:
Stay away from rivers, drains, bridges, and submerged roads.
"""

    elif "fire" in text:
        return """
🔥 Fire Emergency Detected

✅ Safety Instructions:
- Evacuate immediately
- Stay low to avoid smoke
- Cover your nose with cloth
- Do not use elevators
- Call fire emergency services

🚨 Evacuation:
Move to an open safe area and do not re-enter the building.
"""

    elif "cyclone" in text:
        return """
🌪️ Cyclone Emergency Detected

✅ Safety Instructions:
- Stay indoors
- Keep away from windows
- Store food and water
- Charge phones and emergency lights
- Follow official warnings

🚨 Evacuation:
Avoid coastal areas and weak structures.
"""

    elif "gas leak" in text:
        return """
☠️ Gas Leak Emergency Detected

✅ Safety Instructions:
- Evacuate immediately
- Do not switch lights or fans on/off
- Cover your nose with wet cloth
- Stay upwind from the leak
- Call emergency services

🚨 Evacuation:
Move away from the leak source as fast as possible.
"""

    else:
        return """
⚠️ Emergency Guidance

✅ Safety Instructions:
- Stay calm
- Move away from danger
- Keep emergency supplies ready
- Follow official instructions
- Contact emergency services if needed

🚨 Evacuation:
Move toward the nearest safe zone.
"""