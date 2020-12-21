# raidnight
a Flask web service that connects to Blizzard's WoW Profile API, fetches a guild roster and output a simplified json blob with a list of members, each row being a collection of key facts. Spawned from the Officer Team of EU-Boulderfist's "Limited Edition" Guild.

# Basic Architecture
In its current form, intended to be used as a publicly reachable web service, exposing a REST endpoint (with basic authentication). Placing a HTTP GET to /rostermanager/<realm>/<guild> on the endpoint will yield a JSON list-of-collections.
  
In turn, it is used as the datasource for a Google Sheets through bradjasper's [ImportJSON](https://github.com/bradjasper/ImportJSON) custom script, as that's the user interface the Officer team is (so far) accustomed to.

Data flow is roughly like this:

[Profile API]--[Blizzard Developer Account]--[raidnight account on Blizzard Developer Portal]--[raidnight EB deployment]--[AWS Elastic Beanstalk]--[Google Sheets]--[ImportJSON]--[Guild Raid Attendance Sheet]

# Features
- Basic Authentication
- Select only certain ranks (ie: only people promoted to Raiders rank)
- Decoupled Blizzard API Client Library
- All secrets are ENV vars that can be passed in a cloud deployment system

# TODO
Check [Issues](https://github.com/itsgc/raidnight/issues) for details but roughly
- Include support for Discord so we can check if members have signed up to Guild's Discord
- Track sign ups to Guild Events in-game (this is currently not in-scope for Blizzard's REST API footprint so we'll have to think of an alternative)
- Import Guild Notes (also currently not in Blizzard's own API)
- Automated attendance confirmation, as LE requires members to confirm their attendance a couple days prior to raid night.
