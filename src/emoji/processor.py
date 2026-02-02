"""Image processing and cropping utilities."""

import os
from PIL import Image
from typing import List, Tuple


class ImageProcessor:
    """Handles image cropping and emoji preparation."""

    def __init__(self, emoji_size: int = 100):
        """
        Initialize image processor.

        Args:
            emoji_size: Target size for each emoji in pixels
        """
        self.emoji_size = emoji_size

    def crop_to_grid(
        self,
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

                cropped_resized = cropped.resize(
                    (self.emoji_size, self.emoji_size),
                    Image.Resampling.LANCZOS
                )

                output_filename = f"emoji_{row}_{col}.png"
                output_path = os.path.join(output_folder, output_filename)

                cropped_resized.save(output_path, "PNG", optimize=True)
                cropped_files.append(output_path)

        img.close()
        return cropped_files

    def suggest_grid_sizes(self, width: int, height: int) -> List[Tuple[int, int]]:
        """
        Suggest grid sizes based on image aspect ratio.

        Args:
            width: Image width
            height: Image height

        Returns:
            List of suggested grid sizes
        """
        aspect_ratio = width / height

        target_counts = [21, 36, 56, 72]

        grid_sizes = []

        for target_count in target_counts:
            rows = round((target_count / aspect_ratio) ** 0.5)
            rows = max(2, rows)

            cols = round(target_count / rows)
            cols = max(2, cols)

            grid_aspect = cols / rows
            if abs(grid_aspect - aspect_ratio) > 0.4:
                cols = round(aspect_ratio * rows)
                cols = max(2, cols)

            grid_sizes.append((cols, rows))

        seen = set()
        unique_sizes = []
        for size in grid_sizes:
            if size not in seen:
                seen.add(size)
                unique_sizes.append(size)

        return unique_sizes[:5]

    def get_image_dimensions(self, path: str) -> Tuple[int, int]:
        """
        Get image dimensions.

        Args:
            path: Path to image

        Returns:
            Tuple of (width, height)
        """
        with Image.open(path) as img:
            return img.size
