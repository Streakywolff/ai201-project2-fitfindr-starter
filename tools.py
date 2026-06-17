"""
tools.py

The three required FitFindr tools. Each tool is a standalone function that
can be called and tested independently before being wired into the agent loop.

Complete and test each tool before moving to agent.py.

Tools:
    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)              → str
    create_fit_card(outfit, new_item)               → str
"""

import os

from dotenv import load_dotenv
from groq import Groq

from utils.data_loader import (
    load_listings,
    get_example_wardrobe,
    get_empty_wardrobe
)
load_dotenv()


# ── Groq client ───────────────────────────────────────────────────────────────

def _get_groq_client():
    """Initialize and return a Groq client using GROQ_API_KEY from .env."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to a .env file in the project root."
        )
    return Groq(api_key=api_key)


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    listings = load_listings()

    keywords = description.lower().split()
    matches = []

    for item in listings:
        if max_price is not None and item["price"] > max_price:
            continue

        if size:
            user_size = size.lower()
            item_size = item["size"].lower()

            if user_size not in item_size:
                continue

        searchable_text = " ".join([
            item.get("title", ""),
            item.get("description", ""),
            item.get("category", ""),
            " ".join(item.get("style_tags", [])),
            " ".join(item.get("colors", [])),
            str(item.get("brand", "")),
            item.get("platform", "")
        ]).lower()

        score = 0

        for keyword in keywords:
            if keyword in searchable_text:
                score += 1

        if score > 0:
            matches.append((score, item))

    matches.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in matches]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    items = wardrobe.get("items", [])

    client = _get_groq_client()

    if not items:
        prompt = f"""
You are a helpful fashion stylist.

The user is considering this thrifted item:
Title: {new_item.get("title")}
Description: {new_item.get("description")}
Category: {new_item.get("category")}
Colors: {new_item.get("colors")}
Style tags: {new_item.get("style_tags")}

The user's wardrobe is empty.

Suggest 1 complete outfit using common pieces someone might own.
Keep it practical, specific, and casual.
"""
    else:
        wardrobe_text = ""

        for item in items:
            wardrobe_text += (
                f"- {item.get('name')} "
                f"({item.get('category')}, colors: {item.get('colors')}, "
                f"style: {item.get('style_tags')})\n"
            )

        prompt = f"""
You are a helpful fashion stylist.

The user is considering buying this thrifted item:
Title: {new_item.get("title")}
Description: {new_item.get("description")}
Category: {new_item.get("category")}
Colors: {new_item.get("colors")}
Style tags: {new_item.get("style_tags")}
Price: ${new_item.get("price")}
Platform: {new_item.get("platform")}

Here is the user's current wardrobe:
{wardrobe_text}

Suggest 1-2 complete outfits using the thrifted item and named pieces from the wardrobe.
Mention the specific wardrobe pieces by name.
Keep the advice casual, useful, and not too long.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a casual fashion stylist for secondhand clothing."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:

    if not outfit or not outfit.strip():
        return "Unable to create fit card because no outfit suggestion was provided."

    client = _get_groq_client()

    prompt = f"""
Create a short social media caption.

Item:
Title: {new_item.get("title")}
Price: ${new_item.get("price")}
Platform: {new_item.get("platform")}

Outfit:
{outfit}

Requirements:
- 2 to 4 sentences
- Casual and authentic
- Mention the item, price, and platform naturally
- Sound like a real Instagram or TikTok outfit post
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You write short outfit captions for thrifted fashion."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.9,
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    results = search_listings(
        "vintage graphic tee",
        None,
        30
    )

    selected_item = results[0]

    wardrobe = get_example_wardrobe()

    outfit = suggest_outfit(
        selected_item,
        wardrobe
    )

    fit_card = create_fit_card(
        outfit,
        selected_item
    )

    print("\nFIT CARD:")
    print(fit_card)