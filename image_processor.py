"""Image processing and cropping utilities."""

import os
from PIL import Image
from typing import List, Tuple


def crop_image_to_emojis(
    input_path: str,
    output_folder: str,
    grid_size: Tuple[int, int],
    padding: int
) -> List[str]:
    """
    Crop image into NxM grid with padding.

    Args:
        input_path: Path to input image
        output_folder: Folder to save cropped images
        grid_size: Tuple of (columns, rows)
        padding: Padding value (1-5)

    Returns:
        List of paths to cropped images
    """
    os.makedirs(output_folder, exist_ok=True)

    img = Image.open(input_path)

    if img.mode != "RGBA":
        img = img.convert("RGBA")

    cols, rows = grid_size
    img_width, img_height = img.size

    cell_width = img_width // cols
    cell_height = img_height // rows

    padding_pixels = padding * 2

    cropped_files = []

    for row in range(rows):
        for col in range(cols):
            left = col * cell_width + padding_pixels
            top = row * cell_height + padding_pixels
            right = (col + 1) * cell_width - padding_pixels
            bottom = (row + 1) * cell_height - padding_pixels

            left = max(0, left)
            top = max(0, top)
            right = min(img_width, right)
            bottom = min(img_height, bottom)

            cropped = img.crop((left, top, right, bottom))

            emoji_size = 100
            cropped_resized = cropped.resize(
                (emoji_size, emoji_size),
                Image.Resampling.LANCZOS
            )

            output_filename = f"emoji_{row}_{col}.png"
            output_path = os.path.join(output_folder, output_filename)

            cropped_resized.save(output_path, "PNG", optimize=True)
            cropped_files.append(output_path)

    return cropped_files


def suggest_grid_size(width: int, height: int) -> List[Tuple[int, int]]:
    """
    Suggest grid sizes based on image aspect ratio.

    Args:
        width: Image width
        height: Image height

    Returns:
        List of suggested grid sizes
    """
    aspect_ratio = width / height

    if aspect_ratio > 1.3:
        return [(4, 3), (3, 2), (4, 4), (3, 3)]
    elif aspect_ratio < 0.7:
        return [(3, 4), (2, 3), (3, 3), (4, 4)]
    else:
        return [(3, 3), (4, 4), (2, 2), (5, 5)]
