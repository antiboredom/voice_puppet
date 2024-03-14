from voice_puppet import parse_script

test_script = """
# Title

## Scene 1

### RONALD: excited
It’s going to be incredible! We’re going to make so many people happy!

### DEBORAH
Sure I can get on board with that. When should we start?


##Scene 2

### RONALD:sad

What is happening?

### SAM: happy
what is life.
why is life?
"""


def test_parse_script():
    script = parse_script(test_script)
    assert len(script.scenes) == 2
    assert len(list(script.lines())) == 4

    assert script.scenes[0].lines[0].speaker == "RONALD"
    assert script.scenes[0].lines[0].mood == "excited"
    assert (
        script.scenes[0].lines[0].content
        == "It’s going to be incredible! We’re going to make so many people happy!"
    )

    assert script.scenes[0].lines[1].speaker == "DEBORAH"
    assert script.scenes[0].lines[1].mood == "default"

    assert script.scenes[1].lines[1].content == "what is life.why is life?"
