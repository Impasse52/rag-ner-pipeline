import os
import argparse
import sys
from pipelines import do_llm_ner
from dotenv import load_dotenv


load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="CLI to execute NLP pipelines")

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Path to input file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to output file",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="meta-llama/Llama-3.1-8B-Instruct",
        help="HuggingFace Model to be used",
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        default=os.environ["HF_TOKEN"],
        help="HuggingFace token",
    )
    parser.add_argument(
        "-p",
        "--pipeline",
        type=str,
        help="Run a pipeline with the specified parameters",
    )
    parser.add_argument(
        "-ts",
        "--test-size",
        type=float,
        default=0.3,
        help="Specify the portion of the input to be used for testing",
    )

    args = parser.parse_args()

    try:
        match args.pipeline:
            # example usage:
            case "llm_ner":
                do_llm_ner(
                    args.input,
                    args.model,
                    args.prompt,
                    os.environ["HF_TOKEN"],
                    do_quantization=True,
                    test_size=0.3,
                )
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
