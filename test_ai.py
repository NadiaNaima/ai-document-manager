from app.services.ai_service import generate_summary


text = """
The company has approved a budget of €250,000
for the 2026 marketing department.

The main expenses are advertising, personnel,
software subscriptions, and events.

The department must provide a quarterly report
to management.
"""


summary = generate_summary(text)

print("AI SUMMARY")
print("=" * 50)
print(summary)