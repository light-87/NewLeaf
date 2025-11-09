# LaTeX MCP Server

A simple local MCP server that compiles LaTeX and opens PDFs. No cloud, no complexity - just local LaTeX compilation via AI chat.

## Quick Start

### Prerequisites

1. **TeX Live** (LaTeX compiler)
   ```bash
   # macOS
   brew install --cask mactex

   # Ubuntu/Debian
   sudo apt-get install texlive-full

   # Windows
   # Download from https://www.tug.org/texlive/
   ```

2. **Python 3.10+**
   ```bash
   python --version  # Check you have Python 3.10+
   ```

3. **Claude Desktop** (or any MCP-compatible client)
   - Download from https://claude.ai/download

### Installation

1. **Install Python dependencies**:
   ```bash
   pip install mcp
   ```

2. **Configure Claude Desktop**:

   Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or
   `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

   ```json
   {
     "mcpServers": {
       "latex": {
         "command": "python",
         "args": ["/absolute/path/to/latex-mcp/src/server.py"]
       }
     }
   }
   ```

   **Important**: Use the absolute path to `server.py`!

3. **Restart Claude Desktop**

## Usage

Just chat with Claude and ask it to compile LaTeX!

### Example 1: Simple Document

```
You: Compile this LaTeX:
\documentclass{article}
\begin{document}
Hello, World!
\end{document}

Claude: [uses compile_latex tool]
✅ LaTeX compiled successfully!
PDF: /path/to/output/document_20250109_143022.pdf
```

The PDF opens automatically!

### Example 2: Math Document

```
You: Create a LaTeX document with the Pythagorean theorem and compile it

Claude: [generates LaTeX with a² + b² = c² and compiles it]
✅ LaTeX compiled successfully!
```

### Example 3: Project with Citations

```
You: Compile the LaTeX project in /path/to/my/paper/
The directory has main.tex, references.bib, and figures/

Claude: [uses compile_latex_project tool]
✅ LaTeX project compiled successfully!
```

### Example 4: ZIP File (Overleaf Template)

```
You: Compile this Overleaf template ZIP at /path/to/template.zip

Claude: [uses compile_latex_zip tool]
✅ LaTeX ZIP compiled successfully!
```

### Example 5: Paper with Images and Citations

```
You: Create a LaTeX paper with:
- Title "My Research"
- Abstract
- Introduction with citations to \cite{einstein1905}
- A figure from figures/plot.png
- Bibliography from refs.bib

Claude: [generates LaTeX and compiles with all assets]
✅ All citations and figures rendered perfectly!
```

## Available Tools

### `compile_latex`

Compiles LaTeX code directly with full citation support.

**Parameters:**
- `latex_content` (required): The LaTeX source code
- `filename` (optional): Output filename without .pdf
- `auto_open` (optional): Auto-open PDF (default: true)

**Features:**
- Auto-detects BibTeX vs BibLaTeX
- Runs multiple passes for citations
- Handles inline bibliographies

### `compile_latex_project`

Compiles a LaTeX project directory with all assets (images, .bib files, style files).

**Parameters:**
- `project_path` (required): Path to directory containing LaTeX project
- `main_file` (optional): Name of main .tex file (auto-detected if not provided)
- `auto_open` (optional): Auto-open PDF (default: true)

**Features:**
- Auto-finds main .tex file (main.tex, paper.tex, etc.)
- Copies all assets (images, .bib, .cls, .sty files)
- Maintains directory structure
- Handles figures in subdirectories

### `compile_latex_zip`

Extract and compile a LaTeX project from a ZIP file (perfect for Overleaf templates!).

**Parameters:**
- `zip_path` (required): Path to the ZIP file
- `main_file` (optional): Name of main .tex file (auto-detected if not provided)
- `auto_open` (optional): Auto-open PDF (default: true)

**Features:**
- Extracts ZIP automatically
- Handles nested directories
- Perfect for Overleaf exports
- Works with arXiv source files

## Output

- **PDFs**: Saved to `output/` directory
- **Logs**: Saved to `logs/` directory

## Configuration

Edit `src/server.py` to customize:

```python
# Change output directory
OUTPUT_DIR = Path("/your/custom/path")

# Change compiler (pdflatex, xelatex, lualatex)
COMPILER = "xelatex"
```

## Features

✅ **Local compilation** - Runs on your machine, no cloud needed
✅ **Auto-opens PDFs** - Opens in default viewer automatically
✅ **Perfect citations** - BibTeX and BibLaTeX support with multiple compilation passes
✅ **ZIP file support** - Extract and compile Overleaf templates, arXiv papers
✅ **Images & assets** - Handles figures, graphics (.png, .jpg, .pdf, .eps, .svg)
✅ **Multi-file projects** - Supports complex projects with includes
✅ **Smart main file detection** - Auto-finds main.tex or paper.tex
✅ **Detailed error logs** - Comprehensive compilation logs
✅ **Works with any MCP client** - Claude Desktop, or any MCP-compatible AI
✅ **Simple setup** - Just install and go
✅ **Free and open source** - MIT license

## Troubleshooting

### "pdflatex: command not found"

TeX Live is not installed or not in PATH. Install it:
```bash
# macOS
brew install --cask mactex

# Linux
sudo apt-get install texlive-full
```

### PDF doesn't open automatically

Check `output/` directory for the PDF. You can open it manually.

### MCP server not connecting

1. Restart Claude Desktop
2. Check the config file path is absolute (not relative)
3. Check the path in config matches actual file location
4. Make sure `server.py` is executable: `chmod +x src/server.py`

### Compilation errors

Check the log files in `logs/` directory for detailed error messages.

## Examples

See `examples/sample.tex` for a sample document. Compile it:

```
You: Compile the LaTeX file at examples/sample.tex
```

## License

MIT - Free for everyone!

## Contributing

This is intentionally kept simple. If you want to add features:
- Keep it local (no cloud services)
- Keep it simple (no complex setup)
- Keep it free (no paid features)

Pull requests welcome!
