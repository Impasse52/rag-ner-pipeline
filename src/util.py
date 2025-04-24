import pandas as pd
from nltk.tokenize import TreebankWordTokenizer


def convert_dataset_to_hf(df: pd.DataFrame):
    """
    Example usage:
        df = pd.read_json("../data/labelled/all.jsonl", lines=True)
        clean_samples = convert_dataset_to_hf(df)

        with open("../data/labelled/all_hf.jsonl", "w") as f:
            for sample in clean_samples:
                json.dump(sample, f)
                f.write("\n")
    """

    lines = []
    for i in range(df.shape[0]):
        lines.append(df.iloc[i].to_dict())

    formatted_dicts = []
    tokenizer = TreebankWordTokenizer()
    for ln in lines:
        tmp_dict = {}
        for start, end, tag in ln["label"]:
            tmp_dict[start] = (ln["text"][start:end], tag, end)

        tokens = tokenizer.tokenize(ln["text"])
        spans = list(tokenizer.span_tokenize(ln["text"]))

        for token, span in zip(tokens, spans):
            start = span[0]
            end = span[1]

            if start not in tmp_dict:
                tmp_dict[start] = (ln["text"][start:end], "O", end)

        formatted_dicts.append(tmp_dict)

    clean_samples = []

    for i, sample in enumerate(formatted_dicts):
        tokens = []
        labels = []

        for _, v in sorted(sample.items()):
            tokens.append(v[0])
            labels.append(v[1])

        assert len(tokens) == len(labels)

        clean_samples.append({"id": str(i), "tokens": tokens, "ner_tags": labels})

    return clean_samples
