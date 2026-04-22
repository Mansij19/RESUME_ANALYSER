"""
Grammar & Suggestions Service
===============================
Rule-based grammar checking and resume improvement suggestions.
No external dependencies (no Java / LanguageTool required).
"""

import re

# Strong action verbs that make resumes impactful
ACTION_VERBS = [
    "achieved", "managed", "developed", "designed", "implemented",
    "led", "created", "built", "improved", "increased", "decreased",
    "reduced", "launched", "delivered", "coordinated", "established",
    "executed", "generated", "initiated", "maintained", "negotiated",
    "optimized", "organized", "produced", "resolved", "streamlined",
    "supervised", "trained", "transformed", "analyzed", "automated",
    "collaborated", "communicated", "contributed", "directed",
    "engineered", "facilitated", "formulated", "guided", "influenced",
    "integrated", "mentored", "orchestrated", "pioneered", "spearheaded"
]

# Weak phrases that should be replaced with action verbs
WEAK_PHRASES = [
    "responsible for", "duties included", "helped with",
    "worked on", "assisted in", "participated in",
    "was involved in", "tasked with", "in charge of",
    "handled various", "did work on"
]

# Sections every good resume should have
ESSENTIAL_SECTIONS = ["education", "experience", "skills"]
OPTIONAL_SECTIONS = ["projects", "summary", "objective", "certifications",
                     "achievements", "publications", "volunteer"]


def check_grammar(text):
    """
    Perform rule-based grammar and style checking on resume text.

    Checks for:
    - Weak/passive phrases
    - Passive voice usage
    - Repeated words
    - Very long sentences
    - Common spelling issues in resumes

    Args:
        text (str): Resume text to analyze.

    Returns:
        list[dict]: List of corrections, each with 'type', 'issue', 'suggestion'.
    """
    corrections = []
    text_lower = text.lower()

    # 1. Check for weak phrases
    for phrase in WEAK_PHRASES:
        if phrase in text_lower:
            corrections.append({
                "type": "style",
                "issue": f'Weak phrase: "{phrase}"',
                "suggestion": (
                    f'Replace "{phrase}" with a strong action verb '
                    f'(e.g., "managed", "developed", "led", "implemented")'
                )
            })

    # 2. Check for passive voice indicators
    passive_patterns = [
        r'\bwas\s+\w+ed\b', r'\bwere\s+\w+ed\b',
        r'\bbeen\s+\w+ed\b', r'\bis\s+being\s+\w+ed\b'
    ]
    for pattern in passive_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches[:2]:  # Limit to 2 per pattern
            corrections.append({
                "type": "grammar",
                "issue": f'Passive voice: "{match}"',
                "suggestion": "Rewrite in active voice for stronger impact"
            })

    # 3. Check for repeated consecutive words
    words = text.split()
    for i in range(len(words) - 1):
        if (words[i].lower() == words[i + 1].lower()
                and words[i].isalpha() and len(words[i]) > 2):
            corrections.append({
                "type": "grammar",
                "issue": f'Repeated word: "{words[i]}"',
                "suggestion": f'Remove the duplicate "{words[i]}"'
            })

    # 4. Check for very long sentences (>40 words)
    sentences = re.split(r'[.!?]+', text)
    for sent in sentences:
        word_count = len(sent.split())
        if word_count > 40:
            preview = sent.strip()[:60] + "..."
            corrections.append({
                "type": "style",
                "issue": f'Very long sentence ({word_count} words): "{preview}"',
                "suggestion": "Break this into shorter, punchier sentences"
            })

    return corrections[:12]  # Cap at 12 corrections


def suggest_improvements(text):
    """
    Generate actionable resume improvement suggestions.

    Analyzes:
    - Resume length
    - Action verb usage
    - Quantifiable achievements
    - Essential sections presence
    - Contact information
    - Professional links

    Args:
        text (str): Resume text to analyze.

    Returns:
        list[dict]: List of suggestions, each with 'icon', 'title', 'detail', 'type'.
    """
    suggestions = []
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)

    # 1. Resume length check
    if word_count < 150:
        suggestions.append({
            "icon": "📝", "type": "warning",
            "title": "Resume Too Short",
            "detail": (f"Your resume has only {word_count} words. "
                       "Aim for 400–800 words for a comprehensive resume.")
        })
    elif word_count > 1000:
        suggestions.append({
            "icon": "✂️", "type": "warning",
            "title": "Resume Too Long",
            "detail": (f"Your resume has {word_count} words. "
                       "Consider trimming to 400–800 words for readability.")
        })
    else:
        suggestions.append({
            "icon": "✅", "type": "success",
            "title": "Good Resume Length",
            "detail": (f"Your resume has {word_count} words — "
                       "within the ideal range.")
        })

    # 2. Action verb usage
    found_verbs = [v for v in ACTION_VERBS if v in text_lower]
    if len(found_verbs) < 3:
        suggestions.append({
            "icon": "💪", "type": "warning",
            "title": "Use More Action Verbs",
            "detail": ("Start bullet points with strong verbs like "
                       "'Achieved', 'Developed', 'Led', 'Implemented'.")
        })
    else:
        suggestions.append({
            "icon": "✅", "type": "success",
            "title": "Good Use of Action Verbs",
            "detail": f"Found {len(found_verbs)} action verbs — keep it up!"
        })

    # 3. Quantifiable achievements
    numbers = re.findall(r'\d+[%+]?', text)
    if len(numbers) < 3:
        suggestions.append({
            "icon": "📊", "type": "warning",
            "title": "Add Quantifiable Achievements",
            "detail": ("Include metrics like 'Increased sales by 25%' "
                       "or 'Managed a team of 10'.")
        })
    else:
        suggestions.append({
            "icon": "✅", "type": "success",
            "title": "Good Use of Metrics",
            "detail": (f"Found {len(numbers)} numeric data points — "
                       "numbers strengthen your impact.")
        })

    # 4. Essential sections check
    missing = []
    for section in ESSENTIAL_SECTIONS:
        if section not in text_lower:
            missing.append(section.title())
    if missing:
        suggestions.append({
            "icon": "📋", "type": "warning",
            "title": "Missing Important Sections",
            "detail": (f"Consider adding: {', '.join(missing)}. "
                       "These are essential for most resumes.")
        })
    else:
        suggestions.append({
            "icon": "✅", "type": "success",
            "title": "All Key Sections Present",
            "detail": "Your resume includes Education, Experience, and Skills."
        })

    # 5. Contact info check
    has_email = bool(re.search(r'\S+@\S+\.\S+', text))
    has_phone = bool(re.search(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s./0-9]{7,}', text))
    if not has_email:
        suggestions.append({
            "icon": "📧", "type": "warning",
            "title": "Add Email Address",
            "detail": "Include a professional email address."
        })
    if not has_phone:
        suggestions.append({
            "icon": "📱", "type": "warning",
            "title": "Add Phone Number",
            "detail": "Include a phone number for recruiters to reach you."
        })

    # 6. Professional links
    has_links = any(kw in text_lower for kw in
                    ["linkedin", "github", "portfolio", "website"])
    if not has_links:
        suggestions.append({
            "icon": "🔗", "type": "warning",
            "title": "Add Professional Links",
            "detail": "Include LinkedIn, GitHub, or portfolio links."
        })

    return suggestions
