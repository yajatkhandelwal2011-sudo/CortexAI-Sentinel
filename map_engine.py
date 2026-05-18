import folium

def create_map(user_input=None):
    # Default location (you can change later)
    base_location = [28.6139, 77.2090]  # Delhi

    m = folium.Map(location=base_location, zoom_start=13)

    # 🟥 Danger Zone
    folium.Marker(
        [28.6100, 77.2000],
        popup="⚠️ Flood Area",
        icon=folium.Icon(color="red")
    ).add_to(m)

    # 🟩 Safe Zone (Higher Ground)
    folium.Marker(
        [28.6300, 77.2200],
        popup="✅ Safe Zone (Higher Ground)",
        icon=folium.Icon(color="green")
    ).add_to(m)

    # 🧠 AI-Based Direction Line
    if user_input and "where should i go" in user_input.lower():
        folium.PolyLine(
            locations=[
                [28.6100, 77.2000],  # danger
                [28.6300, 77.2200]   # safe
            ],
            color="blue",
            weight=5
        ).add_to(m)

    return m