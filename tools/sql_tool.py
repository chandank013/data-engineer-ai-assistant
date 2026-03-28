# tools/sql_tool.py
# SQL analytics tool — SQLite (local file) and MySQL.
# MySQL uses PyMySQL driver (pure Python, no native lib needed) with
# mysql-connector-python as fallback.

from __future__ import annotations
from urllib.parse import quote_plus


# ─── Connection string builder ─────────────────────────────────────────────────

def _mysql_url(host: str, port: int, user: str, password: str, database: str) -> str:
    """
    Build a SQLAlchemy MySQL URL.
    Tries pymysql first (pure Python, easier to install),
    falls back to mysql+mysqlconnector.
    """
    pw = quote_plus(password)
    try:
        import pymysql  # noqa: F401
        return f"mysql+pymysql://{user}:{pw}@{host}:{port}/{database}"
    except ImportError:
        try:
            import mysql.connector  # noqa: F401
            return f"mysql+mysqlconnector://{user}:{pw}@{host}:{port}/{database}"
        except ImportError:
            raise ImportError(
                "No MySQL driver found. Install one:\n"
                "  pip install pymysql          (recommended)\n"
                "  pip install mysql-connector-python"
            )


# ─── LangChain SQLDatabase wrappers ───────────────────────────────────────────

def get_sqlite_db(db_path: str):
    """Return a read-only LangChain SQLDatabase for a local SQLite file."""
    import sqlite3
    from pathlib import Path
    from sqlalchemy import create_engine
    from langchain_community.utilities import SQLDatabase

    abs_path = str(Path(db_path).absolute())
    creator = lambda: sqlite3.connect(f"file:{abs_path}?mode=ro", uri=True)
    engine = create_engine("sqlite:///", creator=creator)
    return SQLDatabase(engine)


def get_mysql_db(host: str, port: int, user: str, password: str, database: str):
    """Return a LangChain SQLDatabase for a MySQL connection."""
    from sqlalchemy import create_engine
    from langchain_community.utilities import SQLDatabase

    url = _mysql_url(host, port, user, password, database)
    engine = create_engine(url, connect_args={"connect_timeout": 10})
    return SQLDatabase(engine)


# ─── LangChain SQL Agent ───────────────────────────────────────────────────────

def build_sql_agent(db, llm):
    """Build a LangChain SQL agent (ZERO_SHOT_REACT_DESCRIPTION)."""
    from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
    from langchain.agents import create_sql_agent, AgentType

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    return create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )


# ─── Raw SQL execution ─────────────────────────────────────────────────────────

def run_raw_sql_sqlite(db_path: str, sql: str) -> dict:
    """Execute SQL on SQLite and return {columns, rows, row_count}."""
    import sqlite3
    from pathlib import Path

    conn = sqlite3.connect(str(Path(db_path).absolute()))
    try:
        cur = conn.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = [list(r) for r in cur.fetchall()]
        return {"columns": cols, "rows": rows, "row_count": len(rows)}
    finally:
        conn.close()


def run_raw_sql_mysql(host: str, port: int, user: str,
                      password: str, database: str, sql: str) -> dict:
    """Execute SQL on MySQL and return {columns, rows, row_count}."""
    from sqlalchemy import create_engine, text

    url = _mysql_url(host, port, user, password, database)
    engine = create_engine(url, connect_args={"connect_timeout": 10})
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        cols = list(result.keys()) if result.returns_rows else []
        rows = [list(r) for r in result.fetchall()] if result.returns_rows else []
    return {"columns": cols, "rows": rows, "row_count": len(rows)}


# ─── Schema introspection ──────────────────────────────────────────────────────

def get_sqlite_schema(db_path: str) -> dict:
    """Return {tables, schema} for a SQLite database."""
    import sqlite3
    from pathlib import Path

    conn = sqlite3.connect(str(Path(db_path).absolute()))
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [r[0] for r in cur.fetchall()]
        schema = {}
        for t in tables:
            cur.execute(f"PRAGMA table_info([{t}])")
            schema[t] = [{"name": r[1], "type": r[2]} for r in cur.fetchall()]
        row_counts = {}
        for t in tables:
            try:
                cur.execute(f"SELECT COUNT(*) FROM [{t}]")
                row_counts[t] = cur.fetchone()[0]
            except Exception:
                row_counts[t] = "?"
        return {"tables": tables, "schema": schema, "row_counts": row_counts}
    finally:
        conn.close()


def get_mysql_schema(host: str, port: int, user: str, password: str, database: str) -> dict:
    """Return {tables, schema, row_counts} for a MySQL database."""
    from sqlalchemy import create_engine, text, inspect

    url = _mysql_url(host, port, user, password, database)
    engine = create_engine(url, connect_args={"connect_timeout": 10})
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    schema = {}
    row_counts = {}
    with engine.connect() as conn:
        for t in tables:
            cols = inspector.get_columns(t)
            schema[t] = [{"name": c["name"], "type": str(c["type"])} for c in cols]
            try:
                result = conn.execute(text(f"SELECT COUNT(*) FROM `{t}`"))
                row_counts[t] = result.scalar()
            except Exception:
                row_counts[t] = "?"
    return {"tables": tables, "schema": schema, "row_counts": row_counts}