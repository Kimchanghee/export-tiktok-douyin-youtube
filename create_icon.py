"""
Create a simple icon for the video downloader
"""

try:
    from PIL import Image, ImageDraw

    # Create 256x256 icon
    size = 256
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Background circle (gradient effect with green)
    colors = ['#4CAF50', '#45a049', '#3d8b40']
    for i, color in enumerate(colors):
        margin = i * 15
        draw.ellipse([margin, margin, size-margin, size-margin], fill=color)

    # Draw play icon (triangle)
    triangle_color = 'white'
    margin = 70
    points = [
        (margin + 20, margin),
        (margin + 20, size - margin),
        (size - margin - 20, size // 2)
    ]
    draw.polygon(points, fill=triangle_color)

    # Draw download arrow overlay
    arrow_color = '#2E7D32'
    center_x = size - 60
    center_y = size - 60
    arrow_size = 40

    # Arrow circle background
    draw.ellipse(
        [center_x - arrow_size, center_y - arrow_size,
         center_x + arrow_size, center_y + arrow_size],
        fill='white'
    )

    # Arrow pointing down
    arrow_width = 8
    arrow_points = [
        (center_x - arrow_width, center_y - 15),
        (center_x + arrow_width, center_y - 15),
        (center_x + arrow_width, center_y + 5),
        (center_x + 15, center_y + 5),
        (center_x, center_y + 20),
        (center_x - 15, center_y + 5),
        (center_x - arrow_width, center_y + 5),
    ]
    draw.polygon(arrow_points, fill=arrow_color)

    # Save as PNG first
    img.save('icon.png', 'PNG')
    print("OK: Icon created - icon.png")

    # Try to create ICO file
    try:
        # Create multiple sizes for ICO
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        icons = []
        for icon_size in sizes:
            icons.append(img.resize(icon_size, Image.Resampling.LANCZOS))

        icons[0].save('icon.ico', format='ICO', sizes=[(s[0], s[1]) for s in sizes])
        print("OK: ICO file created - icon.ico")
    except Exception as e:
        print(f"SKIP: ICO creation - {e}")
        print("INFO: PNG icon will be used instead")

except ImportError:
    print("WARNING: Pillow not installed")
    print("INFO: Install with - pip install Pillow")
    print("INFO: Icon creation skipped")

except Exception as e:
    print(f"ERROR: {e}")
