from excel_matcher import match_advisor_from_excel
from notion_logger import save_to_notion


class MCPToolRegistry:
    """
    MCP Tool Registry
    Acts as abstraction layer between controller and tools
    """

    def __init__(self):
        self.tools = {
            "match_excel": self.match_excel_tool,
            "save_log": self.save_log_tool
        }

    def execute(self, tool_name, payload):
        """
        Execute tool by name with payload
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found in MCP registry")

        return self.tools[tool_name](payload)

    # Excel Matching
    def match_excel_tool(self, payload):
        keywords = payload.get("keywords", [])

        if not keywords:
            return []

        return match_advisor_from_excel(keywords)

    # Notion Logging
    def save_log_tool(self, payload):

        return save_to_notion(
            payload["topic"],
            payload["keywords"],
            payload["top_advisors"]
        )