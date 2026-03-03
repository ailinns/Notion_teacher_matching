from notion_client import Client

NOTION_TOKEN = "ntn_S31910885477gtlEYp97gkXxRnCvhUYT8waGtOhuNG88XZ"
DATABASE_ID = "3180be34-25a3-8020-b8ec-fc59222190be"

# สร้าง client
notion = Client(auth=NOTION_TOKEN)


def save_to_notion(topic, keywords, top_advisors):

    advisor_text = "\n".join(
        [f"{i+1}. {a['advisor']} ({a['percentage']}%)"
         for i, a in enumerate(top_advisors)]
    )

    response = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Topic": {
                "title": [
                    {"text": {"content": topic}}
                ]
            },
            "Keywords": {
                "multi_select": [
                    {"name": str(k)} for k in keywords
                ]
            },
            "Matched Advisor": {
                "rich_text": [
                    {"text": {"content": advisor_text}}
                ]
            },
            "Score": {
                "number": top_advisors[0]["percentage"]
            }
        }
    )

    return response