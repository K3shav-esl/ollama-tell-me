from pipeline.parser import pdf_to_markdown
from pipeline.prompt_builder import build_prompt
from pipeline.llm_client import generate

markdown = pdf_to_markdown("D:\Projects\Coding_Projects\Ollama_tell_me\docs\ThermoIIEngl2026Ch_1_2.pdf")
system, user = build_prompt(markdown, "summary")

# print both so you can read what you're actually sending
print("=== SYSTEM ===")
print(system)
print("Generating....")
# print(user[:500])

# then actually call it
output = generate(user, system)
print("Please check the output file")
with open("testoutput.tex", "a", encoding="utf-8") as f:
    f.write(r"""
\documentclass{article}
\usepackage{amsmath}
\usepackage{enumerate}
\begin{document}
""")
    f.write(output)

    f.write ( r"""\end{document}""")

