import json, os, time, subprocess, sys

TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")
if not TOKEN:
    print("❌ No REPLICATE_API_TOKEN")
    sys.exit(1)

AUTH = "Bearer " + TOKEN
API = "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions"

ITEMS = [
    ("red-mojito", "Red Mojito Juice", "Fresh red mojito mocktail drink in a tall glass, vibrant red liquid, fresh mint leaves, lime slices, ice cubes, condensation on glass, dark background, professional beverage photography, 8k"),
    ("lemon-mint", "Lemon with Mint", "Fresh lemonade with mint drink in a tall glass, pale yellow-green liquid, mint sprigs, lemon slices, ice cubes, condensation, dark background, professional beverage photography"),
    ("orange-juice", "Orange Juice", "Fresh orange juice in a tall glass, vibrant orange color, orange slices on rim, pulp visible, condensation on glass, dark background, professional beverage photography, 8k"),
    ("saudi-champagne", "Saudi Champagne", "Sparkling Saudi champagne non-alcoholic drink in a champagne flute, golden bubbly liquid, apple juice base, sparkling, condensation, dark elegant background, professional beverage photography"),
    ("tea", "Tea", "Hot cup of tea, amber-brown liquid, steam rising, tea bag string hanging, ceramic cup on dark surface, warm lighting, professional beverage photography"),
    ("thai-hot-tea-lemon", "Thai Hot Tea with Lemon", "Thai hot tea in a glass cup, deep orange-amber color, lemon slice on rim, steam rising, warm lighting, dark background, professional beverage photography"),
    ("thai-ice-tea-lemon", "Thai Ice Tea with Lemon", "Thai iced tea in a tall glass, bright orange color, lemon wedge, ice cubes, condensation, dark background, professional beverage photography, 8k"),
    ("thai-ice-tea-milk", "Thai Ice Tea with Milk", "Thai iced tea with milk in a tall glass, creamy orange-brown color, swirling cream, ice cubes, dark background, professional beverage photography"),
    ("water", "Water", "Clean drinking water in a clear glass, transparent, ice cubes, bubbles, fresh and pure, dark background, minimal, professional beverage photography"),
    ("mineral-water", "Mineral Water", "Premium mineral water bottle, clear glass bottle with blue label, water droplets, cold fresh look, dark background, professional product photography"),
    ("pepsi", "Pepsi", "Pepsi cola in a glass with ice, dark cola liquid, caramel color, bubbles, condensation, dark background, professional beverage photography"),
    ("coca-cola", "Coca-Cola", "Coca-Cola in a glass with ice, dark cola liquid, bubbles, condensation, red accents, dark background, professional beverage photography"),
]

def gen_image(key, label, prompt):
    out = f"/tmp/tom-yum-kung-menu/juice-{key}.jpg"
    if os.path.exists(out) and os.path.getsize(out) > 2000:
        print(f"  ⏭️ {label} — already exists, skipping")
        return True
    
    payload = json.dumps({
        "input": {
            "prompt": prompt,
            "num_outputs": 1,
            "aspect_ratio": "1:1",
            "output_format": "jpg",
            "quality": 85
        }
    })
    
    # Submit
    cmd = ["curl", "-s", "-X", "POST", API,
           "-H", f"Authorization: {AUTH}",
           "-H", "Content-Type: application/json",
           "-d", payload]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    data = json.loads(r.stdout.strip())
    pid = data.get("id")
    if not pid:
        print(f"  ❌ {label} — submit failed: {str(data)[:200]}")
        return False
    
    # Poll
    for attempt in range(30):
        time.sleep(4)
        poll_cmd = ["curl", "-s", f"https://api.replicate.com/v1/predictions/{pid}",
                    "-H", f"Authorization: {AUTH}"]
        pr = subprocess.run(poll_cmd, capture_output=True, text=True, timeout=30)
        sd = json.loads(pr.stdout.strip())
        status = sd.get("status")
        if status == "succeeded":
            url = sd["output"]
            if isinstance(url, list):
                url = url[0]
            subprocess.run(["curl", "-sL", url, "-o", out], timeout=60)
            sz = os.path.getsize(out) if os.path.exists(out) else 0
            print(f"  ✅ {label} — {sz/1024:.0f}KB")
            return True
        elif status in ("failed", "canceled"):
            print(f"  ❌ {label} — {status}")
            return False
        elif attempt % 5 == 0:
            print(f"  ⏳ {label} — {status or 'processing'} ({attempt+1}s)")
    
    print(f"  ⏰ {label} — timed out")
    return False

print("🍹 Generating juice images...")
success = 0
for i, (key, label, prompt) in enumerate(ITEMS):
    print(f"[{i+1}/{len(ITEMS)}] {label}")
    if gen_image(key, label, prompt):
        success += 1
    time.sleep(1)

print(f"\n{'='*40}")
print(f"Done: {success}/{len(ITEMS)} images generated")
