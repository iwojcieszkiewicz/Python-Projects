from openai import OpenAI
import whisper

class App:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key="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",
        )
        self.main()

    def get_trancription(self, path):
        model = whisper.load_model("turbo")
        return model.transcribe(path, fp16=False)

    def text_summaries(self, path):

        result = self.get_trancription(path)
        summaries = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f"Summaries text {result['text']}"
                }
            ]
        )

        return {'Summary': summaries.choices[0].message.content}

    def main(self):
        path = input("Podaj ścieżke do pliku audio: ")
        print(self.text_summaries(path))

app = App()
