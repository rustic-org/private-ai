from collections.abc import Generator

import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()
for voice in list(engine.getProperty("voices")):
    if voice.name == "Daniel":
        engine.setProperty("voice", voice.id)


def stream_text_to_speech(generative: Generator[str]):
    for text in generative:
        engine.say(text)
        engine.runAndWait()


def speaker(text: str):
    engine.say(text)
    engine.runAndWait()
