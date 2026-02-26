import os
import re

# List of CSS files to update
css_files = [
    'static/XII.css', 'static/XI.css', 'static/X.css', 'static/VIII.css',
    'static/VII.css', 'static/VI.css', 'static/V.css', 'static/SAINIKI.css',
    'static/result.css', 'static/physicsteacher.css', 'static/OLYMPIADS.css',
    'static/nonacademic.css', 'static/NaVODAYA.css', 'static/mathteacher.css',
    'static/KVPY.css', 'static/IX.css', 'static/gallery.css', 'static/feedback.css',
    'static/event.css', 'static/englishteacher.css', 'static/drawingteacher.css',
    'static/course.css', 'static/contact.css', 'static/complain.css',
    'static/academic.css', 'static/aboutus.css'
]

# Old CSS pattern for #first and #new
old_first_pattern = r'#first\s*\{[^}]*\}'
old_new_pattern = r'#new\s*\{[^}]*\}'

# New CSS for #first and #new
new_first_css = '''#first{
    height: 35px;
    width: 100%;
    background-color: #29629d;
    color: yellow;
    padding-top: 8px;
    position: relative;
}'''

new_new_css = '''#new{
    background-color: #29909d;
    color: white;
    height: 35px;
    width: 120px;
    position: absolute;
    left: 50px;
    top: 0;
    text-align: center;
    padding-top: 8px;
    z-index: 10;
    font-weight: bold;
}'''

# Add #news-content styling
news_content_css = '''#news-content{
    color: yellow;
    font-size: 16px;
}'''

for css_file in css_files:
    file_path = os.path.join(r'c:\Users\LOQ\OneDrive\Desktop\flask', css_file)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace #first styling
        content = re.sub(old_first_pattern, new_first_css, content, flags=re.DOTALL)
        
        # Replace #new styling
        content = re.sub(old_new_pattern, new_new_css, content, flags=re.DOTALL)
        
        # Add #news-content if not present
        if '#news-content' not in content:
            # Insert after #new block
            content = content.replace(new_new_css, new_new_css + '\n' + news_content_css)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'Updated: {css_file}')
    else:
        print(f'File not found: {css_file}')

print('\nAll CSS files updated successfully!')
