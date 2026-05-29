charList = []
# Global tracking for chapters: {chapter_num: {"title": title, "lines": [story_elements]}}
story_chapters = {} 
current_chapter = None  

def chapter(number: int, title: str):
    """Sets the current active chapter for incoming dialogue, thoughts, and narration."""
    global current_chapter
    current_chapter = number
    if number not in story_chapters:
        story_chapters[number] = {"title": title, "lines": []}

def narrate(text: str):
    """Adds a standard narrator description block to the current chapter."""
    line = f"\n* {text} *\n"  # Italicized standalone text block for scene setting
    if current_chapter is not None:
        story_chapters[current_chapter]["lines"].append(line)
    return line

def narrateSilent(text: str):
    """Adds a narrator description block WITHOUT asterisks (raw text)."""
    line = f"\n{text}\n"
    if current_chapter is not None:
        story_chapters[current_chapter]["lines"].append(line)
    return line

def sceneBreak():
    """Adds a visual scene break (--- separator)."""
    line = "\n---\n"
    if current_chapter is not None:
        story_chapters[current_chapter]["lines"].append(line)
    return line

class Dialogue:
    def __init__(self, character):
        self.character = character

    def __call__(self, text, target=None):
        # Check if a target character object was provided
        if target:
            line = f"**{self.character.name}** (to {target.name}): \"{text}\""
        else:
            line = f"**{self.character.name}**: \"{text}\""
            
        if current_chapter is not None:
            story_chapters[current_chapter]["lines"].append(line)
        return line


class Thought:
    def __init__(self, character):
        self.character = character

    def __call__(self, text):
        # Format thought as italicized text inside brackets
        line = f"**{self.character.name}**: ({text})"
        if current_chapter is not None:
            story_chapters[current_chapter]["lines"].append(line)
        return line

class Character: 
    def __init__(self, role, name, age, power, powername="power", story=None): 
        self.role = role 
        self.name = name 
        self.age = age 
        self.power = power 
        self.powername = powername 
        self.story = story 
        charList.append(self)
        
        # Link both Dialogue and Thought to the character
        self.Dialogue = Dialogue(self)
        self.Thought = Thought(self)

    def __str__(self): 
        info = f"- **{self.name}** the {self.role} (Age: {self.age}, {self.powername}: {self.power})" 
        if self.story: 
            info += f" *-> {self.story}*" 
        return info

def writeMain(title, saveFile="manwha.md"):
    with open(saveFile, "w", encoding="utf-8") as f:
        # Title
        f.write(f"# {title}\n\n")
        
        # Character Profiles
        f.write(f"## Characters\n")
        for character in charList:
            f.write(f"{character}\n")
        f.write("\n---\n\n")  # Visual line break
        
        # Chapters and Script layout
        f.write(f"## Story Script\n\n")
        for num in sorted(story_chapters.keys()):
            ch_title = story_chapters[num]["title"]
            f.write(f"### Chapter {num}: {ch_title}\n\n")
            
            for line in story_chapters[num]["lines"]:
                # Narration lines don't need double spaces at the end, dialogue does
                if line.startswith("\n*"):
                    f.write(f"{line}\n")
                else:
                    f.write(f"{line}  \n")
            f.write("\n")
            
    print(f"Story has been written to '{saveFile}'")
