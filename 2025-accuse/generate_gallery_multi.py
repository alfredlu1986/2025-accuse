import os

# 支援的圖片副檔名
IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.mp3')

def generate_gallery(root='.'):
    # 取得所有子資料夾（略過 . 開頭的）
    folders = [
        d for d in os.listdir(root)
        if os.path.isdir(os.path.join(root, d)) and not d.startswith('.')
    ]

    # 如果你有一些「空資料夾」或暫時不用的，可以在這裡排除
    exclude = {'新增資料夾'}  # 例如：暫時不要顯示這個
    folders = [f for f in folders if f not in exclude]

    sections_html = []

    for folder in sorted(folders):
        folder_path = os.path.join(root, folder)
        files = sorted([
            f for f in os.listdir(folder_path)
            if f.lower().endswith(IMAGE_EXTS)
        ])

        if not files:
            # 沒有圖片就跳過
            continue

        print(f"📁 {folder}：找到 {len(files)} 張圖片")

        img_tags = "\n      ".join(
            [f'<img src="{folder}/{f}" alt="{folder} - {f}">' for f in files]
        )

        section = f"""
  <section>
    <h2>{folder}</h2>
    <div class="gallery">
      {img_tags}
    </div>
  </section>
"""
        sections_html.append(section)

    if not sections_html:
        print("⚠️ 沒找到任何圖片，請確認資料夾內有 .jpg/.png 等圖檔。")
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
    產生時間：手動執行 generate_gallery_multi.py
  </footer>
</body>
</html>
"""

    output_file = os.path.join(root, "index.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"✅ 已產生 {output_file}")

if __name__ == "__main__":
    # 預設掃描目前資料夾
    generate_gallery(".")
