import re
import os
from collections import defaultdict

INPUT_FILE = os.path.join(os.path.dirname(__file__), "AI_Project_Portfolio_Industry_Ready_Edition.md")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "html_projects")

DOMAIN_COLORS = {
    "Healthcare": "#059669", "CV": "#2563eb", "Computer Vision": "#2563eb",
    "NLP": "#7c3aed", "Machine Learning": "#d97706", "ML": "#d97706",
    "FinTech": "#0891b2", "GenAI": "#db2777", "LLM": "#db2777",
    "EdTech": "#0d9488", "E-commerce": "#ea580c", "Time Series": "#4f46e5",
    "Recommendation": "#9333ea", "Smart Cities": "#16a34a", "Agriculture": "#65a30d",
    "HR": "#be123c", "IoT": "#0284c7", "Environment": "#15803d",
    "Accessibility": "#6d28d9", "LegalTech": "#475569", "Media": "#c026d3",
    "Productivity": "#0369a1", "Entertainment": "#a21caf", "Food": "#ea580c",
    "Energy": "#ca8a04", "Supply Chain": "#0d9488", "SaaS": "#6366f1",
    "Enterprise": "#334155", "Globalization": "#0284c7",
    "Anomaly": "#4f46e5", "Deep Learning": "#2563eb",
    "Analytics": "#d97706", "Business": "#d97706",
    "Revenue": "#0891b2", "Industrial": "#475569",
}

TECH_AREAS = [
    ("Machine Learning", "ml", "#d97706", "#fef3c7",
     "Classification, Regression, Ensemble Models, Feature Engineering, XGBoost, SHAP"),
    ("Natural Language Processing", "nlp", "#7c3aed", "#ede9fe",
     "Sentiment Analysis, NER, Text Classification, Topic Modeling, spaCy, BERT"),
    ("GenAI / LLM", "genai", "#db2777", "#fce7f3",
     "RAG, LangChain, Prompt Engineering, Vector Databases, GPT, Whisper"),
    ("Computer Vision", "cv", "#2563eb", "#dbeafe",
     "CNNs, Object Detection, Pose Estimation, Transfer Learning, YOLO, MediaPipe"),
    ("Time Series & Forecasting", "timeseries", "#4f46e5", "#e0e7ff",
     "Prophet, LSTM, ARIMA, Anomaly Detection, Demand Forecasting, Sensor Data"),
    ("Recommendation Systems", "recommendation", "#9333ea", "#f3e8ff",
     "Collaborative Filtering, Content-Based, Hybrid Systems, Personalization"),
]


def get_badge_color(text):
    for key, color in DOMAIN_COLORS.items():
        if key.lower() in text.lower():
            return color
    return "#475569"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #f8fafc;
            color: #1e293b;
            min-height: 100vh;
            line-height: 1.7;
        }}

        .nav {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid #e2e8f0;
            padding: 12px 0;
        }}

        .nav-inner {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .nav a {{
            color: #475569;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            padding: 6px 14px;
            border-radius: 8px;
            transition: all 0.2s;
        }}

        .nav a:hover {{
            color: #1e293b;
            background: #f1f5f9;
        }}

        .nav .project-num {{
            color: #94a3b8;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 48px 24px 80px;
        }}

        .hero {{
            margin-bottom: 48px;
        }}

        .hero h1 {{
            font-size: 2.2rem;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.3;
            margin-bottom: 20px;
        }}

        .badges {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 8px;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
            color: #fff;
        }}

        .card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 24px;
            transition: border-color 0.3s, box-shadow 0.3s;
        }}

        .card:hover {{
            border-color: #cbd5e1;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
        }}

        .card-label {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: #94a3b8;
            margin-bottom: 12px;
        }}

        .card h2 {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .card h2 .icon {{
            font-size: 1.3rem;
        }}

        .abstract {{
            font-size: 15.5px;
            color: #334155;
            line-height: 1.85;
            text-align: justify;
        }}

        .tech-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
        }}

        .tech-item {{
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 10px 14px;
            font-size: 13.5px;
            color: #334155;
            font-weight: 500;
        }}

        .skills-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .skill-tag {{
            background: #eef2ff;
            border: 1px solid #c7d2fe;
            color: #4338ca;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
        }}

        .dataset-text {{
            font-size: 14.5px;
            color: #475569;
            line-height: 1.7;
        }}

        .dataset-text strong {{
            color: #1e293b;
        }}

        .footer-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 48px;
            padding-top: 32px;
            border-top: 1px solid #e2e8f0;
        }}

        .footer-nav a {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #475569;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            padding: 10px 20px;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            transition: all 0.2s;
        }}

        .footer-nav a:hover {{
            color: #1e293b;
            border-color: #cbd5e1;
            background: #f8fafc;
        }}

        .footer-nav .placeholder {{ visibility: hidden; }}

        @media (max-width: 640px) {{
            .hero h1 {{ font-size: 1.6rem; }}
            .card {{ padding: 20px; }}
            .tech-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="nav">
        <div class="nav-inner">
            <a href="index.html">&larr; All Projects</a>
            <span class="project-num">Project {num} / 40</span>
            <div>
                {nav_prev}
                {nav_next}
            </div>
        </div>
    </div>

    <div class="container">
        <div class="hero">
            <h1>{title}</h1>
            <div class="badges">
                {domain_badges}
            </div>
        </div>

        <div class="card">
            <div class="card-label">Tech Stack</div>
            <div class="tech-grid">
                {tech_items}
            </div>
        </div>

        <div class="card">
            <div class="card-label">Skills You Will Learn</div>
            <div class="skills-list">
                {skill_tags}
            </div>
        </div>

        <div class="card">
            <div class="card-label">Dataset Availability</div>
            <p class="dataset-text">{dataset}</p>
        </div>

        <div class="card">
            <h2><span class="icon">📋</span> Project Abstract</h2>
            <p class="abstract">{abstract}</p>
        </div>

        <div class="footer-nav">
            {footer_prev}
            {footer_next}
        </div>
    </div>
</body>
</html>"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Project Portfolio — Industry-Ready Edition</title>
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #f8fafc;
            color: #1e293b;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 48px 24px 80px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 48px;
        }}

        h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 8px;
        }}

        .subtitle {{
            color: #64748b;
            font-size: 16px;
            margin-bottom: 0;
        }}

        /* ---- Tech Areas Section ---- */
        .section-title {{
            font-size: 1.3rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e2e8f0;
        }}

        .tech-areas {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 16px;
            margin-bottom: 56px;
        }}

        .tech-area-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 24px;
            cursor: pointer;
            transition: all 0.25s;
            border-left: 4px solid var(--accent);
        }}

        .tech-area-card:hover {{
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
            transform: translateY(-2px);
        }}

        .tech-area-card .ta-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}

        .tech-area-card .ta-name {{
            font-size: 16px;
            font-weight: 700;
            color: #0f172a;
        }}

        .tech-area-card .ta-count {{
            font-size: 13px;
            font-weight: 700;
            padding: 3px 12px;
            border-radius: 20px;
            color: #fff;
            background: var(--accent);
        }}

        .tech-area-card .ta-skills {{
            font-size: 13px;
            color: #64748b;
            line-height: 1.6;
        }}

        .tech-area-card .ta-projects {{
            margin-top: 12px;
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}

        .tech-area-card .ta-proj-num {{
            font-size: 11px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 6px;
            color: var(--accent);
            background: var(--accent-bg);
        }}

        /* ---- Domain Stats ---- */
        .domain-stats {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 56px;
        }}

        .domain-chip {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 6px 16px;
            font-size: 13px;
            font-weight: 500;
            color: #334155;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .domain-chip:hover {{
            border-color: #94a3b8;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }}

        .domain-chip .dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }}

        .domain-chip .count {{
            font-weight: 700;
            color: #64748b;
        }}

        /* ---- Filters ---- */
        .filters {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            margin-bottom: 32px;
        }}

        .filter-btn {{
            padding: 7px 18px;
            border-radius: 20px;
            border: 1px solid #e2e8f0;
            background: #ffffff;
            color: #475569;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .filter-btn:hover {{
            border-color: #94a3b8;
            background: #f1f5f9;
        }}

        .filter-btn.active {{
            background: #4f46e5;
            border-color: #4f46e5;
            color: #ffffff;
        }}

        /* ---- Project Grid ---- */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 16px;
        }}

        .project-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 24px;
            text-decoration: none;
            color: inherit;
            transition: all 0.25s;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .project-card:hover {{
            border-color: #a5b4fc;
            transform: translateY(-2px);
            box-shadow: 0 8px 28px rgba(79, 70, 229, 0.1);
        }}

        .project-card .num {{
            font-size: 11px;
            font-weight: 700;
            color: #94a3b8;
            letter-spacing: 1.2px;
        }}

        .project-card .title {{
            font-size: 15.5px;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.4;
        }}

        .project-card .domain-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}

        .project-card .dtag {{
            font-size: 11px;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 12px;
            color: #fff;
        }}

        .project-card .tech-preview {{
            font-size: 12.5px;
            color: #94a3b8;
            line-height: 1.5;
        }}

        @media (max-width: 640px) {{
            h1 {{ font-size: 1.8rem; }}
            .grid, .tech-areas {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI Project Portfolio</h1>
            <p class="subtitle">Industry-Ready Edition — 40 Projects for Resume, Demo & Deployment</p>
        </div>

        <div class="section-title">📂 Tech Areas Covered</div>
        <div class="tech-areas">
            {tech_area_cards}
        </div>

        <div class="section-title">🏷️ Industry Domains</div>
        <div class="domain-stats">
            {domain_chips}
        </div>

        <div class="section-title">📋 All Projects</div>
        <div class="filters">
            <button class="filter-btn active" onclick="filterProjects('all')">All (40)</button>
            <button class="filter-btn" onclick="filterProjects('ml')">Machine Learning</button>
            <button class="filter-btn" onclick="filterProjects('nlp')">NLP</button>
            <button class="filter-btn" onclick="filterProjects('genai')">GenAI / LLM</button>
            <button class="filter-btn" onclick="filterProjects('cv')">Computer Vision</button>
            <button class="filter-btn" onclick="filterProjects('timeseries')">Time Series</button>
            <button class="filter-btn" onclick="filterProjects('recommendation')">Recommendation</button>
        </div>

        <div class="grid">
            {cards}
        </div>
    </div>

    <script>
        function filterProjects(category) {{
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            document.querySelectorAll('.project-card').forEach(card => {{
                if (category === 'all' || card.dataset.categories.includes(category)) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}

        document.querySelectorAll('.tech-area-card').forEach(card => {{
            card.addEventListener('click', () => {{
                const cat = card.dataset.category;
                document.querySelectorAll('.filter-btn').forEach(b => {{
                    b.classList.remove('active');
                    if (b.textContent.toLowerCase().includes(cat) ||
                        (cat === 'timeseries' && b.textContent.includes('Time Series')) ||
                        (cat === 'genai' && b.textContent.includes('GenAI'))) {{
                        b.classList.add('active');
                    }}
                }});
                document.querySelectorAll('.project-card').forEach(c => {{
                    c.style.display = c.dataset.categories.includes(cat) ? 'flex' : 'none';
                }});
                document.querySelector('.grid').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }});
        }});

        document.querySelectorAll('.domain-chip').forEach(chip => {{
            chip.addEventListener('click', () => {{
                const domain = chip.dataset.domain.toLowerCase();
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.project-card').forEach(card => {{
                    const tags = card.querySelectorAll('.dtag');
                    let match = false;
                    tags.forEach(tag => {{
                        if (tag.textContent.toLowerCase().includes(domain)) match = true;
                    }});
                    card.style.display = match ? 'flex' : 'none';
                }});
                document.querySelector('.grid').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }});
        }});
    </script>
</body>
</html>"""


def parse_projects(md_text):
    pattern = r"## Project (\d+): (.+?)\n\n\*\*Domain:\*\* (.+?)\n\*\*Tech Stack Suggestion:\*\* (.+?)\n\*\*Skills Covered:\*\* (.+?)\n\*\*Dataset Availability:\*\* (.+?)\n\n\*\*Abstract:\*\*\n(.+?)(?=\n---|\Z)"
    projects = []
    for match in re.finditer(pattern, md_text, re.DOTALL):
        projects.append({
            "num": int(match.group(1)),
            "title": match.group(2).strip(),
            "domain": match.group(3).strip(),
            "tech_stack": match.group(4).strip(),
            "skills": match.group(5).strip(),
            "dataset": match.group(6).strip(),
            "abstract": match.group(7).strip(),
        })
    return projects


def categorize(domain_text):
    cats = []
    d = domain_text.lower()
    if any(k in d for k in ["machine learning", "ml ", "classification", "regression", "explainable"]):
        cats.append("ml")
    if any(k in d for k in ["nlp", "natural language", "sentiment", "text"]):
        cats.append("nlp")
    if any(k in d for k in ["genai", "llm", "generative", "rag"]):
        cats.append("genai")
    if any(k in d for k in ["computer vision", "cv", "image", "video", "object detection"]):
        cats.append("cv")
    if any(k in d for k in ["time series", "forecasting", "anomaly", "time-series"]):
        cats.append("timeseries")
    if any(k in d for k in ["recommendation", "personalization"]):
        cats.append("recommendation")
    return " ".join(cats) if cats else "ml"


def extract_industry_domain(domain_text):
    domains = []
    d = domain_text.lower()
    mapping = [
        ("healthcare", "Healthcare"), ("health", "Healthcare"),
        ("fintech", "FinTech"), ("finance", "FinTech"),
        ("edtech", "EdTech"), ("education", "EdTech"),
        ("e-commerce", "E-commerce"), ("ecommerce", "E-commerce"),
        ("smart cit", "Smart Cities"), ("urban", "Smart Cities"),
        ("agricultur", "Agriculture"), ("crop", "Agriculture"),
        ("hr", "HR Tech"), ("human resource", "HR Tech"),
        ("environment", "Environment"), ("water", "Environment"),
        ("legaltech", "LegalTech"), ("legal", "LegalTech"),
        ("media", "Media Tech"), ("news", "Media Tech"),
        ("developer", "Developer Tools"),
        ("hospitality", "Hospitality"), ("hotel", "Hospitality"),
        ("entertainment", "Entertainment"), ("music", "Entertainment"),
        ("food", "Food Tech"), ("recipe", "Food Tech"),
        ("energy", "Energy"), ("electricity", "Energy"),
        ("supply chain", "Supply Chain"), ("warehouse", "Supply Chain"), ("inventory", "Supply Chain"),
        ("saas", "SaaS"), ("enterprise", "Enterprise"),
        ("accessibility", "Accessibility"), ("sign language", "Accessibility"),
        ("globalization", "Globalization"), ("translat", "Globalization"),
        ("productivity", "Productivity"), ("meeting", "Productivity"),
        ("iot", "Industrial IoT"), ("industrial", "Industrial IoT"),
        ("revenue", "Hospitality"),
        ("risk", "FinTech"),
    ]
    seen = set()
    for keyword, label in mapping:
        if keyword in d and label not in seen:
            domains.append(label)
            seen.add(label)
    return domains if domains else ["General"]


def make_filename(num):
    return f"project_{num:02d}.html"


def generate_project_html(project, total):
    num = project["num"]

    domains = [d.strip() for d in project["domain"].replace("/", ",").split(",")]
    domain_badges = "\n".join(
        f'<span class="badge" style="background:{get_badge_color(d)}">{d.strip()}</span>'
        for d in domains if d.strip()
    )

    techs = [t.strip() for t in re.split(r"[+,]", project["tech_stack"]) if t.strip()]
    tech_items = "\n".join(f'<div class="tech-item">{t}</div>' for t in techs)

    skills = [s.strip() for s in project["skills"].split(",") if s.strip()]
    skill_tags = "\n".join(f'<span class="skill-tag">{s}</span>' for s in skills)

    dataset_html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", project["dataset"])

    nav_prev = f'<a href="{make_filename(num - 1)}">&larr; Prev</a>' if num > 1 else ""
    nav_next = f'<a href="{make_filename(num + 1)}">Next &rarr;</a>' if num < total else ""
    footer_prev = f'<a href="{make_filename(num - 1)}">&larr; Project {num - 1}</a>' if num > 1 else '<span class="placeholder">_</span>'
    footer_next = f'<a href="{make_filename(num + 1)}">Project {num + 1} &rarr;</a>' if num < total else '<span class="placeholder">_</span>'

    return HTML_TEMPLATE.format(
        title=project["title"],
        num=num,
        domain_badges=domain_badges,
        tech_items=tech_items,
        skill_tags=skill_tags,
        dataset=dataset_html,
        abstract=project["abstract"],
        nav_prev=nav_prev,
        nav_next=nav_next,
        footer_prev=footer_prev,
        footer_next=footer_next,
    )


def generate_index_html(projects):
    cat_projects = defaultdict(list)
    for p in projects:
        cats = categorize(p["domain"]).split()
        for c in cats:
            cat_projects[c].append(p["num"])

    tech_area_cards = []
    for name, key, color, bg_color, skills_text in TECH_AREAS:
        nums = cat_projects.get(key, [])
        proj_nums = "".join(f'<span class="ta-proj-num">#{n}</span>' for n in sorted(nums))
        tech_area_cards.append(
            f'<div class="tech-area-card" style="--accent:{color};--accent-bg:{bg_color}" data-category="{key}">'
            f'<div class="ta-header"><span class="ta-name">{name}</span>'
            f'<span class="ta-count">{len(nums)} projects</span></div>'
            f'<div class="ta-skills">{skills_text}</div>'
            f'<div class="ta-projects">{proj_nums}</div>'
            f'</div>'
        )

    domain_map = defaultdict(list)
    for p in projects:
        for d in extract_industry_domain(p["domain"]):
            domain_map[d].append(p["num"])
    domain_map = dict(sorted(domain_map.items(), key=lambda x: -len(x[1])))

    domain_chips = []
    for domain_name, proj_nums in domain_map.items():
        color = get_badge_color(domain_name)
        domain_chips.append(
            f'<span class="domain-chip" data-domain="{domain_name}">'
            f'<span class="dot" style="background:{color}"></span>'
            f'{domain_name} <span class="count">({len(proj_nums)})</span></span>'
        )

    cards = []
    for p in projects:
        cats = categorize(p["domain"])
        domains = [d.strip() for d in p["domain"].replace("/", ",").split(",") if d.strip()]
        dtags = "".join(
            f'<span class="dtag" style="background:{get_badge_color(d)}">{d}</span>'
            for d in domains[:3]
        )
        techs = [t.strip() for t in re.split(r"[+,]", p["tech_stack"]) if t.strip()]
        tech_preview = " · ".join(techs[:4])

        cards.append(
            f'<a href="{make_filename(p["num"])}" class="project-card" data-categories="{cats}">'
            f'<span class="num">PROJECT {p["num"]:02d}</span>'
            f'<span class="title">{p["title"]}</span>'
            f'<div class="domain-tags">{dtags}</div>'
            f'<span class="tech-preview">{tech_preview}</span>'
            f"</a>"
        )

    return INDEX_TEMPLATE.format(
        tech_area_cards="\n            ".join(tech_area_cards),
        domain_chips="\n            ".join(domain_chips),
        cards="\n            ".join(cards),
    )


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        md_text = f.read()

    projects = parse_projects(md_text)
    print(f"Parsed {len(projects)} projects from markdown.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for p in projects:
        html = generate_project_html(p, len(projects))
        filepath = os.path.join(OUTPUT_DIR, make_filename(p["num"]))
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Generated: {make_filename(p['num'])}")

    index_html = generate_index_html(projects)
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  Generated: index.html")

    print(f"\nDone! {len(projects) + 1} HTML files saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
