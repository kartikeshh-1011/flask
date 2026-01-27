import os
import re

TEMPLATE_DIR = r"c:\Users\LOQ\OneDrive\Desktop\flask\templates"

def fix_external_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find {{ url_for('static', filename='http...') }} and revert it
    # Pattern: {{ url_for('static', filename='(http[^']+)') }}
    # We want to replace it with just \1
    
    # Handle single quotes around filename
    def replacer(match):
        url = match.group(1)
        return url

    # Matches: {{ url_for('static', filename='http...') }}
    # Note: spacing might vary, regex handles standard spacing
    content = re.sub(r"\{\{\s*url_for\('static',\s*filename='(https?://[^']+)'\)\s*\}\}", replacer, content)
    
    # Also handle double quotes if they were used in the match (though my previous script used single)
    content = re.sub(r'\{\{\s*url_for\("static",\s*filename="(https?://[^"]+)"\)\s*\}\}', replacer, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed external links in {filepath}")

for filename in os.listdir(TEMPLATE_DIR):
    if filename.endswith(".html"):
        fix_external_links(os.path.join(TEMPLATE_DIR, filename))
