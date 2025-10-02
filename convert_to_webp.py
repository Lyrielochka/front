from pathlib import Path
from PIL import Image

def convert_all(root: Path, quality: int = 80) -> int:
    exts = {'.png', '.jpg', '.jpeg'}
    converted = 0
    for path in root.rglob('*'):
        if path.suffix.lower() not in exts:
            continue
        target = path.with_suffix('.webp')
        if target.exists() and target.stat().st_mtime >= path.stat().st_mtime:
            continue
        try:
            with Image.open(path) as img:
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')
                img.save(target, 'WEBP', quality=quality, method=6)
                converted += 1
        except Exception as exc:
            print(f'Failed to convert {path}: {exc}')
    return converted

if __name__ == '__main__':
    count = convert_all(Path('.'))
    print(f'Converted {count} images to WebP')
