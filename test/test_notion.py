from notion_logger import save_to_notion

result = save_to_notion(
    topic="Test AI Project",
    keywords=["AI", "ML"],
    advisor="Dr. Test",
    score=2
)

print(result)