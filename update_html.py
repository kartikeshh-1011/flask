import os
import re

# List of HTML files that have standalone marquee sections
html_files = [
    'templates/NAVODAYA.html', 'templates/KVPY.html', 'templates/SAINIKI.html',
    'templates/OLYMPIADS.html', 'templates/V.html', 'templates/VI.html',
    'templates/VII.html', 'templates/VIII.html', 'templates/IX.html',
    'templates/X.html', 'templates/XI.html', 'templates/XII.html',
    'templates/drawingteacher.html', 'templates/englishteacher.html',
    'templates/mathteacher.html', 'templates/physicsteacher.html'
]

# New marquee HTML structure
new_marquee_html = '''<div id="first">
        <div id="new">Latest News</div>
        <marquee behavior="" direction="left"> <div id="news-content">Latest News:   22 January 2026  Check Your Result 
       </div></marquee>
    </div>'''

for html_file in html_files:
    file_path = os.path.join(r'c:\Users\LOQ\OneDrive\Desktop\flask', html_file)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match the old marquee structure
        # Looking for <div id="first">...</div> with marquee inside
        old_pattern = r'<div id="first">.*?</div>\s*(?=<div id="second">)'
        
        # Replace with new structure
        content = re.sub(old_pattern, new_marquee_html + '\n    ', content, flags=re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'Updated: {html_file}')
    else:
        print(f'File not found: {html_file}')

print('\nAll HTML files updated successfully!')
