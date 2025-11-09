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

### Example 3: From File

```
You: Compile the LaTeX file at /path/to/my/paper.tex

Claude: [uses compile_latex_file tool]
✅ LaTeX file compiled successfully!
```

## Available Tools

### `compile_latex`

Compiles LaTeX code directly.

**Parameters:**
- `latex_content` (required): The LaTeX source code
- `filename` (optional): Output filename without .pdf
- `auto_open` (optional): Auto-open PDF (default: true)

### `compile_latex_file`

Compiles a .tex file from disk.

**Parameters:**
- `file_path` (required): Path to the .tex file
- `auto_open` (optional): Auto-open PDF (default: true)

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

✅ Local compilation (runs on your machine)
✅ Auto-opens PDFs
✅ Supports bibliographies (auto-runs bibtex)
✅ Detailed error logs
✅ Works with any MCP client
✅ Simple setup
✅ Free and open source

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
