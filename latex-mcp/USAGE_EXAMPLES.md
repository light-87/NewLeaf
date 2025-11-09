# LaTeX MCP Server - Usage Examples

Complete examples showing how to use all features of the enhanced LaTeX MCP server.

## Table of Contents

1. [Simple Documents](#simple-documents)
2. [Documents with Citations](#documents-with-citations)
3. [Projects with Images](#projects-with-images)
4. [ZIP File Templates](#zip-file-templates)
5. [Multi-File Projects](#multi-file-projects)
6. [Common Academic Paper Workflow](#common-academic-paper-workflow)

---

## Simple Documents

### Example 1: Hello World

```
You: Compile this LaTeX:
\documentclass{article}
\begin{document}
Hello, World!
\end{document}

Claude: ✅ LaTeX compiled successfully!
PDF: /path/to/output/document_20250109_143022.pdf
```

### Example 2: Document with Math

```
You: Create a LaTeX document with Einstein's field equations

Claude: [generates LaTeX with tensor equations and compiles]
✅ LaTeX compiled successfully!
```

---

## Documents with Citations

### Example 3: Simple Bibliography

**You:**
```
Compile a paper with these citations:
- Lamport's LaTeX book (1994)
- Knuth's TeXbook (1984)
```

**Claude generates and compiles:**
```latex
\documentclass{article}
\begin{document}

LaTeX is widely used \cite{lamport1994latex}.
It was built on TeX \cite{knuth1984texbook}.

\bibliography{references}
\bibliographystyle{plain}
\end{document}
```

**With references.bib:**
```bibtex
@book{lamport1994latex,
  title={LATEX: A Document Preparation System},
  author={Lamport, Leslie},
  year={1994},
  publisher={Addison-Wesley}
}

@book{knuth1984texbook,
  title={The TeXbook},
  author={Knuth, Donald E.},
  year={1984},
  publisher={Addison-Wesley}
}
```

**Result:**
- MCP server auto-detects BibTeX is needed
- Runs: pdflatex → bibtex → pdflatex → pdflatex
- All citations properly rendered!

### Example 4: BibLaTeX (Modern Bibliography)

**LaTeX:**
```latex
\documentclass{article}
\usepackage[backend=biber]{biblatex}
\addbibresource{references.bib}

\begin{document}
Modern citation \cite{shannon1948}.

\printbibliography
\end{document}
```

**Result:**
- Auto-detects BibLaTeX
- Uses `biber` instead of `bibtex`
- Perfect citation rendering

---

## Projects with Images

### Example 5: Paper with Figure

**Directory structure:**
```
my_paper/
├── main.tex
├── references.bib
└── figures/
    └── plot.png
```

**Prompt:**
```
You: Compile the LaTeX project in /path/to/my_paper/

Claude: [uses compile_latex_project tool]
✅ LaTeX project compiled successfully!
```

**main.tex:**
```latex
\documentclass{article}
\usepackage{graphicx}

\begin{document}
\section{Results}

See Figure~\ref{fig:results}.

\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{figures/plot.png}
\caption{Experimental results}
\label{fig:results}
\end{figure}

\end{document}
```

**What happens:**
- Server finds `main.tex` automatically
- Copies `figures/plot.png` to temp compilation directory
- Maintains directory structure
- Figure renders correctly!

### Example 6: Multiple Image Formats

**Supported formats:**
- PNG, JPG, JPEG, GIF (raster images)
- PDF, EPS, SVG (vector graphics)

```latex
\includegraphics{figure.png}   % PNG
\includegraphics{diagram.pdf}  % PDF vector
\includegraphics{photo.jpg}    % JPEG
\includegraphics{plot.eps}     % EPS (great for publications)
```

All work automatically!

---

## ZIP File Templates

### Example 7: Overleaf Template

**Scenario:** You downloaded an Overleaf template as ZIP

**Prompt:**
```
You: Compile the Overleaf template at /Downloads/ieee_template.zip

Claude: [uses compile_latex_zip tool]
✅ LaTeX ZIP compiled successfully!
PDF: /path/to/output/ieee_template.pdf
```

**What happens:**
1. Extracts ZIP to temp directory
2. Finds main .tex file (usually `main.tex`)
3. Copies all assets (.cls, .bst, figures, etc.)
4. Compiles with all dependencies
5. Cleans up temp files
6. Opens PDF

### Example 8: arXiv Paper Source

**Download arXiv source:**
```
You: I downloaded the arXiv source for paper 2103.12345 as a ZIP.
Compile it at /Downloads/2103.12345.zip

Claude: [extracts and compiles]
✅ LaTeX ZIP compiled successfully!
```

Perfect for reviewing papers with full formatting!

### Example 9: Specify Main File

**If auto-detection fails:**
```
You: Compile /path/to/template.zip with main file "paper.tex"

Claude: [uses compile_latex_zip with main_file parameter]
✅ Compiled successfully!
```

---

## Multi-File Projects

### Example 10: Project with Chapters

**Structure:**
```
thesis/
├── main.tex
├── chapters/
│   ├── intro.tex
│   ├── methods.tex
│   └── results.tex
├── figures/
│   ├── fig1.png
│   └── fig2.pdf
└── references.bib
```

**main.tex:**
```latex
\documentclass{book}

\begin{document}

\input{chapters/intro}
\input{chapters/methods}
\input{chapters/results}

\bibliography{references}
\bibliographystyle{plain}

\end{document}
```

**Prompt:**
```
You: Compile the thesis project in /path/to/thesis/

Claude: ✅ All chapters, figures, and citations compiled!
```

**Server handles:**
- Finds main.tex
- Copies all .tex files (including chapters/)
- Copies all figures/
- Copies references.bib
- Maintains directory structure
- Multiple compilation passes for citations

---

## Common Academic Paper Workflow

### Example 11: Complete Paper Workflow

**Starting from scratch:**

**Step 1: Create structure**
```
You: Create a LaTeX paper with:
- Title: "Machine Learning for Climate Modeling"
- Authors: Me and Prof. Smith
- Abstract
- Introduction with 2 citations
- Methods section
- Results with a figure placeholder
- Conclusion
- Bibliography

Claude: [generates complete LaTeX document]
```

**Step 2: Add your content**
```
You: Update the methods section to describe our neural network architecture

Claude: [edits main.tex with your content]
```

**Step 3: Add citations**
```
You: Add citations for:
- "Attention is All You Need" (2017)
- "ResNet" paper (2016)

Claude: [updates references.bib and adds \cite commands]
```

**Step 4: Add figures**
```
You: Add a figure showing our model architecture from figures/architecture.png

Claude: [adds \includegraphics with proper caption]
```

**Step 5: Compile**
```
You: Compile the project

Claude: [uses compile_latex_project]
✅ Perfect! All citations and figures rendered!

⚠️ Warnings:
  - LaTeX warnings detected (check log)

(Minor overfull hbox warnings, not critical)
```

### Example 12: Conference Paper (IEEE Format)

**Starting with template:**

```
You: I have an IEEE conference template ZIP.
Set it up for a paper titled "Novel Approach to Data Mining"

Claude:
1. [extracts ZIP]
2. [modifies main.tex with your title]
3. [compiles]
✅ IEEE formatted paper ready!
```

**Add content:**
```
You: Add a two-column figure spanning the full page width showing results.png

Claude: [adds figure* environment for two-column span]
```

**Final compilation:**
```
You: Compile with bibliography from my_refs.bib

Claude: ✅ Camera-ready PDF generated!
```

---

## Tips & Tricks

### Tip 1: Multiple Compilation Passes

The server automatically runs multiple passes when needed:
- **Pass 1**: Generate .aux file
- **BibTeX/Biber**: Process citations
- **Pass 2**: Insert citations
- **Pass 3**: Resolve references

You don't need to do anything - it's automatic!

### Tip 2: Directory Structure

Always use relative paths in your LaTeX:

✅ Good:
```latex
\includegraphics{figures/plot.png}
\input{chapters/intro.tex}
```

❌ Bad:
```latex
\includegraphics{/absolute/path/to/plot.png}
```

### Tip 3: Asset File Types

Supported automatically:
- `.tex` - LaTeX sources
- `.bib` - Bibliographies
- `.cls` - Document classes
- `.sty` - Style packages
- `.bst` - Bibliography styles
- `.png, .jpg, .jpeg, .gif` - Images
- `.pdf, .eps, .svg` - Vector graphics

### Tip 4: Debugging

If compilation fails:
- Check logs in `logs/` directory
- Look for errors in the detailed output
- Common issues:
  - Missing packages (install with TeX Live)
  - Undefined citations (check .bib file)
  - Missing figures (check file paths)

### Tip 5: Using with AI

Best prompts:
```
✅ "Create a paper with sections X, Y, Z and compile it"
✅ "Add a figure from path/to/image.png"
✅ "Add citations for [paper names] and compile"
✅ "Fix the compilation errors"

❌ "Make it perfect" (too vague)
❌ "Add everything" (not specific)
```

---

## Advanced Examples

### Example 13: Custom Compiler

Edit `server.py` to use XeLaTeX for Unicode:

```python
COMPILER = "xelatex"  # Instead of pdflatex
```

Then:
```latex
\documentclass{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}

\begin{document}
Unicode: 你好世界 Ω α β 🎉
\end{document}
```

Perfect Unicode support!

### Example 14: Large Bibliography

```
You: I have a paper with 50+ citations in references.bib
Compile the project in /path/to/big_paper/

Claude: [handles it perfectly]
✅ All 50+ citations rendered!
(May take a bit longer)
```

### Example 15: Nested ZIP

```
You: The ZIP has another ZIP inside. Extract and compile.

Claude: [handles nested extraction]
✅ Compiled successfully!
```

---

## Troubleshooting Examples

### Issue: Citations Not Showing

**Problem:**
```
Citation [?] appears in PDF
```

**Solution:**
Check that:
1. `.bib` file is in same directory as `.tex`
2. Citation keys match: `\cite{key}` → `@article{key,...}`
3. Run multiple passes (server does this automatically)

### Issue: Figure Not Found

**Problem:**
```
LaTeX Error: File 'image.png' not found
```

**Solution:**
1. Check file exists: `ls figures/image.png`
2. Use relative path: `figures/image.png` not `/full/path`
3. Check file extension matches

### Issue: Package Not Found

**Problem:**
```
LaTeX Error: File 'algorithm.sty' not found
```

**Solution:**
```bash
# Install missing package
tlmgr install algorithms

# Or install everything (takes space)
sudo apt-get install texlive-full
```

---

## Real-World Examples

### Research Paper

**Full workflow for a machine learning paper:**

1. Start with template:
   ```
   You: Use the NeurIPS template and create a paper about transformers
   ```

2. Add content with AI help:
   ```
   You: Write the introduction discussing attention mechanisms
   ```

3. Add experiments:
   ```
   You: Add a results table comparing our method to baselines
   ```

4. Add figures:
   ```
   You: Include figures/accuracy_plot.pdf showing training curves
   ```

5. Add citations:
   ```
   You: Add citations for BERT, GPT, and T5
   ```

6. Compile:
   ```
   You: Compile the project

   Claude: ✅ Ready to submit to NeurIPS!
   ```

### Thesis

**Complete thesis with 100+ pages:**

```
thesis/
├── main.tex
├── chapters/
│   ├── 01_introduction.tex
│   ├── 02_background.tex
│   ├── 03_method.tex
│   ├── 04_experiments.tex
│   ├── 05_results.tex
│   └── 06_conclusion.tex
├── figures/
│   └── [100+ figures]
├── references.bib (500 citations)
└── appendices/
    └── proofs.tex
```

**Compile:**
```
You: Compile my thesis in /path/to/thesis/

Claude: [runs for ~1 minute due to size]
✅ Thesis compiled! 150 pages, 500 citations, 100+ figures!
```

---

Happy LaTeX-ing! 🎓📄
