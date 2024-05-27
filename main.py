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

llama = "llama2"  # specify llama version here, llama2 is available by default in ollama
for model in models:
    if model.get("name") == f"{llama}:latest":
        print(f"Model {llama!r} found")
        break
else:
    # Run manually: ollama run llama2
    print(f"Downloading {llama!r}")
    ollama.pull(llama)

CLIENT = ollama.Client()

ins = "(keep your response as short as possible, use commas and full stops but don't use emojis or other punctuations)"


def request(speak: bool = False):
    while True:
        if prompt := input("Enter the prompt > "):
            prompt += f" {ins}"
            start = time.time()
            response = []
            for idx, res in enumerate(CLIENT.generate(model=llama, prompt=prompt, stream=True,
                                                      options=ollama.Options(num_predict=100))):
                if idx == 0:
                    print(f"Generator started in {round(float(time.time() - start), 2)}s")
                if speak:
                    response.append(res['response'])
                else:
                    print(res['response'], end='', flush=True)
                if res['done']:
                    break
            print(f"Generator completed in {round(float(time.time() - start), 2)}s\n\n")
            if speak:
                text = ''.join(response)
                print(text)
                audio.speaker(text)
        else:
            print("Prompt is mandatory")


if __name__ == '__main__':
    request(speak=True)
