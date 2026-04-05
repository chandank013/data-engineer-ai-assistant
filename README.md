# 🤖 AI Data Engineer Assistant

An intelligent and efficient web application for *big data analytics* — featuring AI-powered natural language querying, Apache Spark distributed processing, Hadoop YARN cluster management, and comprehensive multi-source data analysis — *through an intuitive browser-based interface with seamless real-time interaction*.

🎯 *GitHub Repository:*
👉 [https://github.com/chandank013/ai-data-engineer-assistant](https://github.com/chandank013/ai-data-engineer-assistant)

*Live Demo:*
👉 [Run locally at http://localhost:5000](http://localhost:5000)

---

<p align="center">
  <img src="docs/page-01.png" width="45%" />
  <img src="docs/page-02.png" width="45%" />
  <img src="docs/page-03.png" width="45%" />
  <img src="docs/page-04.png" width="45%" />
  <img src="docs/page-05.png" width="45%" />
  <img src="docs/page-06.png" width="45%" />
</p>

---

Built using **Flask**, **Apache Spark 3.5.1**, **Hadoop 3.3.6**, **LangChain**, **Groq LLM API**, **FAISS**, and **PySpark**, this project transforms traditional data engineering workflows into a **smart, conversational, and cluster-powered analytics platform**. 📊🐘⚡

---

## 🧑‍💻 Team Members

| Name | Roll No. | Contributions |
|------|----------|---------------|
| **Anchal Jaiswal** | 24BDS003 | Designed the complete user interface and user experience. Implemented the customer-facing Spark Analytics and NL→SQL pages. Built the Schema Explorer with live SVG ER diagram and FK inference. Created the feedback and review system interface. |
| **Chandan Kumar** | 24BDS013 | Developed the Hadoop WSL2 pseudo-distributed cluster setup (7-phase pipeline). Integrated HDFS auto-sync on file upload. Built the `hadoop/` Python package for clean infrastructure separation. Created report, README, and presentation. |
| **Nitish Naveen** | 24BDS050 | Built the PDF RAG pipeline using FAISS and sentence-transformers. Implemented the JSON Analytics module with PySpark DataFrame engine. Developed the AI Chat agent with LangChain multi-tool reasoning. Worked on git operations and presentations. |
| **Prem Kishan** | 24BDS057 | Implemented the Flask REST API layer and all backend routes. Configured PySpark session management and YARN integration. Built the HDFS File Manager with per-file delete operations. Managed deployment, testing, and `.env` configuration. |

---

## 🧰 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Flask 3.0** | Python REST API backend and static file serving |
| **Python 3.11** | Primary development language for all backend logic |
| **Apache Spark 3.5.1 + PySpark** | Distributed SQL query execution on CSV/XLSX/JSON datasets |
| **Hadoop 3.3.6** | HDFS distributed file storage + YARN cluster resource management |
| **LangChain 0.2** | LLM orchestration, SQL agents, and RAG pipeline |
| **Groq API (llama-3.1-8b-instant)** | LLM for NL→SQL generation, explanations, and chat responses |
| **FAISS (CPU)** | Vector similarity search for PDF retrieval-augmented generation |
| **sentence-transformers** | `all-MiniLM-L6-v2` embeddings for PDF document chunks |
| **Pandas + OpenPyXL** | CSV, XLSX, and JSON data ingestion and preview |
| **SQLAlchemy + PyMySQL** | SQLite and MySQL database connectivity |
| **JavaScript ES2022** | Single-page frontend application (no framework) |
| **Tailwind CSS (CDN)** | Utility-first responsive UI design |

---

## 🚀 Features

### For Data Analysts 👥
- ⚡ **Spark Analytics** — Ask questions in plain English; system generates and runs Spark SQL automatically
- 🤖 **AI Explanations** — Every query result includes a natural-language explanation from the LLM
- 🔍 **NL→SQL Engine** — Query SQLite and MySQL databases conversationally
- 📄 **PDF Q&A** — Upload any PDF and ask questions; answers are grounded in the document
- 📊 **JSON Analytics** — Analyze nested JSON files with LLM-driven statistical summaries
- 🗂 **Schema Explorer** — Live ER diagram with auto-inferred foreign keys for any SQLite or MySQL database
- 💬 **AI Chat Agent** — Multi-turn conversational assistant with web search, Wikipedia, and ArXiv tools
- 📁 **Dataset Manager** — Upload CSV, XLSX, JSON, and PDF files with instant preview

### For Administrators / Caterers 👨‍🍳
- 🐘 **HDFS File Manager** — View, manage, and delete files on HDFS directly from the browser
- ⚙ **Spark Mode Switcher** — Toggle between Local, YARN, and Standalone modes from Settings
- 📋 **Execution Environment Panel** — Live view of current Spark mode, HDFS connection, memory, and executors
- 🔌 **Connection Tester** — Verify Flask backend reachability from the UI
- 🛠 **`.env` Snippet Generator** — Copy-ready configuration blocks for all three Spark modes

---

## 🎯 Key Functionalities

### ⚡ Spark Analytics Module
- **Natural Language to SQL**: Type a question like "show total sales by region" and PySpark executes it automatically
- **YARN Integration**: Jobs run on Hadoop YARN cluster with real-time progress tracking (5-step indicator)
- **HDFS Auto-Read**: When HDFS is configured, Spark reads directly from `hdfs://localhost:9000/data/raw/`
- **AI Explanation**: After execution, the LLM explains the result in plain English with a 📋 Copy button
- **Java Smart Detection**: Auto-detects Java 17 in WSL2 paths, sets `JAVA_HOME` dynamically

### 🤖 NL→SQL Engine
- **Dual Database Support**: Works with SQLite files and live MySQL server connections
- **Two Modes**: Direct mode (single LLM call, < 3 s) and Agent mode (multi-step reasoning, 5–15 s)
- **Friendly Error Messages**: Specific, actionable messages for MySQL connection refused, access denied, and unknown database
- **Schema-Aware**: Reads actual table structure before generating SQL for higher accuracy

### 📄 PDF Retrieval-Augmented Generation
- **Chunked Indexing**: 1,000-character chunks with 200-character overlap for optimal retrieval
- **Persistent FAISS Index**: Vector index saved to disk and reloaded between sessions
- **Top-5 Retrieval**: Most relevant chunks fetched and passed to LLM with a question-answering prompt
- **Source Grounding**: Answers cite the uploaded document, preventing hallucination

### 🗂 Schema Explorer & ER Diagram
- **Live Connection**: Connects to SQLite or MySQL and enumerates all tables and columns
- **FK Inference**: Detects foreign keys from column naming (e.g., `order_id` → `orders` table)
- **Interactive SVG**: Full ER diagram rendered in-browser — no server-side image generation
- **Standard Notation**: Filled-arrow and open-circle relationship connectors with pill-shaped labels

### 🐘 HDFS Auto-Sync
- **Trigger on Upload**: Every dataset uploaded via the browser is automatically pushed to HDFS
- **Transparent Skip**: If `HDFS_NAMENODE` is not set, the upload completes silently without error
- **Instant Confirmation**: Upload response includes HDFS sync status (`🐘 Synced to HDFS`)
- **Latency**: ~2.1 seconds average sync time for typical CSV files

### 🔄 Hadoop Utility Package (`hadoop/`)
- **`hdfs_client.py`**: Upload, delete, list files on HDFS via the `hdfs dfs` CLI
- **`yarn_monitor.py`**: Query YARN ResourceManager status and list running applications
- **`hdfs_sync.py`**: Bulk-sync the entire `data/` folder to HDFS in one command
- **`setup_hdfs_dirs.py`**: One-time creation of `/data/raw`, `/data/processed`, and `/spark-jars/`
- **`upload_spark_jars.py`**: Cache all 250+ PySpark JARs to HDFS — cuts YARN cold-start from 74 s to 18 s
- **`health_check.py`**: Pre-flight diagnostic verifying env vars, Java, HDFS, YARN, and jps daemons

---

## 🎯 System Workflow

### Analyst Journey (Spark Analytics)
1. **Upload Dataset** → CSV, XLSX, or JSON via Datasets tab
2. **Auto-Sync to HDFS** → File pushed to `hdfs:///data/raw/` (if configured)
3. **Type NL Query** → E.g., "find top 5 products by revenue"
4. **LLM Generates SQL** → Groq API translates to Spark SQL
5. **YARN Executes** → PySpark submits job to ResourceManager
6. **View Results** → Table with row count displayed in browser
7. **Read Explanation** → LLM explains what the result means

### Analyst Journey (NL→SQL)
1. **Connect Database** → SQLite file or MySQL credentials
2. **Load Schema** → Tables and columns fetched automatically
3. **Ask Question** → Natural language query entered
4. **SQL Generated & Run** → Direct or Agent mode
5. **Results + Explanation** → Table and AI explanation returned

### Caterer / Admin Journey (Hadoop)
1. **Run Health Check** → `python hadoop/health_check.py`
2. **Setup HDFS Dirs** → `python hadoop/setup_hdfs_dirs.py`
3. **Upload Spark JARs** → `python hadoop/upload_spark_jars.py`
4. **Start Hadoop** → `start-dfs.sh && start-yarn.sh`
5. **Update .env** → Switch `SPARK_MASTER=yarn`
6. **Restart Flask** → `python app.py` (from WSL2)
7. **Monitor from UI** → Settings → HDFS Status & Files

---

## 🧩 Project Structure

```text
ai-data-engineer-assistant/
│
├── hadoop/                      # Hadoop/HDFS utility package
│   ├── __init__.py
│   ├── hdfs_client.py           # Upload, delete, list on HDFS
│   ├── yarn_monitor.py          # YARN status and app listing
│   ├── hdfs_sync.py             # Bulk sync data/ → HDFS
│   ├── setup_hdfs_dirs.py       # One-time HDFS directory setup
│   ├── upload_spark_jars.py     # Cache PySpark JARs on HDFS
│   └── health_check.py          # Pre-flight diagnostic
│
├── config/                      # Spark and app configuration
│   ├── __init__.py
│   ├── settings.py              # App-wide constants and env reads
│   └── spark_config.py          # PySpark session builder
│
├── llm/                         # LLM integration
│   ├── __init__.py
│   └── groq_llm.py              # Groq API wrapper via LangChain
│
├── tools/                       # LangChain tool definitions
│   ├── __init__.py
│   ├── spark_tool.py            # Spark SQL execution tool
│   ├── sql_tool.py              # SQL agent and raw SQL runner
│   ├── pdf_tool.py              # FAISS-backed PDF retriever
│   └── web_tools.py             # Web search, Wikipedia, ArXiv
│
├── rag/                         # Retrieval-augmented generation
│   ├── __init__.py
│   ├── embeddings.py            # sentence-transformers setup
│   ├── ingest.py                # PDF chunking and indexing
│   └── retriever.py             # FAISS similarity search
│
├── agents/                      # LangChain agent builders
│   ├── __init__.py
│   └── agent_builder.py         # Multi-tool conversational agent
│
├── utils/                       # Shared utilities
│   ├── __init__.py
│   ├── logger.py                # Structured logging
│   └── helpers.py               # File utilities and validators
│
├── data/
│   ├── raw/                     # Uploaded CSV, XLSX, JSON files
│   └── processed/               # Cleaned or transformed data
│
├── vectorstore/
│   └── faiss_index/             # Persisted FAISS vector index
│
├── templates/
│   └── index.html               # Single-page frontend application
│
├── app.py                       # Flask application and all API routes
├── requirements.txt             # Python dependencies
├── env_template.txt             # Environment variable template
├── SETUP.txt                    # Step-by-step setup guide
└── README.md                    # Project documentation
```

---

## ⚙ Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Node.js not required (pure Python backend)
- Java JDK 17 (required for PySpark)
- Hadoop 3.3.6 (optional — for YARN cluster mode)
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Clone the repository

```bash
git clone https://github.com/your-username/ai-data-engineer-assistant.git
cd ai-data-engineer-assistant
```

### Rename flat output files into subfolders

```bash
mkdir -p config llm tools rag agents utils templates static

mv config__settings.py      config/settings.py
mv config__spark_config.py  config/spark_config.py
mv llm__groq_llm.py         llm/groq_llm.py
mv agents__agent_builder.py agents/agent_builder.py
mv tools__spark_tool.py     tools/spark_tool.py
mv tools__sql_tool.py       tools/sql_tool.py
mv tools__pdf_tool.py       tools/pdf_tool.py
mv tools__web_tools.py      tools/web_tools.py
mv rag__embeddings.py       rag/embeddings.py
mv rag__ingest.py           rag/ingest.py
mv rag__retriever.py        rag/retriever.py
mv utils__logger.py         utils/logger.py
mv utils__helpers.py        utils/helpers.py
mv index.html               templates/index.html

# Create __init__.py in each package
touch config/__init__.py llm/__init__.py tools/__init__.py
touch rag/__init__.py agents/__init__.py utils/__init__.py hadoop/__init__.py
```

### Create required directories

```bash
mkdir -p data/raw data/processed uploads vectorstore/faiss_index
```

### Install Python dependencies

```bash
pip install -r requirements.txt
```

### Install Java 17 (required for PySpark)

```bash
# Ubuntu / WSL2
sudo apt update && sudo apt install openjdk-17-jdk -y
java -version   # should print openjdk 17.0.x

# macOS
brew install openjdk@17

# Windows — download from https://adoptium.net
```

### Configure environment variables

Rename `env_template.txt` to `.env` and fill in your values:

```env
# Groq LLM API (get free key at console.groq.com)
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.1-8b-instant

# Flask server
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=true

# Java (required for PySpark)
# WSL2 / Linux:
JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
# Windows (after installing Adoptium JDK 17):
# JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-17.0.10.7-hotspot

# Spark mode — choose one:
SPARK_MASTER=local[*]             # Development (no cluster needed)
# SPARK_MASTER=yarn               # Hadoop YARN cluster

# Hadoop (only needed for YARN mode)
# HDFS_NAMENODE=hdfs://localhost:9000
# YARN_RESOURCE_MANAGER=localhost:8032
# HADOOP_CONF_DIR=/home/youruser/hadoop/etc/hadoop
# SPARK_YARN_JARS=hdfs://localhost:9000/spark-jars/*

# Embedding model
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Run the development server

```bash
python app.py
```

### Open in browser

```
http://localhost:5000
```

---

## 🐘 Hadoop YARN Setup (Optional — for Distributed Mode)

Follow these 7 phases to set up a pseudo-distributed Hadoop cluster on WSL2:

| Phase | Action | Key Command |
|-------|--------|-------------|
| **1** | Install WSL2 + Java 17 | `sudo apt install openjdk-17-jdk -y` |
| **2** | Download Hadoop 3.3.6 | `wget .../hadoop-3.3.6.tar.gz && tar -xzf ...` |
| **3** | Set env variables | Add `JAVA_HOME`, `HADOOP_HOME`, `PATH` to `~/.bashrc` |
| **4** | Configure XML files | Edit `core-site.xml`, `hdfs-site.xml`, `yarn-site.xml` |
| **5** | Setup SSH + format HDFS | `ssh-keygen` → `hdfs namenode -format` |
| **6** | Start services + verify | `start-dfs.sh && start-yarn.sh` → `jps` |
| **7** | Update `.env` + restart Flask | Set `SPARK_MASTER=yarn` → `python app.py` |

After setup, run the pre-flight check:

```bash
python hadoop/health_check.py
```

Upload Spark JARs to HDFS (one-time, cuts cold start from 74 s → 18 s):

```bash
python hadoop/setup_hdfs_dirs.py
python hadoop/upload_spark_jars.py
```

Web UIs available after startup:
- HDFS NameNode: `http://localhost:9870`
- YARN ResourceManager: `http://localhost:8088`

---

## 📊 Database Schema

### Data Directory Structure

```
data/
├── raw/              ← Uploaded CSV, XLSX, JSON datasets
│                        Auto-synced to HDFS when configured
└── processed/        ← Transformed or cleaned outputs
```

### HDFS Layout (YARN mode)

```
hdfs://localhost:9000/
├── data/
│   ├── raw/          ← Mirrors data/raw/ from local disk
│   └── processed/    ← Mirrors data/processed/
├── spark-jars/       ← 250+ cached PySpark JARs (avoids re-upload)
└── tmp/
    └── spark-logs/   ← YARN application logs
```

### FAISS Vector Index

```
vectorstore/
└── faiss_index/
    ├── index.faiss   ← Binary vector index (all-MiniLM-L6-v2 embeddings)
    └── index.pkl     ← Document chunk metadata and text
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/files` | List all uploaded datasets |
| `GET` | `/api/pdfs` | List all uploaded PDF files |
| `GET` | `/api/databases` | List SQLite database files |
| `POST` | `/api/upload` | Upload a CSV, XLSX, JSON, or PDF file |
| `DELETE` | `/api/delete` | Delete a dataset from local disk |
| `POST` | `/api/preview` | Preview first 20 rows of a dataset |
| `POST` | `/api/spark` | NL query → Spark SQL → results + explanation |
| `GET` | `/api/spark/mode` | Get current Spark mode (local / YARN / standalone) |
| `GET` | `/api/spark/java` | Check Java installation status |
| `POST` | `/api/stats` | Dataset statistics (row count, column types) |
| `POST` | `/api/sql/schema` | Load database schema |
| `POST` | `/api/sql/query` | NL → SQL → results + explanation |
| `POST` | `/api/sql/raw` | Execute raw SQL directly |
| `POST` | `/api/json/analyze` | LLM-driven JSON analysis |
| `POST` | `/api/json/query` | NL query against JSON file |
| `POST` | `/api/chat` | Multi-turn AI chat with web search tools |
| `POST` | `/api/pdf/ask` | PDF question answering via RAG |
| `GET` | `/api/hdfs/status` | List files on HDFS |
| `POST` | `/api/hdfs/delete` | Delete a file from HDFS |
| `GET` | `/api/ping` | Health check — verifies Flask is running |

---

## 🎨 UI Modules

### Customer / Analyst Interface
- **Overview Dashboard**: Live stat cards — total files, Spark mode, HDFS status, executors
- **Datasets Tab**: Drag-and-drop upload zone, file table with preview button
- **Spark Analytics**: NL query input, 5-step progress tracker, result table, AI explanation with copy
- **NL→SQL**: Database connection panel, direct and agent modes, generated SQL viewer
- **Raw SQL**: Direct SQL editor with execute button
- **Schema Explorer**: ER diagram with FK arrows, table/column list panel
- **AI Chat**: Multi-turn chat with markdown rendering and edit message feature
- **PDF Q&A**: PDF file selector, question input, grounded answer display
- **JSON Analytics**: JSON file upload, descriptive stats, LLM analysis
- **Settings**: Connection tester, `.env` snippet tabs, HDFS File Manager, Execution Environment panel

---

## 📈 Results & Performance

- ⚡ **8.2 s** median Spark query latency in local mode
- 🐘 **18.5 s** median YARN warm-run latency (2nd+ query in session)
- 📦 **74.3 s** YARN cold-start (1st query after cluster restart) — reduced to 18 s after JAR caching
- 🎯 **90% NL-to-SQL** generation accuracy (18/20 queries produced valid SQL)
- ✅ **88.9% exact-match** accuracy against hand-written reference queries
- 🔄 **2.1 s** HDFS auto-sync time for typical CSV files
- 💬 **< 3 s** NL→SQL direct mode latency
- 📄 **3.1 s** PDF RAG retrieval + generation latency

---

## 🔮 Future Enhancements

- 🦙 **Local LLM Support**: Swap Groq API for Ollama (`llama3`, `nomic-embed-text`) — zero internet, zero API cost
- 👥 **Multi-Node Cluster**: Scale from WSL2 to a 4-node Hadoop cluster (only 5 config changes needed)
- 💳 **Authentication**: User login, personal API key management, session history
- 📱 **Mobile Responsive**: Optimized layouts for tablet and mobile browsers
- 🔔 **Spark Job Notifications**: Push alerts when long-running YARN jobs complete
- 📊 **Advanced Visualisations**: Plotly charts auto-generated from Spark results
- 🏪 **Data Catalog**: Auto-profile uploaded datasets with column statistics and data quality scores
- 🔁 **Scheduled Jobs**: CRON-style recurring Spark queries with result archiving
- 🌐 **Multi-Language UI**: Support for regional language interfaces

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Contact & Support

For questions, suggestions, or issues:

- **GitHub Issues**: [Report a bug](https://github.com/your-username/ai-data-engineer-assistant/issues)
- **Email**: 24bds013@iiitdwd.ac.in

---

## 🙏 Acknowledgments

- **IIIT Dharwad** for providing resources and support
- **Dr. Animesh Chaturvedi Sir** for guidance on the project
- **Groq** for blazing-fast LLM inference via the llama-3.1-8b-instant model
- **Apache Hadoop & Spark** communities for excellent documentation
- **LangChain** for the composable LLM orchestration framework
- **FAISS** (Meta Research) for efficient vector similarity search
- **Hugging Face** for the `all-MiniLM-L6-v2` embedding model

---

## 💡 Authors

**Team AI Data Engineers — DSAI, IIIT Dharwad**

Built with ❤️ using Flask, Apache Spark, Hadoop YARN, LangChain, Groq LLM, FAISS, and plain JavaScript.

---

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)](https://github.com/your-username/ai-data-engineer-assistant)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5.1-orange?style=for-the-badge&logo=apachespark)](https://spark.apache.org)
[![Hadoop](https://img.shields.io/badge/Hadoop-3.3.6-yellow?style=for-the-badge&logo=apachehadoop)](https://hadoop.apache.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-purple?style=for-the-badge)](https://langchain.com)

---

*⭐ If you find this project helpful, please consider giving it a star on GitHub!*