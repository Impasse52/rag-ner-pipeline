import numpy as np
from collections import Counter
import re
from typing import Iterable
import pandas as pd
from nltk.tokenize import TreebankWordTokenizer
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import rich


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

    # Quit if labels are already in the right format
    assert "-" in ner_tags[0][2], ValueError("Tags are already in the right format.")

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


def process_raw_dataset(raw_ds):
    # Used to map patterns to tags
    patterns = [
        (r"\(\((.*?)\)\)", "PER"),
        (r"\[\[(.*?)\]\]", "LOC"),
        (r"\{\{(.*?)\}\}", "ORG"),
        (r"\<\<(.*?)\>\>", "MISC"),
    ]

    processed_ds = []
    for i, item in enumerate(raw_ds):
        pred, text, labels = item["pred"], item["text"], item["label"]
        labels_pred = []
        for pattern, label in patterns:
            for match in re.finditer(pattern, pred):
                # Get match delimiters
                start_idx = match.start()
                end_idx = match.end()

                # Add +/- 2 brackets to the indexes
                start_idx = match.start() + 2
                end_idx = match.end() - 2

                labels_pred.append((pred[start_idx:end_idx], label))

        # Combine BIO entities into single entities
        combined_ent = combine_bio_entities(item["label"])

        # Extract labels from original text
        labels = []
        for annotation in combined_ent:
            start, end, tag = annotation
            labels.append((text[start:end], tag))

        processed_ds.append(
            {
                "idx": i,
                "text": text,
                "label": labels,
                "text_pred": pred,
                "label_pred": labels_pred,
            }
        )

    return processed_ds


def replace_all(old: str, to_replace: list, new: str):
    for text in to_replace:
        old = old.replace(text, new)

    return old


def _sort_words(tokens: list | set) -> list:
    """Sort words within a string so that multi-word tokens are scored properly.
    This is necessary due to how LLMs sometimes rewrite multi-word tokens in the
    wrong order, causing "unfair" evaluations.

    For example, "Mario Leonardo Ferri" and "Leonardo Ferri Mario" are treated as the same entity."""

    tmp = []
    for w in tokens:
        tmp.append((" ".join(sorted(w[0].split(" "))), w[1]))

    return tmp


def eval_ner(pred: list, true: list):
    """Evaluate a single NER sample"""

    # Return f1 = 1.0 if both pred and gold are empty
    if len(pred) == 0 and len(true) == 0:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}

    # Preprocessing
    pred = _sort_words(pred)
    gold = _sort_words(true)

    # print("--- Pred ---")
    # print(pred)
    # print(pred_set)
    # print("--- True ---")
    # print(true)
    # print(gold_set)

    pred_counter = Counter(pred)
    gold_counter = Counter(gold)

    # Elementwise intersection — counts minimum occurrences in both
    true_positives = pred_counter & gold_counter

    tp = sum(true_positives.values())
    precision = tp / len(pred) if pred else 0.0
    recall = tp / len(gold) if gold else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    return {"precision": precision, "recall": recall, "f1": f1}


def compute_ner_conf_matrix(pred, true, labels=["PER", "LOC", "ORG", "MISC"]):
    """
    Compute confusion matrix for each sentence, then sum the matrices cell-wise.
    """

    matrices = []
    # For each sentence
    for idx in range(len(true)):
        conf_matrix = [[0 for _ in range(len(labels))] for _ in range(len(labels))]

        # Apply preprocessing
        pred_sorted = _sort_words(pred[idx])
        true_sorted = _sort_words(true[idx])

        # Create dictionaries mapping text -> label
        pred_dict = {text: label for text, label in pred_sorted}
        true_dict = {text: label for text, label in true_sorted}

        # Get all unique entities
        entities = set(pred_dict.keys()) | set(true_dict.keys())

        for ent in entities:
            pred_label = pred_dict.get(ent)  # None if not predicted
            true_label = true_dict.get(ent)  # None if not in gold

            if pred_label and true_label:
                # Entity was both predicted and in gold standard
                i = labels.index(pred_label)
                j = labels.index(true_label)

                conf_matrix[i][j] += 1

        matrices.append(conf_matrix)

    return np.sum(matrices, axis=0, keepdims=True)[0]


def print_avg_metrics(y_true, y_pred):
    scores = [eval_ner(y_true[idx], y_pred[idx]) for idx in range(len(y_true))]
    avg_metrics = {key: sum(d[key] for d in scores) / len(scores) for key in scores[0]}
    rich.print(avg_metrics)


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


def flatten(l: Iterable) -> list:
    return list(itertools.chain.from_iterable(l))


def to_list_of_entities(df: pd.DataFrame, idx: int):
    """
    Convert list of tags expressed as [start, end, label] into
    a list of tags expressed as (token, label).

    Input: index of dataframe row
    """
    text = df.iloc[idx]["text"]
    rows = df.iloc[idx]["label"]

    output = []
    for r in rows:
        start = r[0]
        end = r[1]
        tag = r[2]
        output.append((text[start:end], tag))

    return output


def extract_ner_labels(pred):
    patterns = [
        (r"\(\((.*?)\)\)", "PER"),
        (r"\[\[(.*?)\]\]", "LOC"),
        (r"\{\{(.*?)\}\}", "ORG"),
        (r"\<\<(.*?)\>\>", "MISC"),
    ]

    labels_pred = []
    for pattern, label in patterns:
        for match in re.finditer(pattern, pred):
            # Get match delimiters
            start_idx = match.start()
            end_idx = match.end()

            # Add +/- 2 brackets to the indexes
            start_idx = match.start() + 2
            end_idx = match.end() - 2

            labels_pred.append((pred[start_idx:end_idx], label))

    return labels_pred


def replace_with_parentheses(text, entities):
    """
    Replace substrings at specified indices with the same text wrapped in (( )).

    Args:
        text: The original string
        entities: List of (start, end, tag) tuples

    Returns:
        Modified string with replacements
    """
    # Sort entities by start position in reverse order
    # This ensures we process from end to start, avoiding index shifts
    sorted_entities = sorted(entities, key=lambda x: x[0], reverse=True)

    result = text
    for start, end, tag in sorted_entities:
        original = result[start:end]
        if "PER" in tag:
            replacement = f"(({original}))"
        elif "LOC" in tag:
            replacement = f"[[{original}]]"
        elif "ORG" in tag:
            replacement = "{{" + original + "}}"
        elif "MISC" in tag:
            replacement = f"<<{original}>>"
        result = result[:start] + replacement + result[end:]

    return result


def draw_bipartite(b: nx.Graph, figsize: tuple = (12, 15), draw_labels: bool = True):
    # Define colors for each entity type
    entity_colors = {
        "PER": "#FF6B6B",  # Red
        "LOC": "#4ECDC4",  # Teal
        "ORG": "#95E1D3",  # Light green
        "MISC": "#FFE66D",  # Yellow
    }

    # Separate nodes in doc and entity nodes
    doc_nodes = [n for n in b.nodes() if isinstance(n[0], int)]
    entity_nodes = [n for n in b.nodes() if not isinstance(n[0], int)]

    # Assign colors to nodes
    node_colors = []
    for node in b.nodes():
        if node[1] != "DOC":
            # Entity node - color by type
            entity_type = node[1].upper()
            node_colors.append(entity_colors.get(entity_type, "#CCCCCC"))
        else:
            # Document node - gray
            node_colors.append("#AAAAAA")

    plt.figure(figsize=figsize)

    # Use bipartite layout
    pos = nx.drawing.layout.bipartite_layout(b, entity_nodes)

    # Draw nodes with black outline
    nx.draw_networkx_nodes(
        b,
        pos,
        node_color=node_colors,
        node_size=100,
        edgecolors="black",
        linewidths=0.5,
    )

    # Draw edges
    nx.draw_networkx_edges(b, pos, alpha=0.1, width=0.1)

    # Draw labels with offset (below nodes)
    labels = {}
    for node in b.nodes():
        if isinstance(node, tuple):
            labels[node] = node[0]  # Entity name
        else:
            labels[node] = node  # Document ID

    # Draw labels below nodes
    if draw_labels:
        label_pos = {k: (v[0], v[1] - 0.01) for k, v in pos.items()}
        nx.draw_networkx_labels(b, label_pos, labels, font_size=5)

    # Add legend
    legend_elements = [
        plt.Line2D(  # type: ignore
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=color,
            markersize=10,
            markeredgecolor="black",
            markeredgewidth=2,
            label=entity_type,
        )
        for entity_type, color in entity_colors.items()
    ]
    legend_elements.append(
        plt.Line2D(  # type: ignore
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="#AAAAAA",
            markersize=10,
            markeredgecolor="black",
            markeredgewidth=2,
            label="Document",
        )
    )
    plt.legend(handles=legend_elements, loc="upper right", fontsize=10)

    plt.title("Entity-Document Bipartite Graph")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def draw_graph(
    g: nx.Graph,
    title: str,
    figsize: tuple = (12, 15),
    draw_labels: bool = True,
    node_size: int = 100,
    label_font_size: int = 5,
):
    # define colors for each entity type
    entity_colors = {
        "PER": "#FF6B6B",  # RED
        "LOC": "#4ECDC4",  # TEAL
        "ORG": "#95E1D3",  # LIGHT GREEN
        "MISC": "#FFE66D",  # YELLOW
    }

    # assign colors to nodes
    node_colors = []
    for node in g.nodes():
        if node[1] != "DOC":
            # entity node - color by type
            entity_type = node[1].upper()
            node_colors.append(entity_colors.get(entity_type, "#cccccc"))
        else:
            # document node - gray
            node_colors.append("#aaaaaa")

    plt.figure(figsize=figsize)

    pos = nx.drawing.layout.kamada_kawai_layout(g)

    # Draw nodes
    nx.draw_networkx_nodes(
        g,
        pos,
        node_color=node_colors,
        node_size=node_size,
        edgecolors="black",
        linewidths=0.5,
    )

    # Draw edges
    nx.draw_networkx_edges(g, pos, alpha=0.5, width=0.2)

    # Draw labels with offset (below nodes)
    labels = {}
    for node in g.nodes():
        if isinstance(node, tuple):
            labels[node] = node[0]  # entity name
        else:
            labels[node] = node  # document id

    # Draw labels below nodes
    label_pos = {k: (v[0], v[1] - 0.02) for k, v in pos.items()}
    if draw_labels:
        nx.draw_networkx_labels(g, label_pos, labels, font_size=label_font_size)

    # Add legend
    legend_elements = [
        plt.Line2D(  # type: ignore
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=color,
            markersize=10,
            markeredgecolor="black",
            markeredgewidth=2,
            label=entity_type,
        )
        for entity_type, color in entity_colors.items()
    ]
    plt.legend(handles=legend_elements, loc="upper right", fontsize=10)

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def compute_average_metrics(metrics_list):
    """
    Compute average metrics from a list of metric dictionaries.

    Args:
        metrics_list: List of dictionaries containing metrics

    Returns:
        Dictionary with averaged metrics
    """
    if not metrics_list:
        return {}

    # Get all metric names from the first dictionary
    metric_names = metrics_list[0].keys()

    # Initialize sums
    sums = {name: 0 for name in metric_names}

    # Sum up all values
    for metrics in metrics_list:
        for name in metric_names:
            sums[name] += metrics[name]

    # Compute averages
    n = len(metrics_list)
    averages = {name: sums[name] / n for name in metric_names}

    return averages
