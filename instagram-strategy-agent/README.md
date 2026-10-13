# Instagram Strategy Agent

An AI-powered Instagram planning workspace for creators, coaches, local businesses, and small brands. It turns a business brief into a practical 30-day content strategy with pillars, weekly cadence, post ideas, hooks, captions, hashtags, CTAs, and measurement guidance.

## What it does

- Collects audience, offer, voice, goals, cadence, and niche context.
- Generates a structured 30-day plan through an OpenAI-compatible chat API.
- Includes a deterministic fallback plan when no API key is configured, so the demo works offline.
- Lets you copy the strategy as Markdown or download it as a `.md` file.
- Keeps the architecture provider-agnostic: use Manus/OpenAI-compatible models or another compatible endpoint.

## Run locally

```bash
cp .env.example .env
# Optional: set OPENAI_API_KEY and OPENAI_API_BASE in .env
python3 -m agent.server
```

Open <http://localhost:8000>.

No third-party Python package is required. The server uses Python's standard library and calls the configured model endpoint with HTTPS.

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | empty | API key for the compatible chat endpoint |
| `OPENAI_API_BASE` | `https://api.openai.com/v1` | API base URL; Manus users can set the compatible proxy URL |
| `MODEL` | `gpt-5-mini` | Model ID; verify it exists on your endpoint |
| `PORT` | `8000` | Local server port |

## API

`POST /api/strategy` accepts:

```json
{
  "brand": "Northstar Pilates",
  "niche": "Pilates for busy professionals",
  "audience": "Women 28–45 in urban areas",
  "offer": "Small-group classes and online memberships",
  "goal": "Generate qualified trial bookings",
  "voice": "Warm, expert, energising",
  "cadence": "4 feed posts + daily stories",
  "notes": "Avoid fear-based messaging"
}
```

The response is JSON with `strategy`, `source` (`ai` or `fallback`), and `model`.

## Project structure

- `agent/server.py` — zero-dependency HTTP server and AI orchestration.
- `agent/prompt.py` — strategy prompt and fallback plan generator.
- `public/` — single-page user interface.
- `tests/` — standard-library unit tests for validation and fallback behavior.

## Product notes

This starter deliberately does not auto-publish to Instagram. It produces an approval-ready plan; publishing can be added later through Meta's official APIs with appropriate permissions and review.
