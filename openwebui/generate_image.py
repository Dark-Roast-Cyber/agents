"""Generate a single image with the OpenAI Images API and save it locally."""

from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

API_URL = "https://api.openai.com/v1/images/generations"
DEFAULT_MODEL = "gpt-image-1.5"
DEFAULT_TIMEOUT = 60.0
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


class ImageGenerationError(RuntimeError):
    """Raised when image generation fails."""


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", required=True, help="Prompt for the image")
    parser.add_argument("--output", required=True, help="Local output file path")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Image model to use")
    parser.add_argument("--size", default="1024x1024", help="Requested image size")
    parser.add_argument("--quality", default="high", help="Requested image quality")
    parser.add_argument(
        "--background", default="opaque", help="Requested background mode"
    )
    parser.add_argument(
        "--format",
        default="png",
        help="Output format to request from the API",
    )
    return parser.parse_args()


def get_api_key() -> str:
    """Return the OpenAI API key from the environment."""
    load_dotenv(ENV_PATH)
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API")
    if not api_key:
        raise ImageGenerationError(
            "Missing API key. Set OPENAI_API_KEY or OPEN_AI_API."
        )
    return api_key


def extract_error_detail(response: httpx.Response) -> str:
    """Extract a concise error detail from an API response."""
    try:
        payload = response.json()
    except ValueError:
        return response.text.strip() or response.reason_phrase

    error = payload.get("error")
    if isinstance(error, dict):
        message = error.get("message")
        code = error.get("code")
        if message and code:
            return f"{message} (code: {code})"
        if message:
            return str(message)
    return str(payload)


def request_image(api_key: str, args: argparse.Namespace) -> bytes:
    """Request an image and return the decoded bytes."""
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "quality": args.quality,
        "background": args.background,
        "output_format": args.format,
        "n": 1,
    }
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            response = client.post(API_URL, json=payload, headers=headers)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = extract_error_detail(exc.response)
        raise ImageGenerationError(
            f"OpenAI API request failed with {exc.response.status_code}: {detail}"
        ) from exc
    except httpx.HTTPError as exc:
        raise ImageGenerationError(f"OpenAI API request failed: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise ImageGenerationError("OpenAI API returned invalid JSON.") from exc

    items = data.get("data")
    if not isinstance(items, list) or not items:
        raise ImageGenerationError("OpenAI API response did not include image data.")

    image_item = items[0]
    if not isinstance(image_item, dict) or "b64_json" not in image_item:
        raise ImageGenerationError(
            "OpenAI API response did not include base64 image content."
        )

    try:
        return base64.b64decode(image_item["b64_json"])
    except (ValueError, TypeError) as exc:
        raise ImageGenerationError(
            "Failed to decode image bytes from API response."
        ) from exc


def save_image(image_bytes: bytes, output_path: str) -> Path:
    """Write image bytes to disk and return the resolved path."""
    path = Path(output_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(image_bytes)
    return path.resolve()


def main() -> int:
    """Run the image generation CLI."""
    args = parse_args()

    try:
        api_key = get_api_key()
        image_bytes = request_image(api_key, args)
        saved_path = save_image(image_bytes, args.output)
    except ImageGenerationError as exc:
        raise SystemExit(f"Error: {exc}")

    print(f"Saved image to {saved_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
