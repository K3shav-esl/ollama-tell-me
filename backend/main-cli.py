import argparse
import sys
from pipeline.parser import pdf_to_markdown
from pipeline.prompt_builder import build_prompt
from pipeline.llm_client import generate

def main():
    parser = argparse.ArgumentParser(description="MechMind CLI")
    parser.add_argument("--pdf", required=True, help="Path to the lecture PDF")
    parser.add_argument("--mode", choices=["summary", "mcq", "problems"], required=True, help="Generation mode")
    parser.add_argument("--chars", type=int, default=6000, help="Max characters to send to LLM (default: 6000)")
    args = parser.parse_args()

    # Step 1 — Parse
    print(f"[1/3] Parsing PDF: {args.pdf}")
    try:
        markdown = pdf_to_markdown(args.pdf)
    except Exception as e:
        print(f"[ERROR] Failed to parse PDF: {e}")
        sys.exit(1)

    if not markdown.strip():
        print("[ERROR] Parser returned empty content. Check the PDF is not scanned/image-only.")
        sys.exit(1)

    print(f"       Extracted {len(markdown)} characters")

    # Slice to avoid context overflow — remove this in Weekend 5 when chunking is implemented
    if len(markdown) > args.chars:
        print(f"       Trimming to {args.chars} chars to fit LLM context window")
        markdown = markdown[:args.chars]

    # Step 2 — Build prompt and generate
    print(f"[2/3] Generating {args.mode} (this may take 1-3 minutes)...")
    try:
        system, prompt = build_prompt(markdown, args.mode)
        output = generate(prompt, system)
    except Exception as e:
        print(f"[ERROR] LLM generation failed: {e}")
        print("       Is 'ollama serve' running in a separate terminal?")
        sys.exit(1)

    if not output.strip():
        print("[ERROR] LLM returned empty output.")
        sys.exit(1)

    # Step 3 — Print output
    print(f"[3/3] Done.\n")
    print(output)

if __name__ == "__main__":
    main()