import time

import httpcore
import httpx
import ollama

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
    print(f"Downloading {llama!r}")
    ollama.pull(llama)

CLIENT = ollama.Client()


def request():
    while True:
        if prompt := input("Enter the prompt > "):
            prompt += " (keep your response short)"
            start = time.time()
            for idx, res in enumerate(CLIENT.generate(model=llama, prompt=prompt, stream=True,
                                                      options=ollama.Options(num_predict=100))):
                if idx == 0:
                    print(f"\nGenerator started in {round(float(time.time() - start), 2)}s\n")
                print(res['response'], end='', flush=True)
                if res['done']:
                    break
            print(f"\nGenerator completed in {round(float(time.time() - start), 2)}s\n\n")
        else:
            print("Prompt is mandatory")


if __name__ == '__main__':
    request()
