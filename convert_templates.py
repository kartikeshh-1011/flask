"""
Script to convert all HTML templates to use the base.html template
This will extract the main content from each page and wrap it in the base template
"""

import os
import re

# Templates directory
TEMPLATES_DIR = r"C:\Users\LOQ\OneDrive\Desktop\flask\templates"

# Files to skip (already converted or special cases)
SKIP_FILES = ['base.html', 'home.html', 'login.html', 'signup.html', 'forgot.html', 'newpass.html']

# Simple templates that just need content extraction
SIMPLE_PAGES = [
    'contact.html', 'feedback.html', 'complain.html', 'aboutus.html', 
    'gallery.html', 'event.html', 'result.html', 'addmision.html',
    'course.html', 'academic.html', 'nonacademic.html',
    'view_admissions.html', 'update_result.html'
]

def extract_content_between_header_footer(html_content):
    """Extract content between header and footer"""
    # Find content after </header> and before <footer
    header_end = html_content.rfind('</header>')
    footer_start = html_content.find('<footer', header_end if header_end != -1 else 0)
    
    if header_end != -1 and footer_start != -1:
        content = html_content[header_end + 9:footer_start]
        return content.strip()
    return None

def extract_css_files(html_content):
    """Extract CSS file references from head"""
    css_files = []
    css_pattern = r'<link[^>]*href=["\']{{url_for\([\'"]static[\'"],\s*filename=[\'"]([^"\']+)[\'"]\)["\'][^>]*>'
    matches = re.findall(css_pattern, html_content)
    css_files.extend(matches)
    
    # Also check for simple href patterns
    simple_pattern = r'<link[^>]*href=["\']{{[^}]+filename=[\'"]([^"\']+\.css)[\'"][^}]*}}["\'][^>]*>'
    matches = re.findall(simple_pattern, html_content)
    css_files.extend(matches)
    
    return list(set(css_files))  # Remove duplicates

def extract_title(html_content):
    """Extract page title"""
    title_match = re.search(r'<title>([^<]+)</title>', html_content)
    if title_match:
        return title_match.group(1)
    return "Apex Learning Hub"

def extract_flash_messages_block(html_content):
    """Extract flash messages block if present"""
    flash_pattern = r'{% with messages = get_flashed_messages.*?{% endwith %}'
    match = re.search(flash_pattern, html_content, re.DOTALL)
    if match:
        return match.group(0)
    return None

def convert_template(filename):
    """Convert a single template to use base.html"""
    filepath = os.path.join(TEMPLATES_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filename}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Extract components
    title = extract_title(original_content)
    css_files = extract_css_files(original_content)
    main_content = extract_content_between_header_footer(original_content)
    flash_block = extract_flash_messages_block(original_content)
    
    if not main_content:
        print(f"⚠️  Could not extract content from {filename}")
        return False
    
    # Build new template
    new_template = '{% extends "base.html" %}\n\n'
    new_template += f'{{% block title %}}{title}{{% endblock %}}\n\n'
    
    # Add CSS block if there are CSS files
    if css_files:
        new_template += '{% block extra_css %}\n'
        for css_file in css_files:
            new_template += f'<link rel="stylesheet" href="{{{{url_for(\'static\', filename=\'{css_file}\')}}}}\">\n'
        new_template += '{% endblock %}\n\n'
    
    # Add content block
    new_template += '{% block content %}\n'
    
    # Add flash messages if present
    if flash_block:
        new_template += flash_block + '\n'
    
    new_template += main_content + '\n'
    new_template += '{% endblock %}\n'
    
    # Backup original
    backup_path = filepath + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    
    # Write new template
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_template)
    
    print(f"✅ Converted {filename} (backup saved)")
    return True

def main():
    print("🚀 Starting template conversion...\n")
    
    converted = 0
    failed = 0
    
    for filename in SIMPLE_PAGES:
        if filename in SKIP_FILES:
            continue
        
        print(f"Converting {filename}...")
        if convert_template(filename):
            converted += 1
        else:
            failed += 1
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Converted: {converted}")
    print(f"   ❌ Failed: {failed}")
    print(f"\n💡 Note: Original files backed up with .backup extension")

if __name__ == "__main__":
    main()
