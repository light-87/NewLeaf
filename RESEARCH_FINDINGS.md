# Research: Overleaf-like Platform with MCP & GitHub Integration

## Executive Summary

This document presents comprehensive research findings for building a web-based collaborative LaTeX editor similar to Overleaf, with integrated MCP (Model Context Protocol) and GitHub capabilities. The platform would enable AI assistants to automatically render LaTeX documents on every GitHub commit.

---

## 1. Overleaf Architecture Analysis

### Core Architecture
- **Container-based**: Uses Docker with Phusion base-image
- **Service Management**: Runit service manager for managing services
- **Tech Stack**:
  - Frontend: React
  - Backend: Node.js (CoffeeScript/JavaScript)
  - Compiler: TeX Live (2025 currently available)
  - PDF Rendering: pdf.js in HTML canvas

### Compilation Process
1. **Server-side Compilation**: LaTeX compilation runs on backend servers (NOT in browser)
2. **TeX Live Engine**: Uses TeX Live distribution on compile servers
3. **Auto-compilation**: Automatically compiles as you type for instant preview
4. **Security**: Sandboxed compilation for multi-user environments
5. **Workflow**: Source files → LaTeX compile (via latexmk) → PDF → browser (pdf.js)

### Key Features
- Real-time collaborative editing
- Instant preview with automatic compilation
- Version control integration
- Template library
- Rich text mode alongside LaTeX

---

## 2. LaTeX Compilation & Rendering Systems

### Compilation Approaches

#### Server-Side (Recommended for Production)
**Full TeX Live Installation**
- Complete LaTeX environment on backend
- All packages and fonts available
- Mature and reliable
- Used by: Overleaf, Papeeria

**Advantages:**
- Full feature support
- Reliable compilation
- Complex document support
- Bibliography and reference handling

**Disadvantages:**
- Server resource intensive
- Requires backend infrastructure
- Scaling complexity

#### Browser-Based (Limited Use Cases)
**LaTeX.js**
- 100% JavaScript implementation
- Runs entirely in browser
- Limited package support
- Only suitable for simple documents

**Advantages:**
- No server needed
- Instant rendering
- Offline capability

**Disadvantages:**
- Limited feature set
- Cannot handle complex documents
- Package compatibility issues

### Rendering Pipeline

```
.tex files → TeX Live (latexmk) → PDF → pdf.js → HTML Canvas
```

**Key Components:**
1. **latexmk**: Automates LaTeX compilation sequence
2. **pdf.js**: Mozilla's PDF rendering library for browsers
3. **Caching**: Incremental compilation for large documents

---

## 3. Real-Time Collaborative Editing

### Core Technologies

#### WebSocket Communication
- Bidirectional real-time communication
- Client connects to server via WebSocket
- Server broadcasts updates to all connected clients
- Handle disconnections and reconnections gracefully

#### Conflict Resolution Strategies

**Operational Transformation (OT)**
- Used by Google Docs and earlier collaborative editors
- Transforms operations based on concurrent changes
- Complex to implement correctly

**Conflict-Free Replicated Data Types (CRDTs)**
- Modern approach with mathematical guarantees
- Automatically resolves conflicts
- Better for distributed systems
- Examples: Yjs, Automerge

### Implementation Best Practices
1. **Optimize Data Transfer**: Send only diffs, not entire document
2. **Graceful Reconnection**: Handle network interruptions
3. **Presence Awareness**: Show who's editing what
4. **Cursor Sharing**: Real-time cursor positions
5. **Version History**: Track all changes

### Reference Implementations
- **Overleaf**: Open-source collaborative LaTeX editor
- **Papeeria**: Feature-rich with margin discussions
- **FlyLatex**: Node.js-based real-time collaborative environment

---

## 4. GitHub Integration & Webhooks

### GitHub Actions for LaTeX

**Popular Actions:**
1. **xu-cheng/latex-action**: Uses latexmk, well-maintained
2. **dante-ev/latex-action**: Stores artifacts, PDF diffs on PRs
3. **DanySK/compile-latex-action**: Minimal configuration

### Webhook Architecture

```
GitHub Commit → Webhook → Server → Compile LaTeX → Generate PDF →
Store Artifact/Deploy
```

**Workflow:**
1. Developer commits to GitHub
2. Webhook triggers server endpoint
3. Server pulls latest changes
4. Runs LaTeX compilation
5. Uploads PDF to:
   - GitHub Releases
   - GitHub Pages (gh-pages branch)
   - Artifact storage
   - Dropbox/Cloud storage

### CI/CD Pipeline Options

**GitHub Actions (Recommended)**
- Native GitHub integration
- Free for public repos
- Configurable workflows
- Artifact storage included

**Travis CI**
- External service
- Good for cross-platform builds
- Requires separate configuration

**Self-Hosted**
- Custom webhook handlers
- Full control
- Requires infrastructure

### Implementation Steps
1. Set up webhook endpoint on server
2. Verify webhook signatures (security)
3. Pull repository changes
4. Run compilation in isolated environment
5. Store/deploy resulting PDF
6. Send status back to GitHub (commit status API)

---

## 5. Model Context Protocol (MCP) Integration

### What is MCP?

MCP is an open protocol for connecting AI assistants to external data sources and tools, introduced by Anthropic and now widely adopted.

### Major Platform Adoption (2025)

**OpenAI** (March 2025):
- ChatGPT desktop app
- Agents SDK
- Responses API

**Google DeepMind** (April 2025):
- Gemini models
- Related infrastructure

**Microsoft** (May 2025):
- Copilot Studio (GA)
- Azure OpenAI integration
- Semantic Kernel

### Integration Opportunities for LaTeX Platform

#### 1. AI-Assisted Writing
```
AI Assistant → MCP → LaTeX Server → Document Context
             ← MCP ← Suggestions   ← Current State
```

**Capabilities:**
- Context-aware suggestions
- Citation recommendations
- Grammar and style improvements
- LaTeX syntax assistance

#### 2. Reference Management
- MCP server for bibliography databases
- Auto-fetch citations from DOI/arXiv
- Integration with Zotero, Mendeley via MCP
- Semantic search for relevant papers

#### 3. Version Control Integration
```
AI Assistant → MCP → GitHub Server → Repository Access
             ← MCP ← File Context  ← Project History
```

**Use Cases:**
- Commit message generation
- Change summarization
- Merge conflict resolution
- Code review for LaTeX

#### 4. Cloud & Enterprise Integration

**MCP Servers Available (2025):**
- GitHub (official)
- Google Drive
- Slack
- Notion
- Supabase
- Postgres
- Stripe

### Implementation Architecture

```
┌─────────────────┐
│  AI Assistant   │
│  (Claude, GPT)  │
└────────┬────────┘
         │ MCP Protocol
┌────────▼────────┐
│   MCP Server    │
│  (Your LaTeX    │
│    Platform)    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│GitHub │ │ LaTeX   │
│  API  │ │Compiler │
└───────┘ └─────────┘
```

### MCP Server Components

**Resources:**
- Project files (.tex, .bib)
- Compiled PDFs
- Build logs
- Version history

**Tools:**
- compile_document
- add_citation
- create_section
- format_table
- resolve_reference

**Prompts:**
- "Help write abstract"
- "Suggest improvements"
- "Check formatting"
- "Generate bibliography"

---

## 6. LaTeX Reference Management

### BibTeX System

**How It Works:**
1. References stored in `.bib` file
2. Each entry has unique key
3. Cite in document: `\cite{key}`
4. During compilation, BibTeX formats references
5. Only cited entries appear in bibliography

**Example:**
```bibtex
@article{einstein1905,
  author = {Albert Einstein},
  title = {On the Electrodynamics of Moving Bodies},
  journal = {Annalen der Physik},
  year = {1905}
}
```

### Modern Alternatives

**BibLaTeX + Biber:**
- Full Unicode support
- Multi-language support
- More flexible formatting
- Better localization

### Reference Management Tools

**JabRef:**
- Open-source GUI for BibTeX
- Cross-platform
- Bibliography database management

**CiteDrive:**
- Online collaborative tool
- Overleaf integration
- Real-time collaboration
- BibTeX format

**Zotero + Better BibTeX:**
- Auto-updating .bib files
- Browser integration
- PDF management
- Overleaf sync

**Mendeley:**
- Reference manager
- BibTeX export
- Overleaf integration

### Automation Opportunities

**AI-Assisted Citation:**
- Extract citations from PDFs
- Auto-generate BibTeX entries
- Suggest relevant papers
- Fix formatting errors

**Integration Points:**
- DOI/arXiv lookup APIs
- CrossRef API for metadata
- Semantic Scholar API
- Google Scholar scraping

---

## 7. Proposed Architecture for MCP-GitHub-LaTeX Platform

### System Overview

```
┌──────────────────────────────────────────────────────┐
│                    Frontend Layer                     │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   React    │  │  CodeMirror  │  │   pdf.js     │ │
│  │   Editor   │  │  (LaTeX Mode)│  │  (Preview)   │ │
│  └──────┬─────┘  └──────┬───────┘  └──────┬───────┘ │
└─────────┼────────────────┼──────────────────┼─────────┘
          │                │                  │
      WebSocket         HTTP/REST          HTTP/REST
          │                │                  │
┌─────────▼────────────────▼──────────────────▼─────────┐
│                   Backend Layer (Node.js)              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │  WebSocket   │  │     API      │  │    MCP      │ │
│  │   Server     │  │   Gateway    │  │   Server    │ │
│  │   (CRDT)     │  │              │  │             │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘ │
└─────────┼──────────────────┼──────────────────┼────────┘
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼────────┐
│                   Services Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Compilation  │  │   GitHub     │  │  Reference   │ │
│  │   Service    │  │   Service    │  │   Manager    │ │
│  │  (TeX Live)  │  │  (Webhooks)  │  │  (BibTeX)    │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼─────────┐
│                    Storage Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  PostgreSQL  │  │     Redis    │  │  S3/Blob     │  │
│  │  (Metadata)  │  │    (Cache)   │  │   (PDFs)     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### Frontend Components

**1. Editor (React + CodeMirror)**
- Syntax highlighting for LaTeX
- Auto-completion (commands, citations)
- Split view: source and preview
- Cursor synchronization

**2. Preview Panel**
- pdf.js for rendering
- Auto-scroll synchronization
- Error highlighting
- Live updates

**3. Collaboration UI**
- User presence indicators
- Real-time cursors
- Comment system
- Change tracking

#### Backend Services

**1. WebSocket Server**
- CRDT implementation (Yjs recommended)
- Broadcast text changes
- Presence synchronization
- Room management

**2. Compilation Service**
- Docker containers for isolation
- TeX Live 2025
- latexmk for compilation
- Error parsing and reporting
- Incremental builds

**3. GitHub Service**
- Webhook receiver
- OAuth authentication
- Repository sync
- Commit status updates
- PR integration

**4. MCP Server**
- Expose LaTeX operations as MCP tools
- Provide document context to AI
- Handle AI-generated content
- Reference management integration

**5. Reference Manager**
- BibTeX parser
- Citation database
- DOI/arXiv lookup
- Auto-formatting

### Data Flow Examples

#### Scenario 1: User Edits Document

```
1. User types in editor
2. Frontend sends change via WebSocket
3. CRDT server processes change
4. Broadcast to other users
5. Queue compilation job
6. Compile LaTeX → PDF
7. Send PDF to frontend
8. Update preview
```

#### Scenario 2: GitHub Commit Triggers Compilation

```
1. Developer pushes to GitHub
2. GitHub webhook → Platform
3. Platform pulls latest changes
4. Trigger compilation service
5. Generate PDF
6. Upload to GitHub Release
7. Update commit status
8. Notify collaborators
```

#### Scenario 3: AI Assistant Helps via MCP

```
1. User invokes AI assistant
2. AI connects via MCP
3. AI reads document context
4. AI suggests improvements
5. User accepts suggestion
6. Changes propagate via WebSocket
7. Auto-compile triggers
8. Preview updates
```

---

## 8. Technology Stack Recommendation

### Frontend
- **Framework**: React 18+
- **Editor**: CodeMirror 6 (LaTeX mode)
- **PDF Viewer**: pdf.js
- **CRDT**: Yjs
- **State Management**: Zustand or Redux Toolkit
- **Styling**: Tailwind CSS
- **Build Tool**: Vite

### Backend
- **Runtime**: Node.js 20+ (LTS)
- **Framework**: Express.js or Fastify
- **WebSocket**: Socket.io or ws
- **MCP**: @modelcontextprotocol/sdk
- **Authentication**: Passport.js (GitHub OAuth)
- **API**: RESTful + GraphQL (optional)

### Services
- **LaTeX**: TeX Live 2025 in Docker
- **Compiler**: latexmk
- **Queue**: BullMQ (Redis-based)
- **File Storage**: MinIO or S3
- **Database**: PostgreSQL 16+
- **Cache**: Redis 7+

### Infrastructure
- **Containers**: Docker + Docker Compose
- **Orchestration**: Kubernetes (for scale)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack or Loki

### Security
- **Sandboxing**: Docker with resource limits
- **Secrets**: HashiCorp Vault or environment variables
- **Authentication**: OAuth 2.0
- **Authorization**: RBAC
- **Rate Limiting**: Redis-based

---

## 9. Implementation Phases

### Phase 1: MVP (3-4 months)
**Core Features:**
- [x] Basic LaTeX editor (CodeMirror)
- [x] Server-side compilation (TeX Live)
- [x] PDF preview (pdf.js)
- [x] User authentication
- [x] File management
- [x] GitHub OAuth

**No collaboration yet, single-user focus**

### Phase 2: Collaboration (2-3 months)
**Add:**
- [x] Real-time editing (Yjs + WebSocket)
- [x] Multi-user support
- [x] Presence indicators
- [x] Conflict resolution
- [x] Version history

### Phase 3: GitHub Integration (2 months)
**Add:**
- [x] Repository sync
- [x] Webhook integration
- [x] Auto-compilation on commit
- [x] GitHub Actions integration
- [x] Commit status updates
- [x] PR preview links

### Phase 4: MCP Integration (2-3 months)
**Add:**
- [x] MCP server implementation
- [x] AI assistant integration
- [x] Context-aware suggestions
- [x] Citation assistance
- [x] Auto-formatting tools
- [x] Content generation

### Phase 5: Advanced Features (ongoing)
**Add:**
- [x] Template library
- [x] Advanced reference management
- [x] Figure/table managers
- [x] Custom packages
- [x] Export options
- [x] Mobile support

---

## 10. Key Challenges & Solutions

### Challenge 1: Compilation Performance
**Problem**: LaTeX compilation can be slow for large documents

**Solutions:**
- Incremental compilation (only changed sections)
- Caching intermediate files
- Pre-compiled headers
- Parallel compilation for multi-file projects
- Fast preview mode (draft quality)

### Challenge 2: Sandboxing Security
**Problem**: User LaTeX code can execute arbitrary commands

**Solutions:**
- Docker containers with resource limits
- Disable shell-escape by default
- Whitelist allowed packages
- Network isolation
- File system restrictions
- Timeout mechanisms

### Challenge 3: Scaling WebSockets
**Problem**: Many concurrent users with real-time updates

**Solutions:**
- Redis adapter for Socket.io (multi-server)
- Room-based isolation
- Message throttling
- Horizontal scaling
- Load balancing (sticky sessions)

### Challenge 4: Storage Costs
**Problem**: PDFs and project files accumulate quickly

**Solutions:**
- Compression (gzip PDFs)
- Lifecycle policies (auto-delete old versions)
- Tiered storage (hot/cold)
- User quotas
- Deduplication

### Challenge 5: MCP Integration Complexity
**Problem**: Coordinating AI actions with user edits

**Solutions:**
- Operation queuing
- Conflict detection
- User approval workflows
- Undo/redo support
- Clear AI attribution

---

## 11. Competitive Analysis

### Overleaf
**Strengths:**
- Mature, stable platform
- Large template library
- University partnerships
- Git integration
- Rich text mode

**Limitations:**
- Proprietary (freemium model)
- Limited AI integration
- No MCP support
- Compilation speed

**Our Advantage:**
- Native AI integration via MCP
- GitHub-first workflow
- Modern tech stack
- Open source potential

### Papeeria
**Strengths:**
- Auto-compilation
- Margin discussions
- Clean UI

**Limitations:**
- Smaller community
- Limited integrations
- No AI features

**Our Advantage:**
- MCP integration
- GitHub workflows
- Better collaboration tools

### ShareLaTeX / Overleaf Community
**Strengths:**
- Open source
- Self-hostable
- Customizable

**Limitations:**
- Outdated tech stack
- Complex setup
- Limited modern features

**Our Advantage:**
- Modern architecture
- Cloud-native
- AI-first design

---

## 12. Business Model Considerations

### Free Tier
- Public projects
- Basic compilation
- Limited storage (1 GB)
- Community templates
- Basic MCP features

### Pro Tier ($10-15/month)
- Private projects
- Faster compilation
- More storage (10 GB)
- Priority support
- Advanced MCP features
- Unlimited collaborators

### Team Tier ($30-50/user/month)
- Organization accounts
- SSO integration
- Admin controls
- Usage analytics
- Custom branding
- Dedicated resources

### Enterprise
- Self-hosted option
- SLA guarantees
- Custom integrations
- Training & support
- Volume licensing

---

## 13. Next Steps

### Immediate Actions

1. **Prototype Basic Editor**
   - Set up React + CodeMirror
   - Implement basic LaTeX highlighting
   - Create simple compilation pipeline

2. **Docker Setup**
   - Create TeX Live Docker image
   - Set up compilation service
   - Test latexmk integration

3. **MCP Proof of Concept**
   - Implement basic MCP server
   - Test with Claude desktop app
   - Create simple LaTeX tools

4. **GitHub Integration Test**
   - Set up webhook receiver
   - Test compilation trigger
   - Verify artifact upload

### Research Gaps to Fill

1. **Performance Benchmarks**
   - Test compilation speed vs Overleaf
   - WebSocket message throughput
   - CRDT performance at scale

2. **User Research**
   - Survey potential users
   - Interview researchers/academics
   - Identify killer features

3. **Legal & Compliance**
   - Open source licensing
   - GDPR compliance
   - University data policies

---

## 14. References & Resources

### Open Source Projects
- **Overleaf**: https://github.com/overleaf/overleaf
- **FlyLatex**: https://github.com/alabid/flylatex
- **Yjs**: https://github.com/yjs/yjs
- **pdf.js**: https://github.com/mozilla/pdf.js

### Documentation
- **MCP Specification**: https://modelcontextprotocol.io/
- **LaTeX Project**: https://www.latex-project.org/
- **TeX Live**: https://www.tug.org/texlive/
- **CodeMirror**: https://codemirror.net/

### APIs & Tools
- **GitHub API**: https://docs.github.com/en/rest
- **CrossRef API**: https://www.crossref.org/documentation/
- **arXiv API**: https://arxiv.org/help/api/
- **Semantic Scholar**: https://www.semanticscholar.org/product/api

### Learning Resources
- **CRDT Explainer**: https://crdt.tech/
- **WebSocket Guide**: https://javascript.info/websocket
- **LaTeX Compilation**: https://mg.readthedocs.io/latexmk.html

---

## Conclusion

Building an Overleaf-like platform with MCP and GitHub integration is technically feasible and offers significant advantages over existing solutions. The key differentiators are:

1. **AI-First Design**: Native MCP integration for AI-assisted writing
2. **GitHub-Native**: First-class Git integration with auto-compilation
3. **Modern Architecture**: React, Node.js, CRDT-based collaboration
4. **Open Ecosystem**: MCP enables integration with any AI assistant

**Estimated Timeline**: 12-15 months for full v1.0 release
**Team Size**: 3-5 developers (1 frontend, 2 backend, 1 DevOps, 1 AI/MCP specialist)
**Infrastructure Cost**: ~$500-1000/month for MVP (scales with users)

The project is ambitious but achievable with the right team and phased approach. Starting with a solid MVP focusing on core editor + compilation, then layering collaboration, GitHub, and MCP features is recommended.
