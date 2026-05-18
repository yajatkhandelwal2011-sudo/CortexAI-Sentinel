import json
import os
from datetime import datetime

FILE_NAME = "mesh_messages.json"

# Create file if not exists
if not os.path.exists(FILE_NAME):

    with open(FILE_NAME, "w") as f:

        json.dump([], f)

# -----------------------------------
# SAVE MESSAGE
# -----------------------------------
def broadcast_message(message):

    with open(FILE_NAME, "r") as f:

        data = json.load(f)

    data.append({
        "time": str(datetime.now()),
        "message": message
    })

    with open(FILE_NAME, "w") as f:

        json.dump(data, f, indent=4)

# -----------------------------------
# LOAD MESSAGES
# -----------------------------------
def get_messages():

    with open(FILE_NAME, "r") as f:

        data = json.load(f)

    return data[::-1]