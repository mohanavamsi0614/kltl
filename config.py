import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "analytics_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Metadata Paths
TABLE_MAP_PATH = "knowledge/db_table_map.json"
METRICS_REGISTRY_PATH = "knowledge/analytics_metrics.json"

# Execution Constraints
DEFAULT_LIMIT = 100
MAX_LIMIT = 1000

# OpenAI API Key (for LangChain)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
