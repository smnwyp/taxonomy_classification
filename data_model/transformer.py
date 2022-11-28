import requests

class Transformer:
    def __init__(self):
        self.url = 'https://api-inference.huggingface.co/models/erst/xlm-roberta-base-finetuned-nace'

    @staticmethod
    def filter_nacecode(preds: list[dict])->list[dict]:
        return Transformer.filter_top1(preds=preds)

    @staticmethod
    def filter_top1(preds: list[dict]) -> list[dict]:
        if preds:
            return [preds[0][0]]

    def query_nacecode(self, dscp: str) -> dict[str, list[dict]]:
        myobj = {'inputs': dscp}

        try:
            res = requests.post(self.url, json=myobj)
            if res.status_code == 200:
                preds = self.filter_nacecode(eval(res.text))
                return preds
            else:
                return {}
        except Exception as e:
            raise f"{e}"


if __name__ == "__main__":
    transformer = Transformer()
    transformer.query_nacecode("i mine fish")