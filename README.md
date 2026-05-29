# Manwha Module Documentation

A lightweight Python module for writing **text-based manhwas** with structured dialogue, narration, and character management. Output is rendered as clean, readable Markdown.

---

## Table of Contents
1. [Installation & Setup](#installation--setup)
2. [Core Concepts](#core-concepts)
3. [API Reference](#api-reference)
4. [Examples](#examples)
5. [Output Format](#output-format)

---

## Installation & Setup

```bash
pip install manwha
```

and

```python
import manwha
```

That's it! Import the module and start building your story.

---

## Core Concepts

### Characters
Every story needs a cast. Define characters once, use them throughout.

```python
hero = manwha.Character(
    role="Protagonist",
    name="Kaelen",
    age=19,
    power="Spatial Manipulation",
    powername="Void Step"
)
```

Characters are automatically registered in `manwha.charList` and appear in your final markdown output.

### Chapters
Stories are organized into chapters. Set the active chapter before adding any content.

```python
manwha.chapter(1, "The Awakening")
```

All subsequent narration, dialogue, and thoughts are added to this chapter until you call `chapter()` again.

### Story Elements
Four main ways to add content to a chapter:
- **Narration** — Scene description (with emphasis)
- **Silent Narration** — Scene description (plain text)
- **Dialogue** — Character speech
- **Thoughts** — Internal monologue

---

## API Reference

### `Character(role, name, age, power, powername="power", story=None)`

Creates a character for your story.

**Parameters:**
- `role` (str) — Character's role (e.g., "Protagonist", "Antagonist", "Ally")
- `name` (str) — Character's name
- `age` (int) — Character's age
- `power` (str) — Description of their power
- `powername` (str, optional) — Name of their power ability (default: `"power"`)
- `story` (str, optional) — Brief character backstory/description

**Returns:** Character object

**Example:**
```python
vesper = manwha.Character(
    role="Antagonist",
    name="Vesper",
    age=22,
    power="Chronos Anchor",
    powername="Frozen Second",
    story="A rogue time manipulator seeking to rewrite the past"
)
```

---

### `chapter(number, title)`

Sets the active chapter for incoming content.

**Parameters:**
- `number` (int) — Chapter number
- `title` (str) — Chapter title

**Returns:** None

**Example:**
```python
manwha.chapter(1, "The Fracture")
manwha.chapter(2, "Rising Shadows")
```

---

### `narrate(text)`

Adds a narrator description block with asterisk emphasis (rendered as italicized text).

**Parameters:**
- `text` (str) — The narrative description

**Returns:** Formatted line string

**Example:**
```python
manwha.narrate("The sky tears open like wet paper.")
```

**Output:**
```
* The sky tears open like wet paper. *
```

---

### `narrateSilent(text)`

Adds a narrator description block **without** asterisks (plain text).

**Parameters:**
- `text` (str) — The narrative description

**Returns:** Formatted line string

**Example:**
```python
manwha.narrateSilent("Three hours later...")
```

**Output:**
```
Three hours later...
```

---

### `sceneBreak()`

Adds a visual scene break separator (`---`).

**Parameters:** None

**Returns:** Separator string

**Example:**
```python
manwha.sceneBreak()
```

**Output:**
```
---
```

---

### `character.Dialogue(text, target=None)`

Character speaks. Creates a dialogue line.

**Parameters:**
- `text` (str) — What the character says
- `target` (Character, optional) — If dialogue is directed at another character, include them here

**Returns:** Formatted dialogue string

**Example:**
```python
kaelen.Dialogue("Where am I?")
vesper.Dialogue("You're in my domain now.", target=kaelen)
```

**Output:**
```
**Kaelen**: "Where am I?"
**Vesper** (to Kaelen): "You're in my domain now."
```

---

### `character.Thought(text)`

Character has an internal thought. Formats as thought (in parentheses).

**Parameters:**
- `text` (str) — The internal monologue

**Returns:** Formatted thought string

**Example:**
```python
kaelen.Thought("His power... it's evolved.")
```

**Output:**
```
**Kaelen**: (His power... it's evolved.)
```

---

### `writeMain(title, saveFile="manwha.md")`

Exports your entire story to a Markdown file.

**Parameters:**
- `title` (str) — Story title (appears as H1 header)
- `saveFile` (str, optional) — Output filename (default: `"manwha.md"`)

**Returns:** None (prints confirmation message)

**Example:**
```python
manwha.writeMain("Echoes of the Aether", saveFile="my_story.md")
```

---

## Examples

### Simple Scene
```python
import manwha

# Define character
hero = manwha.Character(
    role="Protagonist",
    name="Kaelen",
    age=19,
    power="Spatial Manipulation",
    powername="Void Step"
)

# Set chapter
manwha.chapter(1, "First Light")

# Add content
manwha.narrate("The morning sun breaks through the clouds.")
hero.Thought("Another day. Another battle.")
hero.Dialogue("Time to train.")

# Export
manwha.writeMain("My Story")
```

---

### Multi-Character Scene with Scene Break
```python
import manwha

# Characters
hero = manwha.Character("Protagonist", "Kaelen", 19, "Spatial Manipulation", "Void Step")
rival = manwha.Character("Antagonist", "Vesper", 22, "Chronos Anchor", "Frozen Second")

# Story
manwha.chapter(1, "The Confrontation")

manwha.narrate("They stand face to face in the ruins of the tower.")

hero.Dialogue("Vesper! Why have you done this?")
rival.Thought("Naive. He still doesn't understand.")
rival.Dialogue("Because the old world must fall.", target=hero)

manwha.sceneBreak()

manwha.narrateSilent("Hours later, the battle concluded...")

hero.Thought("I'm alive. But at what cost?")

manwha.writeMain("Clash of Titans")
```

---

### Using Markdown Formatting in Text
You can use **Markdown syntax** directly in your text for emphasis:

```python
manwha.narrate("Reality *bends* at the seams as **ancient power** awakens.")
hero.Dialogue("This is ***impossible***!")
```

---

## Output Format

### File Structure
The exported Markdown file has the following structure:

```
# Story Title

## Characters
- **Name** the Role (Age: XX, PowerName: Power Description)
- **Name** the Role (Age: XX, PowerName: Power Description)

---

## Story Script

### Chapter 1: Chapter Title

* Narrated scene description. *

**Character**: "Dialogue"

**Character**: (Internal thought)

---

### Chapter 2: Next Chapter Title

...
```

### Character List
- Auto-generated from all `Character()` instances
- Shows: Name, Role, Age, Power Name, Power Description
- Appears at the top of the file for easy reference

### Story Script
- Organized by chapter number (in order)
- Narration appears in `* asterisks *`
- Silent narration appears as plain text
- Dialogue and thoughts are clearly attributed to characters
- Scene breaks appear as `---`

---

## Tips & Tricks

### 1. Use `narrateSilent()` for Smooth Transitions
```python
manwha.narrate("The battle raged for hours.")
manwha.sceneBreak()
manwha.narrateSilent("By dawn, the dust had settled.")
```

### 2. Markdown Emphasis Works Everywhere
```python
hero.Dialogue("I won't let this ***happen*** again!")
manwha.narrate("The sky **burns** with **crimson** light.")
```

### 3. Direct Dialogue to Specific Characters
```python
hero.Dialogue("Why did you betray us?", target=villain)
# Output: **Hero** (to Villain): "Why did you betray us?"
```

### 4. Use Story Parameter for Character Bio
```python
mage = manwha.Character(
    role="Ally",
    name="Mira",
    age=18,
    power="Aether Sense",
    powername="Echo Sight",
    story="A gifted mage haunted by her past"
)
```

### 5. Multiple Chapters in One Script
```python
manwha.chapter(1, "The Beginning")
# ... add content ...

manwha.chapter(2, "The Storm")
# ... add more content ...

manwha.chapter(3, "The Truth")
# ... add even more ...

manwha.writeMain("Epic Story")
# All chapters exported in order!
```

---

## Global Variables

### `manwha.charList`
List of all `Character` objects created. Auto-populated when you instantiate a character.

### `manwha.story_chapters`
Dictionary of all chapters: `{chapter_num: {"title": title, "lines": [story_elements]}}`.

### `manwha.current_chapter`
Currently active chapter number. Set via `chapter()` function.

---

## License & Credits

Built for text-based manhwa enthusiasts. Have fun creating!
