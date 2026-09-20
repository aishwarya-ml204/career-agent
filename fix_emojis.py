from pathlib import Path
import shutil

# Your existing Streamlit file
app_path = Path("app/app.py")

# Check that the file exists
if not app_path.exists():
    print("ERROR: app/app.py was not found.")
    print("Run this script from your career-agent project folder.")
    raise SystemExit(1)

# Create a backup before making changes
backup_path = Path("app/app_backup_before_emoji_fix.py")
shutil.copy2(app_path, backup_path)

# Read the existing file
text = app_path.read_text(encoding="utf-8")

# Replace corrupted emojis with correct Unicode emojis
replacements = {
    "ðŸ§­": "🧭",
    "ðŸ‘¤": "👤",
    "ðŸ“„": "📄",
    "ðŸ“": "📍",
    "â¤ï¸": "❤️",
    "âš™ï¸": "⚙️",
    "ðŸ†“": "🆓",
    "â°": "⏰",
    "ðŸš€": "🚀",
    "âŒ": "❌",
    "ðŸ”„": "🔄",
    "ðŸ›£ï¸": "🛣️",
    "ðŸŽ‰": "🎉",
    "ðŸ’»": "💻",
    "ðŸŽ“": "🎓",
    "ðŸ’¼": "💼",
    "ðŸ› ï¸": "🛠️",
    "â€¢": "•",
    "ðŸ“ˆ": "📈",
    "ðŸ¤–": "🤖",
    "ðŸ§ ": "🧠",
    "ðŸŽ¯": "🎯",
    "ðŸ“š": "📚",
    "ðŸ¢": "🏢",
    "âœ…": "✅",
    "âš ï¸": "⚠️",
    "ðŸ«": "🏫",
    "â±ï¸": "⏱️",
    "ðŸ’°": "💰",
    "ðŸ”—": "🔗",
    "ðŸ’¡": "💡",
}

# Apply replacements
fixed_count = 0

for corrupted, correct in replacements.items():
    count = text.count(corrupted)

    if count > 0:
        text = text.replace(corrupted, correct)
        fixed_count += count

# Save the corrected file as UTF-8
app_path.write_text(
    text,
    encoding="utf-8",
    newline="\n"
)

print("========================================")
print("EMOJI FIX COMPLETED")
print("========================================")
print(f"Replacements made: {fixed_count}")
print(f"Backup created: {backup_path}")
print(f"Updated file: {app_path}")
print("Encoding: UTF-8")
print("========================================")