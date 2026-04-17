# AI Avatar Prompt Styling Guide

## Purpose

This guide defines the default visual direction for AI agent avatars in this repository.

Use it to write consistent image prompts that produce a recognizable family of avatars: polished chibi-style mascots with strong personality, clean presentation, and minimal visual clutter.

---

## Core visual style

- chibi / mascot-like character design
- expressive and memorable
- professional but fun
- product-mascot quality, not generic security clipart
- large expressive eyes
- soft polished shading
- clean outline work
- compact proportions
- centered character composition
- transparent PNG preferred

The target feel is a polished, modern mascot illustration that could represent a real product character.

---

## Character design rules

- Keep a consistent family style across all agents.
- Vary identity through hair, expression, clothing details, pose, prop choice, and primary color.
- Make the character feel specific, not like a stock avatar.
- Prompts should explicitly ask for personality and memorability.
- Encourage role inference from the agent's name or function where appropriate.
  - Example: Cody should read as a boy unless intentionally changed.
- Keep proportions compact and readable at small sizes.
- Favor clear silhouettes and facial readability over tiny detail.

---

## Composition rules

- Center the character.
- Compose for avatar use first.
- Prefer waist-up or full compact figure framing that still reads well when cropped.
- Keep the character as the main subject with no competing elements.
- Use a clean pose with one obvious focal point.

---

## Background rules

- Keep avatars transparent when possible.
- Use no background or only extremely subtle background treatment if transparency is not possible.
- Avoid scenes, environments, desks, rooms, dashboards, or visual storytelling backgrounds.
- Let OpenWebUI framing handle presentation.
- Do not bake in circles, badges, frames, halos, shields, or background containers behind the character.

---

## Props and role cues

- Role-specific props and details are allowed, but should be restrained.
- Prefer one subtle prop, or two at most.
- Props should support role recognition without cluttering the avatar.
- Examples of acceptable cues:
  - analyst: tablet, notebook, subtle lens, headset
  - engineer: small laptop, code badge, understated tool cue
  - threat intel: document, pinboard cue, subtle map/data reference
  - compliance: clipboard, folder, checklist cue
- Clothing details, insignia, color accents, and expression should do as much work as props.

---

## Color system

- Each agent should have one unique primary color.
- The primary color should be immediately recognizable and reusable across future variants.
- Use the primary color in clothing accents, accessories, props, or small interface details.
- Keep the rest of the palette controlled and complementary.
- Avoid rainbow palettes or over-saturated multi-color effects.
- If a team of avatars is viewed together, each should feel distinct at a glance because of primary color plus character details.

Recommended approach per avatar:

- 1 primary color
- 1-2 supporting neutrals
- optional subtle secondary accent only if needed

---

## Prompt writing rules

- Explicitly request a polished chibi mascot avatar.
- Explicitly request personality, memorability, and product-mascot quality.
- State the role and emotional tone.
- Call out the character's likely presentation when useful from name/function.
- Specify transparent background / transparent PNG when supported.
- Specify centered composition and minimal background.
- Specify clean outlines, soft polished shading, and large expressive eyes.
- Mention the unique primary color.
- Keep role cues restrained and specific.
- Ask for minimal clutter and no generic cyber decoration.

Good prompt ingredients:

- role identity
- personality adjectives
- chibi mascot styling
- primary color
- restrained prop cue
- transparent background
- centered composition
- polished commercial illustration quality

---

## Negative prompt / avoid list

Avoid:

- busy floating UI
- random locks
- digital particles
- excessive symbols
- generic cyber clutter
- circuit wallpaper backgrounds
- dramatic environment scenes
- framing circles or shapes behind the character
- badge-style containers
- crowded compositions
- too many props
- realistic photo style
- generic corporate headshot look
- low-detail clipart look
- overly dark or muddy lighting
- unreadable tiny accessories

---

## Base prompt template

```text
Create a polished chibi mascot-style avatar for [Agent Name], an AI agent for [role/function].

The character should feel [personality traits] and instantly memorable, with product-mascot quality rather than generic stock security art. Use large expressive eyes, clean outline work, soft polished shading, compact proportions, and a centered composition.

Use [primary color] as the unique primary color for this agent, supported by restrained neutral accents. Include [one subtle role-specific prop or clothing cue], but keep the design uncluttered.

Prefer a transparent background / transparent PNG. Use minimal or no background elements. Do not include framing circles, badges, or graphic shapes behind the character.

The final avatar should look professional but fun, readable at small sizes, and visually consistent with a family of related AI agent mascots.
```

---

## Variant prompt template

```text
Design a centered avatar illustration of [Agent Name], a [gender presentation if relevant] AI agent focused on [role/function]. Keep the same polished family style as the other agents: chibi mascot design, large expressive eyes, compact proportions, clean linework, soft polished shading, and high-end product mascot quality.

Make this version distinct through [expression], [hair/style detail], [clothing detail], and [primary color] as the signature color. Include only [prop] as a subtle role cue. Keep the personality [adjectives].

Use a transparent background if possible. Avoid scenes, floating UI, locks, particles, cyber clutter, circles, badges, and background containers. Minimal background only.
```

---

## Review checklist

Before approving an avatar prompt or output, check:

- Is it clearly chibi / mascot-like?
- Does it feel expressive and memorable?
- Does it look professional but still fun?
- Is the character centered and readable at avatar size?
- Is the background transparent or minimal?
- Are there no circles, badges, or framing shapes behind the character?
- Is the design free of random cyber clutter?
- Is there only one main primary color for this agent?
- Are props restrained to one or two subtle cues max?
- Does it feel like part of a consistent family while still being distinct?
- Does it avoid generic clipart or stock-avatar energy?
- Does the avatar visually fit the agent's name and role?

---

## Default style summary

If in doubt, aim for this:

**A transparent-background, polished chibi product mascot with big expressive eyes, clean outlines, soft shading, compact proportions, centered composition, one unique primary color, and only minimal role-specific detail.**
