import os
import json

from blizzard import BlizzardTools

if __name__ == "__main__":
    auth_data = {"client_id": os.environ.get("BLIZZARD_CLIENT_ID"),
                 "client_secret": os.environ.get("BLIZZARD_CLIENT_SECRET")}

blizztools = BlizzardTools(auth_data)
# print(blizztools.get_character_profile(realm="sunstrider", char_name="karmik"))
print(json.dumps(blizztools.get_guild_roster(realm="boulderfist", guild_name="limited-edition")))
