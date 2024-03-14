# voice-puppet

Command line tool to clone voice with TTS. Can be used for individual lines or fed a script file.

## Basic usage:

```bash
voice_puppet --clone AUDIOFILETOCLONE.wav --text "Text to say." --output "cloned.wav"
```

## Usage with a script file

You can also provide a script file and a folder with voices to clone.

```bash
voice_puppet --script SCRIPTFILE.txt --voices FOLDERWITHVOICES --output OUTPUTDIRECTORY
```

The script file should follow this format:

```
## Scene 1

### Karl
A spectre is haunting this script.

### Fred
The spectre of voice cloning.


## Scene 2

### Karl: excited
So many spectres!

```

A folder will be created for each scene, and indidual wav files for each line of dialog.

Scene names are preceded by 2 hashes `##`.

Lines of dialog are preceded by 3 hashes `###`, followed by a voice file to use as the source of the clone, and optionally followed by a colon and a mood.

You must provide a folder with wav files for each voice that matches the names you put in the script. So if you write "Karl" in the script, there should be a file called `Karl.wav` in a `voices` directory (or another directory name that you can specify).

If you optionally provide a mood with a character name, you should provide another voice file, in the format `Character_mood.wav`.
