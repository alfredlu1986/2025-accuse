import os

IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.mp3')

def generate_gallery(root='.'):
    sections_html = []

    # 走訪 root 底下所有子資料夾（含多層）
    for dirpath, dirnames, filenames in os.walk(root):
        # 跳過 root 自己，只處理子資料夾
        if os.path.abspath(dirpath) == os.path.abspath(root):
            continue

        # 把資料夾裡的圖片挑出來
        imgs = sorted(
            [f for f in filenames if f.lower().endswith(IMAGE_EXTS)]
        )
        if not imgs:
            continue  # 沒圖就略過

        # 取得「相對路徑」當標題與 src
        rel_dir = os.path.relpath(dirpath, root)   # 例如：正常\中興高中補校 - 澳洲烏日長佑
        print(f"📁 {rel_dir}：{len(imgs)} 張圖片")

        img_tags = "\n      ".join(
            [f'<img src="{rel_dir}/{img}" alt="{rel_dir} - {img}">' for img in imgs]
        )

        section = f"""
  <section>
    <h2>{rel_dir}</h2>
    <div class="gallery">
      {img_tags}
    </div>
  </section>
"""
        sections_html.append(section)

    if not sections_html:
        print("⚠️ 沒找到任何圖片")
        return

    full_html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <title>2025-accuse 相簿</title>
  <style>
    body {{
      font-family: "Noto Sans TC", "Microsoft JhengHei", sans-serif;
      background-color: #f8f8f8;
      margin: 0;
      padding: 20px;
    }}
    h1 {{
      text-align: center;
      margin-bottom: 20px;
    }}
    h2 {{
      margin-top: 40px;
      margin-bottom: 10px;
      border-left: 4px solid #555;
      padding-left: 8px;
      word-break: break-all;
    }}
    .gallery {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 10px;
      max-width: 1200px;
      margin: 0 auto;
    }}
    .gallery img {{
      width: 100%;
      height: 220px;
      object-fit: cover;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.15);
      transition: transform 0.2s, box-shadow 0.2s;
      background: #ddd;
    }}
    .gallery img:hover {{
      transform: scale(1.03);
      box-shadow: 0 4px 10px rgba(0,0,0,0.25);
    }}
    footer {{
      text-align: center;
      margin-top: 40px;
      font-size: 0.9em;
      color: #777;
    }}
  </style>
</head>
<body>
  <h1>2025-accuse 圖片總覽</h1>
  {"".join(sections_html)}
  <footer>
    由 generate_gallery_recursive.py 自動產生
  </footer>
</body>
</html>
"""
    out = os.path.join(root, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"✅ 已產生 {out}")

if __name__ == "__main__":
    generate_gallery(".")
