import warnings
import os
import re
from pathlib import Path
from dataclasses import dataclass

warnings.filterwarnings("ignore")


tts = None

os.environ["COQUI_TOS_AGREED"] = "1"


@dataclass
class Line:
    speaker: str
    content: str
    outputfile: str
    voice_actor: str
    mood: str


@dataclass
class Scene:
    number: int
    lines: list[Line]


@dataclass
class Script:
    title: str
    scenes: list[Scene]

    def lines(self):
        for scene in self.scenes:
            for line in scene.lines:
                yield line


def load_tts(model="tts_models/multilingual/multi-dataset/xtts_v2", device="cpu"):
    global tts

    if tts is not None:
        return tts

    from TTS.api import TTS
    import torch

    tts = TTS(model)
    # tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

    if device == "cuda" and torch.cuda.is_available():
        print("Using CUDA")
        tts = tts.to("cuda")
    elif device == "mps" and torch.backends.mps.is_available():
        print("Using MPS")
        tts = tts.to("mps")
    else:
        print("Using CPU")

    return tts


def test_generate():
    load_tts()
    # tts.tts_with_vc_to_file(
    #     "La la la I am michael lavine, a real human being.",
    #     speaker_wav="tests/voices/michael_default.m4a",
    #     file_path="output.wav",
    # )
    voice_path = os.path.abspath("tests/voices/Tega/Tega.wav")

    tts.tts_to_file(
        text="My name is Tega. I am a robot.",
        file_path="output4.wav",
        speaker_wav=voice_path,
        # language="en",
        # voice_dir="tests/voices/",
        # speaker="Mal",
    )


def generate(text: str, source: str, output: str = "output.wav"):
    try:
        tts.tts_to_file(text=text, file_path=output, speaker_wav=source, language="en")
    except Exception:
        tts.tts_to_file(text=text, file_path=output, speaker_wav=source)


def generate_from_script(script_content: str, voices: str, output: str):
    script = parse_script(script_content)
    Path(output).mkdir(parents=True, exist_ok=True)
    for scene in script.scenes:
        scene_dir = os.path.join(output, f"scene_{scene.number:02}")
        Path(scene_dir).mkdir(parents=True, exist_ok=True)
        for index, line in enumerate(scene.lines):
            dest_filename = os.path.join(
                scene_dir, f"scene_{scene.number:02}_{index:04}.wav"
            )
            source_filename = os.path.join(voices, f"{line.speaker}.wav")
            if line.mood != "default":
                source_filename = os.path.join(
                    voices, f"{line.speaker}_{line.mood}.wav"
                )
            if not os.path.exists(source_filename):
                print(f"Voice file not found: {source_filename}")
                continue
            # print(source_filename, dest_filename)
            generate(line.content, source_filename, dest_filename)


def parse_script(content: str) -> Script:
    scenes = []
    scene_number = 0

    lines = content.split("\n")
    title = "untitled"

    for line in lines:
        line = line.strip()

        if re.search(r"^## ?scene", line.lower()):
            scene_number += 1
            scene = Scene(number=scene_number, lines=[])
            scenes.append(scene)
            continue

        if re.search(r"^###", line):
            line = line.replace("#", "")
            speaker_parts = line.split(":")
            speaker = speaker_parts[0].strip()
            try:
                mood = speaker_parts[1].strip()
            except Exception:
                mood = "default"

            speaker_line = Line(
                speaker=speaker,
                mood=mood,
                content="",
                outputfile="",
                voice_actor="",
            )
            scenes[-1].lines.append(speaker_line)
            continue

        if len(scenes) > 0 and len(scenes[-1].lines) > 0:
            scenes[-1].lines[-1].content += line

    return Script(title=title, scenes=scenes)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Voice Puppet")

    parser.add_argument(
        "--script", "-s", type=argparse.FileType("r"), help="Path to script file"
    )

    parser.add_argument(
        "--voices", "-v", type=str, default="voices/", help="Path to voices folder"
    )

    parser.add_argument(
        "--output", "-o", type=str, help="Path to output folder or file"
    )

    parser.add_argument(
        "--device", "-d", type=str, help="Device to use (cpu, cuda, mps)", default="cpu"
    )

    parser.add_argument(
        "--model",
        "-m",
        type=str,
        help="TTS model",
        default="tts_models/multilingual/multi-dataset/xtts_v2",
    )

    parser.add_argument(
        "--clone", "-c", type=str, help="Speaker to clone, if not using script"
    )

    parser.add_argument(
        "--text", "-t", type=str, help="Text to use, if not using script"
    )

    args = parser.parse_args()

    if args.clone and args.text:
        load_tts(model=args.model, device=args.device)
        output_name = args.output or "cloned.wav"
        generate(text=args.text, source=args.clone, output=output_name)

    elif args.script:
        load_tts(model=args.model, device=args.device)
        output_name = args.output or "output/"
        generate_from_script(args.script.read(), args.voices, output_name)

    else:
        print("Please provide a script or text to generate audio from.")
