import json
from datetime import datetime
from itertools import chain

from sklearn.model_selection import train_test_split

from models import extract_ner, init_llm
from util import evaluate_ner, process_raw_dataset


def do_llm_ner(
    input_dataset: str,
    model_name: str,
    prompt: str,
    hf_token: str,
    do_quantization: bool = True,
    test_size: float = 0.3,
    seed: int = 52,
):
    """
    Run Named Entity Recognition (NER) experiments using a large language model (LLM).

    This function loads a dataset, performs inference with a specified LLM,
    extracts NER predictions, cleans and normalizes the output, evaluates
    performance against gold labels, and saves both raw predictions and
    evaluation results.

    Args:
        input_dataset (str): Path to the input dataset in `.jsonl` format. Each line
            should contain a JSON dictionary with text and gold labels.
        model_name (str): Hugging Face model name or local path to load the model from.
        prompt (str): Prompt template used to query the LLM for NER predictions.
        hf_token (str): Hugging Face authentication token required for model loading.
        do_quantization (bool, optional): Whether to apply quantization when loading
            the model to reduce memory usage. Defaults to True.
        test_size (float, optional): Proportion of the dataset used for testing.
            Defaults to 0.3.
        seed (int, optional): Random seed for reproducible train-test splits.
            Defaults to 52.

    Workflow:
        1. Load model and tokenizer with optional quantization.
        2. Load the dataset from JSONL file.
        3. Split into train/test sets with a fixed random seed.
        4. Run the model on test set to extract NER predictions.
        5. Save raw predictions to a timestamped file.
        6. Clean predictions (model-specific post-processing for Gemma).
        7. Parse predictions into entity-tag structures.
        8. Save cleaned predictions as JSONL for evaluation.
        9. Compute and print evaluation metrics:
            - Entity-level evaluation (entity + label)
            - Token-level evaluation (entity only, ignoring label)
        10. Update a central results JSON file with evaluation metrics.

    Outputs:
        - `../output/llm_ner_pred_<model>_<timestamp>.txt`: Raw model predictions
        - `../output/llm_ner_pred_<model>_<timestamp>_eval.json`: Cleaned predictions
        - `../output/experiments_results.json`: Aggregated evaluation results

    Notes:
        - Predictions are normalized (stripped and title-cased) before evaluation
          to ensure consistency across models.
        - If the model name contains `"gemma"`, additional cleaning is applied to
          remove prompt formatting artifacts.
    """

    # Load model and tokenizer
    model, tokenizer = init_llm(
        model_name,
        hf_token,
        do_quantization=do_quantization,
    )

    # Load jsonl file into a list of dictionaries
    with open(input_dataset) as test_f:
        data = [json.loads(line) for line in test_f]

    # Create test split (notice: fixed seed)
    _, test_data = train_test_split(data, test_size=test_size, random_state=seed)

    # Extract NER tags from input sentences
    pred = extract_ner(model, tokenizer, prompt, test_data)

    # Attach NER tags to original dataset
    for sent, pred in zip(test_data, pred):
        sent["pred"] = pred

    # Create timestamp to uniquely identify output files
    dt = str(datetime.now()).split(".")[0].replace(" ", "_").replace(":", "-")

    # Save predictions to file
    model_name = model_name.replace("../", "")
    output_file = f"../output/{dt}_llm_ner_pred_{model_name.split('/')[-1]}.txt"
    with open(output_file, "w") as test_f:
        json.dump(test_data, test_f)
        print(f"Saved raw predictions to {output_file}")

    # example
    # output_file = "../output/llm_ner_pred_Llama-3.1-8B-Instruct_2025-08-20_18-58-19.txt"

    with open(output_file, "r") as f:
        # output = [line.strip() for line in f.readlines()]
        raw_dataset = json.load(f)

    # additional cleaning needed for gemma
    if "gemma" in model_name:
        for item in raw_dataset:
            item["pred"] = item["pred"].split("output:\n")[-1]

    # For each line in output look for double brackets to extract the predicted entity, its tag and its start/end indexes using regular expressions
    dataset = process_raw_dataset(raw_dataset)

    # Save as jsonl file
    with open(output_file.replace(".txt", "_eval.json"), "w") as file:
        file.write(json.dumps(dataset, ensure_ascii=False))
        print(f"Saved clean predictions to {output_file}")

    # ----- Evaluation -----
    y_true = [el["label"] for el in dataset]
    y_pred = [el["label_pred"] for el in dataset]

    # Flatten lists to evaluate metrics on whole dataset
    flat_preds = list(map(tuple, chain.from_iterable(y_pred)))
    flat_golds = list(map(tuple, chain.from_iterable(y_true)))

    # Normalize style to ensure fair comparisons
    flat_preds = [(w[0].strip().title(), w[1]) for w in flat_preds]
    flat_golds = [(w[0].strip().title(), w[1]) for w in flat_golds]

    results = evaluate_ner(flat_preds, flat_golds)
    print("NER evaluation results")
    print(results)
    print()

    # Entity-only evaluation
    # Flatten lists to evaluate metrics on whole dataset
    flat_preds = list(map(tuple, chain.from_iterable(y_pred)))
    flat_golds = list(map(tuple, chain.from_iterable(y_true)))

    # Normalize style to ensure fair comparisons
    flat_preds = [w[0].strip().title() for w in flat_preds]
    flat_golds = [w[0].strip().title() for w in flat_golds]

    tokenlevel_results = evaluate_ner(flat_preds, flat_golds)
    print("Token-level results (token only, no label)")
    print(tokenlevel_results)

    results_path = "../experiments_results.json"

    # ----- Output -----
    # Load existing results
    with open(results_path, "r") as f:
        results_dict = json.load(f)

    # Add new result under filename
    clean_name = output_file.split("/")[-1].replace(".txt", "")
    if clean_name not in results_dict:
        results_dict[clean_name] = results

        # Save back
        with open(results_path, "w") as f:
            json.dump(results_dict, f, indent=4)
            print(f"Updated results file at {results_path}")
