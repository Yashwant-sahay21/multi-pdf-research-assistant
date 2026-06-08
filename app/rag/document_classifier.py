def detect_document_type(text):

    text = text.lower()

    research_keywords = [
        "abstract",
        "methodology",
        "dataset",
        "results",
        "conclusion",
        "references",
        "experiment",
        "accuracy"
    ]

    resume_keywords = [
        "skills",
        "education",
        "experience",
        "projects",
        "certifications"
    ]

    notification_keywords = [
        "candidate",
        "examination",
        "instructions",
        "application",
        "notification",
        "admit card",
        "eligibility",
        "commission"
    ]

    research_score = sum(
        keyword in text
        for keyword in research_keywords
    )

    resume_score = sum(
        keyword in text
        for keyword in resume_keywords
    )

    notification_score = sum(
        keyword in text
        for keyword in notification_keywords
    )

    scores = {
        "research_paper": research_score,
        "resume": resume_score,
        "notification": notification_score
    }

    best_type = max(
        scores,
        key=scores.get
    )

    if scores[best_type] == 0:
        return "general"
        

    return best_type
    print("DOCUMENT TYPE:", best_type)