"""
Central Crawl Policy Configuration

Defines governance rules for all web crawling activities.
"""

# -----------------------------
# Allowed Domains
# -----------------------------

# ALLOWED_DOMAINS is no longer enforced.
ALLOWED_DOMAINS = []

# -----------------------------
# Allowed Page Types
# -----------------------------

ALLOWED_PAGE_TYPES = [
    "homepage",
    "about",
    "services",
    "solutions",
    "products",
    "careers",
    "jobs",
    "blog",
    "contact",
]

# -----------------------------
# Excluded URL Keywords
# -----------------------------

EXCLUDED_PATHS = [
    "/login",
    "/signup",
    "/register",
    "/dashboard",
    "/admin",
    "/checkout",
    "/cart",
    "/profile",
    "/account",
]

# -----------------------------
# Crawl Configuration
# -----------------------------

MAX_CRAWL_DEPTH = 2

DOWNLOAD_DELAY = 2          # seconds

DOWNLOAD_TIMEOUT = 15       # seconds

RETRY_TIMES = 3

CONCURRENT_REQUESTS = 4

USER_AGENT = (
    "O2Geeks-WebCrawler/1.0 "
    "(AI Internship Project)"
)

# -----------------------------
# Data Governance
# -----------------------------

STORE_HTML = True

STORE_TEXT = True

STORE_METADATA = True

GENERATE_SHA256 = True

RESPECT_ROBOTS = True

ALLOW_DYNAMIC_RENDERING = False

# -----------------------------
# Approval Workflow
# -----------------------------

DEFAULT_APPROVAL_STATE = "Pending"