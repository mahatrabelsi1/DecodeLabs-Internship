from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CatalogItem:
    title: str
    category: str
    difficulty: str
    tags: set[str]
    description: str


CATALOG = [
    CatalogItem(
        title="Python Basics Practice Pack",
        category="Programming",
        difficulty="beginner",
        tags={"python", "programming", "logic", "beginner", "practice"},
        description="Short exercises for variables, loops, functions, and problem solving.",
    ),
    CatalogItem(
        title="Data Cleaning Mini Project",
        category="Data Analytics",
        difficulty="beginner",
        tags={"python", "pandas", "data", "cleaning", "analytics"},
        description="Clean missing values, rename columns, and prepare data for analysis.",
    ),
    CatalogItem(
        title="Classification With KNN",
        category="Machine Learning",
        difficulty="intermediate",
        tags={"ai", "machine learning", "classification", "knn", "sklearn"},
        description="Train a KNN model and evaluate accuracy, F1 score, and confusion matrix.",
    ),
    CatalogItem(
        title="Recommendation Logic Starter",
        category="Artificial Intelligence",
        difficulty="intermediate",
        tags={"ai", "recommendation", "similarity", "matching", "logic"},
        description="Build a content-based recommendation system using preference matching.",
    ),
    CatalogItem(
        title="Dashboard Design With Charts",
        category="Data Visualization",
        difficulty="beginner",
        tags={"data", "visualization", "charts", "dashboard", "seaborn"},
        description="Create readable charts and dashboards from a structured dataset.",
    ),
    CatalogItem(
        title="Natural Language Chatbot",
        category="Artificial Intelligence",
        difficulty="intermediate",
        tags={"ai", "chatbot", "nlp", "text", "automation"},
        description="Create a rule-based chatbot and improve it with better intent matching.",
    ),
    CatalogItem(
        title="Advanced Model Evaluation",
        category="Machine Learning",
        difficulty="advanced",
        tags={"machine learning", "metrics", "evaluation", "sklearn", "model"},
        description="Compare precision, recall, F1 score, and confusion matrices across models.",
    ),
]


def normalize_preferences(raw_preferences: str) -> set[str]:
    """Convert comma-separated user input into a clean set of lowercase preferences."""
    return {
        preference.strip().lower()
        for preference in raw_preferences.split(",")
        if preference.strip()
    }


def similarity_score(preferences: set[str], item: CatalogItem) -> float:
    """Score an item using tag overlap plus small category and difficulty bonuses."""
    if not preferences:
        return 0.0

    overlap = preferences.intersection(item.tags)
    union = preferences.union(item.tags)
    score = len(overlap) / len(union)

    if item.category.lower() in preferences:
        score += 0.15

    if item.difficulty.lower() in preferences:
        score += 0.10

    return round(score, 4)


def recommend_items(raw_preferences: str, limit: int = 5) -> list[tuple[CatalogItem, float]]:
    preferences = normalize_preferences(raw_preferences)

    scored_items = [
        (item, similarity_score(preferences, item))
        for item in CATALOG
    ]

    scored_items.sort(key=lambda result: result[1], reverse=True)
    return [result for result in scored_items if result[1] > 0][:limit]


def display_recommendations(recommendations: list[tuple[CatalogItem, float]]) -> None:
    if not recommendations:
        print("\nNo strong matches found. Try interests like python, ai, data, beginner, or sklearn.")
        return

    print("\nRecommended items:\n")
    for index, (item, score) in enumerate(recommendations, start=1):
        print(f"{index}. {item.title}")
        print(f"   Category: {item.category}")
        print(f"   Difficulty: {item.difficulty.title()}")
        print(f"   Similarity score: {score:.2f}")
        print(f"   Why: {item.description}\n")


def main() -> None:
    print("DecodeLabs Project 3 - AI Recommendation Logic")
    print("Enter interests separated by commas.")
    print("Example: ai, python, beginner, classification\n")

    user_preferences = input("Your interests: ")
    recommendations = recommend_items(user_preferences)
    display_recommendations(recommendations)


if __name__ == "__main__":
    main()
