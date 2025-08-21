import os
import argparse
import sys
from pipeline import run_pipeline
from dotenv import load_dotenv


load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="CLI to execute NLP pipelines")

    parser.add_argument("-i", "--input", type=str, help="Path to input file")
    parser.add_argument("-o", "--output", type=str, help="Path to output file")
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

    args = parser.parse_args()

    try:
        run_pipeline(args.input, args.output, verbose=args.verbose)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
