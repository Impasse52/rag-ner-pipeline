# %% [markdown]
# # RENER
# %%
import json

# Load jsonl file into a list of dictionaries
with open("./data/kind/parallel/fiction_filtered.jsonl") as test_f:
    data = [json.loads(line) for line in test_f]

len(data)

# %%
from collections import Counter

import matplotlib.pyplot as plt

from util import extract_ner_labels, flatten

entities = []
for item in data:
    entities.append(extract_ner_labels(item["text"]))

entities = flatten(entities)
entities_dist = Counter([ent[1] for ent in entities])

plt.figure()
plt.pie(
    entities_dist.values(),  # type: ignore
    labels=entities_dist.keys(),  # type: ignore
    autopct=lambda pct: f"{pct:.0f}%" if pct > 1.1 else "",
    startangle=90,
    pctdistance=0.5,
    wedgeprops={"edgecolor": "black"},
)

plt.title("Distribution of NER labels")
plt.show()

# %%
import json
from datetime import datetime
from pathlib import Path
from time import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import seaborn as sns
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.dataclasses import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.document_stores.types import DuplicatePolicy
from haystack_integrations.components.generators.ollama import OllamaGenerator
from sklearn.model_selection import KFold
from tqdm.notebook import tqdm

from prompts import default_examples, guidelines_llama3_legal_lite
from util import eval_ner, extract_ner_labels


def _sort_words(entities: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Sort entities by text for consistent comparison."""
    return sorted(entities, key=lambda x: x[0])


def compute_ner_conf_matrix(
    pred: List[List[Tuple[str, str]]],
    true: List[List[Tuple[str, str]]],
    labels: List[str] = ["PER", "LOC", "ORG", "MISC"],
) -> np.ndarray:
    """
    Compute confusion matrix for each sentence, then sum the matrices cell-wise.

    Args:
        pred: List of predicted entity lists (one per sentence)
        true: List of true entity lists (one per sentence)
        labels: List of entity type labels

    Returns:
        Confusion matrix as numpy array
    """
    matrices = []

    for idx in range(len(true)):
        conf_matrix = [[0 for _ in range(len(labels))] for _ in range(len(labels))]

        pred_sorted = _sort_words(pred[idx])
        true_sorted = _sort_words(true[idx])

        pred_dict = {text: label for text, label in pred_sorted}
        true_dict = {text: label for text, label in true_sorted}

        entities = set(pred_dict.keys()) | set(true_dict.keys())

        for ent in entities:
            pred_label = pred_dict.get(ent)
            true_label = true_dict.get(ent)

            if pred_label and true_label:
                i = labels.index(pred_label)
                j = labels.index(true_label)
                conf_matrix[i][j] += 1

        matrices.append(conf_matrix)

    return np.sum(matrices, axis=0, keepdims=True)[0]


class NERExperiment:
    """Handles NER evaluation experiments with k-fold cross-validation."""

    ENTITY_TYPES = ["PER", "LOC", "ORG", "MISC"]

    def __init__(
        self, model: str, temperature: float, n_splits: int = 5, debug: bool = False
    ):
        self.model = model
        self.temperature = temperature
        self.n_splits = n_splits
        self.llm = OllamaGenerator(
            model=model,
            url="http://localhost:11434",
            generation_kwargs={"temperature": temperature},
        )
        self.results = {
            "model": model,
            "temperature": temperature,
        }
        self.debug = debug

    def preprocess_entities(
        self, entities: List[Tuple[str, str]]
    ) -> List[Tuple[str, str]]:
        """Preprocess entity tuples for consistent comparison."""
        return [(w[0].strip().title(), w[1]) for w in entities]

    def filter_entities_by_type(
        self, entities: List[Tuple[str, str]], entity_type: str
    ) -> List[Tuple[str, str]]:
        """Filter entities by type."""
        return [(e[0], e[1]) for e in entities if e[1] == entity_type]

    def build_prompt(self, retrieved_docs: List[Document], query: str) -> str:
        """Build the complete prompt from retrieved documents and query."""
        context = "".join(
            [
                f"Input: {doc.content}\n<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
                f"Output: {doc.meta['output']}<|eot_id|>\n\n"
                for doc in retrieved_docs
            ]
        ).strip()

        return guidelines_llama3_legal_lite + default_examples + context + query

    def setup_document_store(self, train_data: List[Dict]) -> InMemoryDocumentStore:
        """Initialize and populate document store with training data."""
        document_store = InMemoryDocumentStore()
        docs = [
            Document(content=d["input"], meta={"output": d["text"]}) for d in train_data
        ]
        document_store.write_documents(docs, policy=DuplicatePolicy.OVERWRITE)
        return document_store

    def retrieve_documents(
        self, document_store: InMemoryDocumentStore, query: str, top_k: int
    ) -> List[Document]:
        """Retrieve top-k documents using BM25."""
        retriever = InMemoryBM25Retriever(document_store=document_store)
        retrieval_result = retriever.run(query=query, top_k=top_k)
        return retrieval_result["documents"]

    def generate_prediction(self, prompt: str) -> str:
        """Generate prediction using LLM."""
        try:
            generation_result = self.llm.run(
                prompt=prompt,
                generation_kwargs={"temperature": self.temperature},
            )
            llm_output = generation_result["replies"][0]
            return llm_output.replace("Output: \n", "")
        except Exception as e:
            print(f"Exception occurred: {e}. Returning empty prediction.")
            return ""

    def evaluate_single_item(
        self,
        item: Dict,
        document_store: InMemoryDocumentStore,
        top_k: int,
    ) -> Dict[str, Any]:
        """Evaluate a single test item."""
        query = f"Input: {item['input']}\n<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"

        retrieved_docs = self.retrieve_documents(document_store, query, top_k)

        prompt = self.build_prompt(retrieved_docs, query)
        prediction = self.generate_prediction(prompt)

        if not prediction:
            return None

        item["pred"] = prediction

        true = self.preprocess_entities(extract_ner_labels(item["text"]))
        pred = self.preprocess_entities(extract_ner_labels(prediction))

        overall_score = eval_ner(pred, true)

        if self.debug:
            print(f"Input: {item['text']}")
            print(f"Pred:  {prediction}")
            print(f"Score: {overall_score}")
            print()

        entity_scores = {}
        for entity_type in self.ENTITY_TYPES:
            true_type = self.filter_entities_by_type(true, entity_type)
            pred_type = self.filter_entities_by_type(pred, entity_type)
            entity_scores[entity_type] = eval_ner(pred_type, true_type)

        return {
            "overall": overall_score,
            "by_entity": entity_scores,
            "retrieval_scores": [d.score for d in retrieved_docs],
            "true": true,
            "pred": pred,
        }

    def calculate_fold_metrics(self, scores: List[Dict]) -> Tuple[Dict, Dict]:
        """Calculate average and standard deviation metrics across fold."""
        if not scores:
            return {}, {}

        avg_metrics = {
            key: sum(d[key] for d in scores) / len(scores) for key in scores[0]
        }
        std_metrics = {
            key: float(np.std([d[key] for d in scores])) for key in scores[0]
        }
        return avg_metrics, std_metrics

    def run_fold(
        self, train_data: List[Dict], test_data: List[Dict], top_k: int, fold_idx: int
    ) -> Dict:
        """Run evaluation for a single fold."""
        print(f"Running split # {fold_idx + 1}/{self.n_splits}")

        start_time = time()

        document_store = self.setup_document_store(train_data)

        all_scores = {
            "overall": [],
            **{entity_type: [] for entity_type in self.ENTITY_TYPES},
            "retrieval": [],
        }

        y_true = []
        y_pred = []

        pbar = tqdm(test_data, desc=f"Fold {fold_idx + 1}")
        for item in pbar:
            result = self.evaluate_single_item(item, document_store, top_k)

            if result is None:
                continue

            all_scores["overall"].append(result["overall"])
            all_scores["retrieval"].append(result["retrieval_scores"])

            y_true.append(result["true"])
            y_pred.append(result["pred"])

            for entity_type in self.ENTITY_TYPES:
                all_scores[entity_type].append(result["by_entity"][entity_type])

            avg_metrics, _ = self.calculate_fold_metrics(all_scores["overall"])
            pbar.set_postfix(avg_metrics)

        runtime = time() - start_time

        confusion_matrix = compute_ner_conf_matrix(y_pred, y_true, self.ENTITY_TYPES)

        fold_results = {
            "runtime": runtime,
            "retrieval_scores": all_scores["retrieval"],
            "confusion_matrix": confusion_matrix.tolist(),
        }

        for key in ["overall"] + self.ENTITY_TYPES:
            avg, std = self.calculate_fold_metrics(all_scores[key])
            fold_results[f"avg_metrics_{key.lower()}"] = avg
            fold_results[f"std_metrics_{key.lower()}"] = std

            fold_results[f"all_scores_{key.lower()}"] = all_scores[
                key
            ]  # possible cause for memory leak?

        return fold_results

    def aggregate_topk_metrics(self, top_k: int) -> None:
        """Aggregate metrics across all folds for a given top_k."""
        fold_keys = [f"kfold={i + 1}" for i in range(self.n_splits)]

        confusion_matrices = [
            np.array(self.results[f"top_k={top_k}"][fold_key]["confusion_matrix"])
            for fold_key in fold_keys
        ]
        avg_confusion_matrix = np.mean(confusion_matrices, axis=0)
        self.results[f"top_k={top_k}"]["avg_confusion_matrix"] = (
            avg_confusion_matrix.tolist()
        )

        for metric_type in ["overall"] + [e.lower() for e in self.ENTITY_TYPES]:
            fold_avgs = [
                self.results[f"top_k={top_k}"][fold_key][f"avg_metrics_{metric_type}"]
                for fold_key in fold_keys
            ]

            avg_metrics = {
                key: sum(d[key] for d in fold_avgs) / len(fold_avgs)
                for key in fold_avgs[0]
            }
            std_metrics = {
                key: float(np.std([d[key] for d in fold_avgs])) for key in fold_avgs[0]
            }

            suffix = f"_{metric_type}" if metric_type != "overall" else ""
            self.results[f"top_k={top_k}"][f"avg_metrics_topk={top_k}{suffix}"] = (
                avg_metrics
            )
            self.results[f"top_k={top_k}"][f"std_metrics_topk={top_k}{suffix}"] = (
                std_metrics
            )

    def run_experiment(self, data: List[Dict], top_k_range: range) -> None:
        """Run the complete experiment across all top_k values."""
        kf = KFold(n_splits=self.n_splits)

        for top_k in top_k_range:
            print(f"\nRunning experiment with top_k={top_k}")
            self.results[f"top_k={top_k}"] = {}

            for i, (train_idx, test_idx) in enumerate(kf.split(data)):
                train_data = [data[idx] for idx in train_idx]
                test_data = [data[idx] for idx in test_idx]

                fold_results = self.run_fold(train_data, test_data, top_k, i)
                self.results[f"top_k={top_k}"][f"kfold={i + 1}"] = fold_results

            self.aggregate_topk_metrics(top_k)

    def save_results(self, output_path: Path) -> None:
        """Save results to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to {output_path}")

    def load_results(self, input_path: Path) -> None:
        """Load results from JSON file."""
        with open(input_path, "r") as f:
            self.results = json.load(f)

        print("\nResults loaded into self.results")

    def print_confusion_matrix(self, top_k: int, normalize: bool = True) -> None:
        """Pretty print the confusion matrix for a given top_k value.

        Args:
            top_k: The top_k value to print results for
            normalize: If True, normalize by row (show proportions). If False, show counts.
        """
        if f"top_k={top_k}" not in self.results:
            print(f"No results found for top_k={top_k}")
            return

        conf_matrix = np.array(self.results[f"top_k={top_k}"]["avg_confusion_matrix"])

        if normalize:
            row_sums = conf_matrix.sum(axis=1, keepdims=True)
            row_sums = np.where(row_sums == 0, 1, row_sums)
            conf_matrix = conf_matrix / row_sums

        matrix_type = "Normalized" if normalize else "Count-based"
        print(f"\n{'=' * 60}")
        print(f"{matrix_type} Average Confusion Matrix for top_k={top_k}")
        print(f"{'=' * 60}")
        print(f"{'':>8}", end="")
        for label in self.ENTITY_TYPES:
            print(f"{label:>8}", end="")
        print(" (True)")
        print("-" * 60)

        format_str = "{:>8.3f}" if normalize else "{:>8.1f}"
        for i, pred_label in enumerate(self.ENTITY_TYPES):
            print(f"{pred_label:>8}", end="")
            for j in range(len(self.ENTITY_TYPES)):
                print(format_str.format(conf_matrix[i][j]), end="")
            print()
        print("(Pred)")
        print(f"{'=' * 60}\n")

    def plot_confusion_matrix(
        self,
        top_k: int,
        normalize: bool = True,
        save_path: Optional[Path] = None,
        figsize: Tuple[int, int] = (7, 5),
    ) -> None:
        """Plot confusion matrix as a heatmap for a given top_k value.

        Args:
            top_k: The top_k value to plot results for
            normalize: If True, normalize by row (show proportions). If False, show counts.
            save_path: Optional path to save the figure. If None, displays interactively.
            figsize: Figure size as (width, height)
        """
        if f"top_k={top_k}" not in self.results:
            print(f"No results found for top_k={top_k}")
            return

        conf_matrix = np.array(self.results[f"top_k={top_k}"]["avg_confusion_matrix"])

        if normalize:
            row_sums = conf_matrix.sum(axis=1, keepdims=True)
            row_sums = np.where(row_sums == 0, 1, row_sums)
            conf_matrix = conf_matrix / row_sums

        fig, ax = plt.subplots(figsize=figsize)

        fmt = ".3f" if normalize else ".1f"
        sns.heatmap(
            conf_matrix,
            annot=True,
            fmt=fmt,
            cmap="Blues",
            xticklabels=self.ENTITY_TYPES,
            yticklabels=self.ENTITY_TYPES,
            cbar_kws={"label": "Proportion" if normalize else "Count"},
            ax=ax,
            vmin=0,
            vmax=1 if normalize else None,
        )

        ax.set_xlabel("True Label", fontsize=12, fontweight="bold")
        ax.set_ylabel("Predicted Label", fontsize=12, fontweight="bold")

        matrix_type = "Normalized" if normalize else "Count-based"
        title = f"{matrix_type} Confusion Matrix (top_k={top_k})"
        ax.set_title(title, fontsize=14, fontweight="bold", pad=20)

        plt.tight_layout()

        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Figure saved to {save_path}")
        else:
            plt.show()

        plt.close()


# %%
# Set parameters
MODEL = "llama3.1:8b"
TEMPERATURE = 0
N_SPLITS = 10
TOP_K_RANGE = range(0, 8)

# Create output filename
dt = str(datetime.now()).split(".")[0].replace(" ", "_").replace(":", "-")
output_filename = Path(f"./output/rener_{dt}.json")

# Initialize and run experiment
experiment = NERExperiment(
    model=MODEL,
    temperature=TEMPERATURE,
    n_splits=N_SPLITS,
    debug=True,
)
experiment.run_experiment(data, TOP_K_RANGE)
experiment.save_results(output_filename)


# %%
# experiment.load_results(
#     Path(
#         "/home/giuseppetermerissa/Scrivania/tesi-gtermerissa/output/rener_2026-01-09_10-47-21.json"
#     )
# )

# %%
# Print confusion matrices
for top_k in range(0, 8):
    experiment.plot_confusion_matrix(top_k)
