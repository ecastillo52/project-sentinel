Post-Audit Cleanup |

☐ Remove core/sensors.py after all imports point to core/engine/sensors.py. 

☐ Remove backwards-compatibility wrappers in core/engine/scanner.py if they're no longer needed.

☐ Replace SessionDatabase.contains_hash() with find_by_hash().

☐ Consolidate duplicated historical sensor lookup helpers.

☐ Replace dictionary-based historical reports with typed domain models.

☐ Consider making health thresholds configuration-driven.

☐ Evaluate making Report immutable after construction.

| Item                                            | Status        | Notes                                                                                                                   |
| ----------------------------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Remove legacy `core/sensors.py` after migration | 🚩 Post-Audit | The new `core/engine/sensors.py` is the architectural owner. Delete the legacy registry once all imports have migrated. |

Small cleanup list after the audit

These are the only things I'd put on the post-audit list.

1. Empty presentation package
core/presentation/

It's empty.

Either:

remove it

or

move renderers there in the future.

Right now it's just dead structure.

2. models/game.py

Exactly as you said:

future dreams :'(

😂

I'd leave it.

Having

Game
Session
Report
Sensor

as the eventual domain model is actually a nice design.

3. Visualization
visualization/
    charts.py
    html.py

Not yet audited.

We'll review those when you send them.

4. metadata/hashing.py vs utils/hash.py

This one jumped out immediately.

You currently have

core/
    metadata/
        hashing.py

    utils/
        hash.py

I would expect only one hashing utility.

We'll need to see both files.

One of them is almost certainly legacy.

5. Game Detector

I still think this is the only module that is doing a little too much.

It currently owns:

alias persistence
JSON storage
detection
learning
user prompting

Architecturally it isn't wrong—it's only about 150 lines—but eventually I could see it evolving into:

metadata/
    alias_store.py
    detector.py
    game_detector.py   (facade)