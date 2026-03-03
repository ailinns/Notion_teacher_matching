from mcp_tools import MCPToolRegistry

mcp = MCPToolRegistry()

# Test match tool
keywords = ["AI", "Machine Learning"]

top3 = mcp.execute(
    "match_excel",
    {"keywords": keywords}
)

print("Top 3:", top3)