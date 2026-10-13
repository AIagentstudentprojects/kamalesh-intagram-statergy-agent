import json

SYSTEM_PROMPT = """You are Instagram Strategy Agent, a senior social strategist for small brands.
Return ONLY valid JSON matching the requested schema. Make advice specific, realistic, ethical,
and action-oriented. Never promise virality. Favor audience insight, clear positioning,
repeatable formats, strong hooks, useful CTAs, and measurable experiments."""

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "positioning": {"type": "string"},
        "content_pillars": {"type": "array", "items": {"type": "object", "additionalProperties": False, "properties": {"name": {"type": "string"}, "purpose": {"type": "string"}, "share": {"type": "string"}}, "required": ["name", "purpose", "share"]}},
        "weekly_rhythm": {"type": "array", "items": {"type": "string"}},
        "calendar": {"type": "array", "items": {"type": "object", "additionalProperties": False, "properties": {"day": {"type": "string"}, "format": {"type": "string"}, "title": {"type": "string"}, "hook": {"type": "string"}, "cta": {"type": "string"}, "hashtags": {"type": "array", "items": {"type": "string"}}}, "required": ["day", "format", "title", "hook", "cta", "hashtags"]}},
        "story_system": {"type": "array", "items": {"type": "string"}},
        "measurement": {"type": "array", "items": {"type": "object", "additionalProperties": False, "properties": {"metric": {"type": "string"}, "why": {"type": "string"}, "weekly_action": {"type": "string"}}, "required": ["metric", "why", "weekly_action"]}},
        "next_7_days": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["positioning", "content_pillars", "weekly_rhythm", "calendar", "story_system", "measurement", "next_7_days"]
}

def build_user_prompt(data):
    return "Create a 30-day Instagram strategy for this brand. Include 12 calendar entries (three per week), a daily story system, and a measurement loop.\n\n" + json.dumps(data, ensure_ascii=False, indent=2)

def fallback_strategy(data):
    brand = data.get("brand") or "this brand"
    niche = data.get("niche") or "the target niche"
    goal = data.get("goal") or "consistent growth"
    formats = [("Reel", "The 3-second mistake most people make"), ("Carousel", "A simple framework your audience can use today"), ("Founder post", "What we believe about serving this audience")]
    calendar = []
    for i in range(12):
        fmt, title = formats[i % 3]
        calendar.append({"day": f"Day {i * 2 + 1}", "format": fmt, "title": title, "hook": f"If you are working on {niche}, save this before your next decision.", "cta": "Comment with your biggest question and save this for later.", "hashtags": [f"#{niche.replace(' ', '')[:18]}", "#contentstrategy", "#smallbusiness"]})
    return {"positioning": f"{brand} helps {niche} move from uncertainty to a clear, repeatable next step.", "content_pillars": [{"name": "Teach", "purpose": "Build trust with useful answers.", "share": "40%"}, {"name": "Proof", "purpose": "Show outcomes, process, and credibility.", "share": "30%"}, {"name": "Connect", "purpose": "Make the brand memorable and human.", "share": "20%"}, {"name": "Offer", "purpose": "Turn attention into an appropriate next step.", "share": "10%"}], "weekly_rhythm": ["Monday: teach a problem", "Wednesday: show proof or process", "Friday: invite conversation or action"], "calendar": calendar, "story_system": ["Morning: poll or question", "Midday: behind-the-scenes proof", "Evening: answer one FAQ and invite a DM"], "measurement": [{"metric": "Saves and shares", "why": "Signals useful content-market fit.", "weekly_action": "Repeat the top two topics in a new format."}, {"metric": "Profile visits to actions", "why": "Shows whether positioning is clear.", "weekly_action": "Test one bio or CTA improvement."}, {"metric": "Qualified replies", "why": "Connects content to the business goal.", "weekly_action": f"Review replies against the goal: {goal}."}], "next_7_days": ["Write one audience pain-point list.", "Record one 30-second teaching Reel.", "Publish one proof-based carousel.", "Set up three Story templates.", "Reply to every meaningful comment within 24 hours.", "Review saves, shares, and profile actions.", "Choose next week's topic from audience language."]}
