"""
Skill Extractor Service
========================
Matches skills from resume text against a comprehensive,
categorized skill database using NLP pattern matching.
"""

import re

# Comprehensive skill database organized by category
SKILL_DATABASE = {
    "Programming Languages": [
        "python", "java", "javascript", "c++", "c#", "ruby", "go", "golang",
        "swift", "kotlin", "rust", "php", "typescript", "scala", "matlab",
        "perl", "dart", "lua", "haskell", "objective-c", "visual basic",
        "assembly", "fortran", "cobol", "groovy", "elixir"
    ],
    "Web Development": [
        "html", "css", "react", "angular", "vue.js", "vue", "node.js",
        "express.js", "express", "django", "flask", "fastapi", "spring boot",
        "asp.net", "next.js", "nuxt.js", "bootstrap", "tailwind css",
        "tailwind", "jquery", "sass", "webpack", "graphql", "rest api",
        "restful", "wordpress", "shopify", "svelte"
    ],
    "Data Science & ML": [
        "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
        "scikit-learn", "sklearn", "pandas", "numpy", "matplotlib", "seaborn",
        "natural language processing", "nlp", "computer vision", "opencv",
        "data analysis", "data visualization", "statistics", "neural network",
        "random forest", "regression", "classification", "clustering",
        "data mining", "big data", "spark", "hadoop", "tableau", "power bi",
        "data engineering", "etl", "airflow", "jupyter"
    ],
    "Databases": [
        "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite",
        "oracle", "cassandra", "elasticsearch", "dynamodb", "firebase",
        "neo4j", "mariadb", "couchdb", "influxdb", "snowflake"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "jenkins", "ci/cd", "cicd", "terraform", "ansible", "linux", "git",
        "github", "gitlab", "bitbucket", "nginx", "apache", "heroku",
        "digital ocean", "cloudflare", "serverless", "lambda"
    ],
    "Tools & Frameworks": [
        "jira", "confluence", "slack", "trello", "figma", "postman",
        "swagger", "agile", "scrum", "kanban", "microservices",
        "api development", "unit testing", "selenium", "cypress",
        "pytest", "jest", "mocha", "maven", "gradle"
    ],
    "Soft Skills": [
        "leadership", "communication", "teamwork", "problem solving",
        "critical thinking", "time management", "project management",
        "collaboration", "adaptability", "creativity", "analytical",
        "presentation", "mentoring", "negotiation", "decision making",
        "conflict resolution", "strategic planning", "interpersonal"
    ]
}


def extract_skills(text):
    """
    Extract skills from resume text by matching against the skill database.

    Uses case-insensitive matching with word-boundary awareness for
    short skill names (≤2 chars) to avoid false positives.

    Args:
        text (str): Resume text to analyze.

    Returns:
        tuple: (skills_dict: {category: [skills]}, total_count: int)
    """
    text_lower = text.lower()
    found_skills = {}
    total_count = 0

    for category, skills in SKILL_DATABASE.items():
        matched = []
        for skill in skills:
            if len(skill) <= 2:
                # For very short terms (e.g., "r", "go"), use word boundaries
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    matched.append(skill.upper())
            else:
                if skill in text_lower:
                    # Capitalize skill name for display
                    display_name = skill.title()
                    # Special formatting for acronyms and compound names
                    if skill in ('sql', 'html', 'css', 'aws', 'gcp', 'nlp',
                                 'etl', 'api', 'cicd', 'ci/cd'):
                        display_name = skill.upper()
                    elif '.' in skill or '-' in skill:
                        display_name = skill  # Keep original casing for Node.js etc.
                    matched.append(display_name)

        if matched:
            # Remove duplicates while preserving order
            seen = set()
            unique = []
            for s in matched:
                if s.lower() not in seen:
                    seen.add(s.lower())
                    unique.append(s)
            found_skills[category] = unique
            total_count += len(unique)

    return found_skills, total_count
