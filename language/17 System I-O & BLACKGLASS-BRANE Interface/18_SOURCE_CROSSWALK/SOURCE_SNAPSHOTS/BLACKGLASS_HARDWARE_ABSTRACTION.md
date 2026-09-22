# Hardware-Abstraction Contract

Bodies expose capabilities rather than identity-specific hardware assumptions.

Examples:

```text
vision.capture
hearing.capture
speech.output
pose.read
translate.request
rotate.request
hold_position.request
manipulator.pose
manipulator.grip
proximity.read
touch.read
battery.read
thermal.read
```

A locomotion backend may be legs today and a different actuator architecture later. Hangar cognition issues typed capability intents; local body controllers compile them to hardware-specific actions.
