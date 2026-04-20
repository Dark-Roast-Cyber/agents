# Future Note: OpenWebUI Workspace Model Profile Images

## Problem

Custom avatars set via `meta.profile_image_url` on workspace models do not render in the chat/runtime UI when the value is a file-backed URL such as `/api/v1/files/<id>/content`. The model editor renders these correctly, but the chat UI does not.

## Formats Tested

| Format | Model Editor | Chat UI |
|--------|-------------|---------|
| `/api/v1/files/<id>/content` | Works | Broken |
| `data:image/png;base64,...` | Works | Works |
| `data:image/webp;base64,...` | Works | Works |
| `data:image/jpeg;base64,...` | Works | Likely works |

## Working Solution

Embed the avatar image directly as a `data:image/<mime>;base64,...` data URL in `meta.profile_image_url` via the API. This works in both the model editor and the chat/runtime UI.

The file-backed URL format (`/api/v1/files/<id>/content`) is the only format that fails in chat.

## Root Cause (Suspected)

The chat/runtime frontend either:
- Does not resolve relative or authenticated file-backed URLs from `meta.profile_image_url`
- Handles `data:` URLs natively (they're self-contained) but cannot fetch file-backed URLs in the chat rendering context

## Recommended Format: WebP

WebP is the preferred format for embedded data URLs because:
- Smaller file size than PNG (typically 40-60% smaller) while maintaining quality
- Renders correctly in the chat UI as `data:image/webp;base64,...`
- The Cody model's avatar was automatically re-encoded to WebP by OpenWebUI after pushing a PNG, confirming WebP is natively supported

## Batch Avatar Generation & Upload Process

### 1. Generate Avatars

Use `openwebui/generate_image.py` to create PNG avatars following the styling guide in `AI-AVATAR-PROMPT-STYLING-GUIDE.md`:

```bash
uv run python openwebui/generate_image.py \
  --prompt "<avatar prompt per styling guide>" \
  --output ".opencode/images/<agent-slug>.png" \
  --background transparent \
  --format png
```

### 2. Convert to WebP and Push to OpenWebUI

```python
import base64, io, json
from PIL import Image
from pathlib import Path
from openwebui.client import OpenWebUIClient

IMAGES_DIR = Path(".opencode/images")

# Map: (image_filename, model_id)
agents = [
    ("stacey-the-scripter.png", "stacey-the-scripter"),
    ("logan-the-log-analyst.png", "logan-the-log-analyst"),
    # ... etc
]

c = OpenWebUIClient()

for img_file, model_id in agents:
    img_path = IMAGES_DIR / img_file
    img = Image.open(img_path)
    buf = io.BytesIO()
    img.save(buf, format="WEBP", quality=85)
    webp_bytes = buf.getvalue()

    b64 = base64.b64encode(webp_bytes).decode("ascii")
    data_url = f"data:image/webp;base64,{b64}"

    model = c.get_model(model_id)
    meta = dict(model.get("meta", {}))
    meta["profile_image_url"] = data_url

    payload = {
        "id": model["id"],
        "name": model["name"],
        "base_model_id": model.get("base_model_id"),
        "meta": meta,
        "params": model.get("params", {}),
        "access_grants": model.get("access_grants", []),
    }
    c.update_model(payload)
```

### 3. Conversion Snippet (Legacy: File URL → Data URL)

For migrating existing file-backed URLs:

```python
import base64
import httpx
from PIL import Image
from io import BytesIO
from openwebui.client import OpenWebUIClient

c = OpenWebUIClient()

file_path = "/api/v1/files/<id>/content"
url = f"{c.base_url}{file_path}"
headers = {"Authorization": f"Bearer {c.api_key}"}

with httpx.Client(timeout=30.0) as client:
    resp = client.get(url, headers=headers, follow_redirects=True)
    resp.raise_for_status()
    image_bytes = resp.content

img = Image.open(BytesIO(image_bytes))
buf = BytesIO()
img.save(buf, format="WEBP", quality=85)
webp_bytes = buf.getvalue()

b64 = base64.b64encode(webp_bytes).decode("ascii")
data_url = f"data:image/webp;base64,{b64}"

model = c.get_model("<model-id>")
meta = dict(model.get("meta", {}))
meta["profile_image_url"] = data_url
payload = {
    "id": model["id"],
    "name": model["name"],
    "base_model_id": model.get("base_model_id"),
    "meta": meta,
    "params": model.get("params", {}),
    "access_grants": model.get("access_grants", []),
}
c.update_model(payload)
```

## Agent Avatar Inventory

| Agent | Model ID | Color | Character | Avatar File |
|-------|----------|-------|-----------|-------------|
| Stacey | stacey-the-scripter | Deep green | Mid-30s F, short curly hair, glasses, script badge | `.opencode/images/stacey-the-scripter.png` |
| Logan | logan-the-log-analyst | Navy blue | Late-40s M, silver-streaked dark hair, magnifying glass pin | `.opencode/images/logan-the-log-analyst.png` |
| Madison | madison-the-cybersecurity-manager | Plum purple | Early-50s F, silver-streaked locs, shield brooch | `.opencode/images/madison-the-cybersecurity-manager.png` |
| Casey | casey-the-compliance-analyst | Teal | Early-40s NB, auburn hair, clipboard badge, gavel keychain | `.opencode/images/casey-the-compliance-analyst.png` |
| Nyx | ai-nyx-the-red-teamer | Dark violet | Late-20s F, asymmetric black/violet hair, lockpick collar clip | `.opencode/images/ai-nyx-the-red-teamer.png` |
| Armis Query Agent | armis-query-agent | Burnt orange | Early-30s M, short dark hair, radar-sweep badge | `.opencode/images/armis-query-agent.png` |
| Sonny | sonny-the-soc-analyst | Electric yellow | Early-30s M, spiked dark hair, alert-bell headset | `.opencode/images/sonny-the-soc-analyst.png` |
| John Anderton | john-anderton-procog-analyst-clone | Slate gray | Late-50s M, graying hair, pinboard pocket pattern | `.opencode/images/john-anderton-procog-analyst-clone.png` |
| SOC Analyst | soc-analyst | Steel blue | Early-30s M, close-cropped hair, tactical vest | `.opencode/images/soc-analyst.png` |
| Tim | tim-the-threat-intel-analyst | Forest green | Mid-40s M, receding hair, rectangular glasses, pushpin lapel | `.opencode/images/tim-the-threat-intel-analyst.png` |
| CISOinaBox | cisoinabox | Burgundy red | Early-50s M, silver beard, angular glasses, gavel pin | `.opencode/images/cisoinabox.png` |
| Cody | cody-the-code-security-analyst | (existing) | (existing WebP avatar) | N/A - already uploaded |

## Note for Sync Tooling

The `openwebui` sync tool should embed avatars as `data:image/webp;base64,...` data URLs rather than relying on file-backed URLs when pushing agent models, since the chat UI only reliably renders `data:` URLs from `meta.profile_image_url`. WebP is preferred for its smaller payload size.