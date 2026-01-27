import os
import re

TEMPLATE_DIR = r"c:\Users\LOQ\OneDrive\Desktop\flask\templates"

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex for CSS links not already using url_for
    # Matches href="something.css" but not href="{{..."
    # Note: simple check.
    
    def css_replacer(match):
        full_match = match.group(0)
        filename = match.group(1)
        if "{{" in full_match: return full_match
        return f'href="{{{{ url_for(\'static\', filename=\'{filename}\') }}}}"'

    content = re.sub(r'href="([^"]+\.css)"', css_replacer, content)

    # Regex for Images
    # src="something.png/jpg/jpeg"
    def img_replacer(match):
        full_match = match.group(0)
        filename = match.group(1)
        if "{{" in full_match: return full_match
        # Check if it's an external link (http/https)
        if filename.startswith('http'): return full_match
        return f'src="{{{{ url_for(\'static\', filename=\'{filename}\') }}}}"'

    content = re.sub(r'src="([^"]+\.(?:png|jpg|jpeg|gif))"', img_replacer, content)

    # Regex for Shortcut Icon
    # link rel="shortcut icon" href="..."
    # This is trickier because href matches above.
    # Actually checking href="... .jpeg" or similar in <link> might be covered by general href replacer if I expand it?
    # But usually href is used for .css or links.
    # Let's fix specific file extensions in href.
    
    def icon_replacer(match):
        full_match = match.group(0)
        filename = match.group(1)
        if "{{" in full_match: return full_match
        return f'href="{{{{ url_for(\'static\', filename=\'{filename}\') }}}}"'

    content = re.sub(r'href="([^"]+\.(?:jpeg|jpg|png|ico))"', icon_replacer, content)

    # Inject responsive.css if NOT present
    if "responsive.css" not in content:
        # Try to insert after the last <link ...> tag or before </head>
        if "</head>" in content:
            responsive_link = f'\n    <link rel="stylesheet" href="{{{{ url_for(\'static\', filename=\'responsive.css\') }}}}">'
            content = content.replace("</head>", responsive_link + "\n</head>")


    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filepath}")

for filename in os.listdir(TEMPLATE_DIR):
    if filename.endswith(".html"):
        fix_file(os.path.join(TEMPLATE_DIR, filename))
