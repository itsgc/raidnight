import os
import json

from blizzard import BlizzardTools

if __name__ == "__main__":
    auth_data = {"client_id": os.environ.get("BLIZZARD_CLIENT_ID"),
                 "client_secret": os.environ.get("BLIZZARD_CLIENT_SECRET")}

blizztools = BlizzardTools(auth_data)
# print(blizztools.get_character_profile(realm="sunstrider", char_name="karmik"))
guild_roster = blizztools.get_guild_roster(realm="boulderfist", guild_name="limited-edition")
members = guild_roster["members"]

ranks = {0: "Guild Master",
         1: "Officer",
         2: "Officer Alt",
         3: "Raider",
         4: "Veteran",
         5: "Member",
         6: "Alt",
         7: "Initiate"
         }
for member in members:
    rank = member["rank"]
    char_name = member["character"]["name"].lower()
    realm = member["character"]["realm"]["slug"]
    if rank in [0, 1, 3]:
        profile = blizztools.get_character_profile(realm, char_name)
        player_class = profile["character_class"]["name"]
        player_spec = profile["active_spec"]["name"]
        ilvl = profile["average_item_level"]
        memberdetails = {"ilvl": ilvl,
                         "name": char_name,
                         "realm": realm,
                         "class": player_class,
                         "spec": player_spec,
                         "role": ranks[rank]}
        print(json.dumps(memberdetails, ensure_ascii=False))
