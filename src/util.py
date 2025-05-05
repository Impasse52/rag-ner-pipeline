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


def combine_bio_entities(ner_tags):
    """
    Example usage:

    from util import combine_bio_entities

    with open("../data/labelled/test.jsonl", "r") as file:
        data = [json.loads(line) for line in file]

    # Delete id and meta keys in each dict
    for item in data:
        del item["id"]
        del item["meta"]

    for d in data:
        d["label"] = combine_bio_entities(d["label"])


    with open("../data/labelled/test_combined.jsonl", "w") as file:
        file.writelines([json.dumps(item, ensure_ascii=False) + "\n" for item in data])
    """

    combined = []
    i = 0
    while i < len(ner_tags):
        start, end, label = ner_tags[i]
        if label.startswith("B-"):
            entity_type = label[2:]
            entity_start = start
            entity_end = end
            i += 1
            while i < len(ner_tags) and ner_tags[i][2] == f"I-{entity_type}":
                _, next_end, _ = ner_tags[i]
                entity_end = next_end
                i += 1
            combined.append([entity_start, entity_end, entity_type])
        else:
            i += 1  # skip I- tags that don't follow a B-

    return combined


def replace_all(old: str, to_replace: list, new: str):
    for text in to_replace:
        old = old.replace(text, new)

    return old


def evaluate_ner(pred_spans: list, gold_spans: list):
    pred_set = set(map(tuple, pred_spans))
    gold_set = set(map(tuple, gold_spans))

    true_positives = pred_set & gold_set

    precision = len(true_positives) / len(pred_set)  # if pred_set else 0.0
    recall = len(true_positives) / len(gold_set)  # if gold_set else 0.0

    f1 = (
        (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    )

    return {"precision": precision, "recall": recall, "f1": f1}


def biluo_to_bio(biluo_tags):
    bio_tags = []
    for tag in biluo_tags:
        if tag == "O":
            bio_tags.append("O")
        elif tag.startswith("B-") or tag.startswith("U-"):
            bio_tags.append("B-" + tag[2:])
        elif tag.startswith("I-") or tag.startswith("L-"):
            bio_tags.append("I-" + tag[2:])
        else:  # for '-' or other errors
            bio_tags.append(tag)
    return bio_tags
