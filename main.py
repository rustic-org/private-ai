import os
import subprocess
import time

import httpcore
import httpx
import ollama

import audio

try:
    models = ollama.list().get('models', [])
except (httpcore.ConnectError, httpx.ConnectError) as error:
    raise RuntimeError(
        "\n\tMake sure llama is installed, refer: https://ollama.com/download"
    )

llama = "llama3"
model_name = "mario"
for model in models:
    if model.get("name") == f"{llama}:latest":
        print(f"Model {llama!r} found")
        break
else:
    print(f"Downloading {llama!r}")
    ollama.pull(llama)

try:
    model_file = os.path.join(os.path.dirname(__file__), "Modelfile")
    assert os.path.isfile(model_file)
    response = ollama.create(
        model="mario",
        modelfile=model_file,
        stream=False
    )
    print(response)
except ollama.ResponseError:
    model_file = "Modelfile"
    assert os.path.isfile(model_file)
    process = subprocess.Popen(
        f"ollama create {model_name} -f {model_file}",
        shell=True,
        universal_newlines=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    for line in process.stdout:
        print(line.strip())
    process.wait()
    for line in process.stderr:
        print(line.strip())
    assert process.returncode == 0, "Failed to customize the model"

CLIENT = ollama.Client()


def request(speak: bool = False):
    while True:
        if prompt := input("Enter the prompt > "):
            start = time.time()
            model_response = []
            for idx, res in enumerate(CLIENT.generate(model=model_name, prompt=prompt, stream=True,
                                                      options=ollama.Options(num_predict=100))):
                if idx == 0:
                    print(f"Generator started in {round(float(time.time() - start), 2)}s")
                if speak:
                    model_response.append(res['response'])
                else:
                    print(res['response'], end='', flush=True)
                if res['done']:
                    break
            print(f"Generator completed in {round(float(time.time() - start), 2)}s\n\n")
            if speak:
                text = ''.join(model_response)
                print(text)
                audio.speaker(text)
        else:
            print("Prompt is mandatory")


if __name__ == '__main__':
    request(speak=False)
