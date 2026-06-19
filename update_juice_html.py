import json
import os

ITEMS = [
    ("red-mojito", "Red Mojito Juice", "عصير موهيتو أحمر", "One Size", 15, "single"),
    ("lemon-mint", "Lemon with Mint", "ليمون بالنعناع", "One Size", 15, "single"),
    ("orange-juice", "Orange Juice", "عصير برتقال", "One Size", 16, "single"),
    ("saudi-champagne", "Saudi Champagne", "شمبانيا سعودي", None, None, "multi-sizes"),
    ("tea", "Tea", "شاي", "One Size", 7, "single"),
    ("thai-hot-tea-lemon", "Thai Hot Tea with Lemon", "شاي تايلندي ساخن بالليمون", None, None, "multi-sizes"),
    ("thai-ice-tea-lemon", "Thai Ice Tea with Lemon", "شاي تايلندي مثلج بالليمون", None, None, "multi-sizes"),
    ("thai-ice-tea-milk", "Thai Ice Tea with Milk", "شاي تايلندي مثلج بالحليب", None, None, "multi-sizes"),
    ("water", "Water", "ماء", "One Size", 2, "single"),
    ("mineral-water", "Mineral Water", "مياه معدنية", "One Size", 14, "single"),
    ("pepsi", "Pepsi", "بيبسي", "One Size", 4, "single"),
    ("coca-cola", "Coca-Cola", "كوكاكولا", "One Size", 4, "single"),
]

# TEMPLATES
single_template = '''        <div class="menu-item featured-item" data-aos="fade-up">
      <div class="featured-heading">
        <span class="item-name-ar">{ar}</span>
        <span class="item-name-en">{en}</span>
      </div>
      <div class="featured-body">
        <div class="featured-img">
          <img class="dish-img-featured" src="juice-{key}.jpg" alt="{en}">
        </div>
        <div class="featured-sizes">
          <div class="item-size-single">
        <span class="item-size">{size}</span>
      </div>
      <div class="item-price-single">
        <span class="price-val">{price}</span>
        <span class="price-cur">SR</span>
      </div>
        </div>
      </div>
    </div>'''

multi_template = '''        <div class="menu-item featured-item" data-aos="fade-up">
      <div class="featured-heading">
        <span class="item-name-ar">{ar}</span>
        <span class="item-name-en">{en}</span>
      </div>
      <div class="featured-body">
        <div class="featured-img">
          <img class="dish-img-featured" src="juice-{key}.jpg" alt="{en}">
        </div>
        <div class="featured-sizes">
          
    {table}
        </div>
      </div>
    </div>'''

# Build replacement dict: old HTML -> new HTML
with open("/tmp/tom-yum-kung-menu/index.html", "r") as f:
    html = f.read()

replacements = {
    "Red Mojito Juice": single_template.format(key="red-mojito", en="Red Mojito Juice", ar="عصير موهيتو أحمر", size="One Size", price=15),
    "Lemon with Mint": single_template.format(key="lemon-mint", en="Lemon with Mint", ar="ليمون بالنعناع", size="One Size", price=15),
    "Orange Juice": single_template.format(key="orange-juice", en="Orange Juice", ar="عصير برتقال", size="One Size", price=16),
    "Saudi Champagne": multi_template.format(key="saudi-champagne", en="Saudi Champagne", ar="شمبانيا سعودي", table="""    <table class="sz-table">
      <thead>
        <tr><th class="sz-th">L</th><th class="sz-th">S</th><th class="sz-th sz-th-last">Calories</th></tr>
      </thead>
      <tbody>
        <tr><td class="sz-td-price">33 <span class="sz-cur">SR</span></td><td class="sz-td-price">15 <span class="sz-cur">SR</span></td><td class="sz-td-label">Price</td></tr>
        <tr><td class="sz-td-cal">&mdash;</td><td class="sz-td-cal">&mdash;</td><td class="sz-td-label">Cal</td></tr>
      </tbody>
    </table>"""),
    "Tea": single_template.format(key="tea", en="Tea", ar="شاي", size="One Size", price=7),
    "Thai Hot Tea with Lemon": multi_template.format(key="thai-hot-tea-lemon", en="Thai Hot Tea with Lemon", ar="شاي تايلندي ساخن بالليمون", table="""    <table class="sz-table">
      <thead>
        <tr><th class="sz-th">M</th><th class="sz-th">L</th><th class="sz-th">S</th><th class="sz-th sz-th-last">Calories</th></tr>
      </thead>
      <tbody>
        <tr><td class="sz-td-price">22 <span class="sz-cur">SR</span></td><td class="sz-td-price">28 <span class="sz-cur">SR</span></td><td class="sz-td-price">9 <span class="sz-cur">SR</span></td><td class="sz-td-label">Price</td></tr>
        <tr><td class="sz-td-cal">&mdash;</td><td class="sz-td-cal">&mdash;</td><td class="sz-td-cal">&mdash;</td><td class="sz-td-label">Cal</td></tr>
      </tbody>
    </table>"""),
    "Thai Ice Tea with Lemon": multi_template.format(key="thai-ice-tea-lemon", en="Thai Ice Tea with Lemon", ar="شاي تايلندي مثلج بالليمون", table="""    <table class="sz-table">
      <thead>
        <tr><th class="sz-th">M</th><th class="sz-th">L</th><th class="sz-th">S</th><th class="sz-th sz-th-last">Calories</th></tr>
      </thead>
      <tbody>
        <tr><td class="sz-td-price">20 <span class="sz-cur">SR</span></td><td class="sz-td-price">27 <span class="sz-cur">SR</span></td><td class="sz-td-price">9 <span class="sz-cur">SR</span></td><td class="sz-td-label">Price</td></tr>
        <tr><td class="sz-td-cal">&mdash;</td><td class="sz-td-cal">&mdash;</td><td class="sz-td-cal">&mdash;</td><td class="sz-td-label">Cal</td></tr>
      </tbody>
    </table>"""),
    "Thai Ice Tea with Milk": multi_template.format(key="thai-ice-tea-milk", en="Thai Ice Tea with Milk", ar="شاي تايلندي مثلج بالحليب", table="""    <table class="sz-table">
      <thead>
        <tr><th class="sz-th">M</th><th class="sz-th">L</th><th class="sz-th">S</th><th class="sz-th sz-th-last">Calories</th></tr>
      </thead>
      <tbody>
        <tr><td class="sz-td-price">25 <span class="sz-cur">SR</span></td><td class="sz-td-price">38 <span class="sz-cur">SR</span></td><td class="sz-td-price">15 <span class="sz-cur">SR</span></td><td class="sz-td-label">Price</td></tr>
        <tr><td class="sz-td-cal">&mdash;</td><td class="sz-td-cal">&mdash;</td><td class="sz-td-cal">&mdash;</td><td class="sz-td-label">Cal</td></tr>
      </tbody>
    </table>"""),
    "Water": single_template.format(key="water", en="Water", ar="ماء", size="One Size", price=2),
    "Mineral Water": single_template.format(key="mineral-water", en="Mineral Water", ar="مياه معدنية", size="One Size", price=14),
    "Pepsi": single_template.format(key="pepsi", en="Pepsi", ar="بيبسي", size="One Size", price=4),
    "Coca-Cola": single_template.format(key="coca-cola", en="Coca-Cola", ar="كوكاكولا", size="One Size", price=4),
}

# For each item, find the old multi-size / single HTML and replace
import re

for item_en, new_html in replacements.items():
    # Find the old item block - it starts with <div class="menu-item ..." 
    # and contains the placeholder with this item's name
    # Pattern: find the menu-item div that contains this item's placeholder title
    
    # Build the old placeholder pattern
    placeholder_title = f"📸 ATM - Add image for {item_en}"
    
    # Find the start of the menu-item containing this placeholder
    # Find the placeholder first
    idx = html.find(placeholder_title)
    if idx == -1:
        print(f"❌ Could not find placeholder for {item_en}")
        continue
    
    # Find the opening <div class="menu-item ..." before this
    start = html.rfind('<div class="menu-item', 0, idx)
    if start == -1:
        print(f"❌ Could not find menu-item start for {item_en}")
        continue
    
    # Find the closing </div> of this menu-item
    # Count nested divs
    depth = 0
    end = start
    first_close = False
    for i in range(start, len(html)):
        if html[i:i+5] == '<div ' or html[i:i+11] == '<div class=':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                end = i + 6
                break
    
    old_block = html[start:end]
    
    # Replace old block with new
    html = html[:start] + new_html + html[end:]
    print(f"✅ Replaced {item_en}")

with open("/tmp/tom-yum-kung-menu/index.html", "w") as f:
    f.write(html)

print("\n🎉 All 12 items updated!")
