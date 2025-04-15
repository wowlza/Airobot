from PIL import Image, ImageDraw, ImageFont
import os
import shutil

def add_text_to_images(image_dir, text_dict, output_dir, font_path="arial.ttf", font_size=20, text_position=None):
    """
    Copy all images to the output directory and add specified text to those images that have corresponding text in the dictionary.
    :param image_dir: Directory containing the images.
    :param text_dict: Dictionary mapping image frame IDs to text.
    :param output_dir: Directory where modified images will be saved.
    :param font_path: Path to the font file.
    :param font_size: Font size of the text.
    :param text_position: Tuple (x, y) representing the position of the text.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font path is incorrect. Falling back to default font.")
        font = ImageFont.load_default()

    # Iterate over all files in the input directory
    for filename in os.listdir(image_dir):
        if filename.endswith(".jpeg"):  # Ensure we are processing .jpeg files
            frame_id = int(filename.split('.')[0])  # Extract frame ID from filename
            image_path = os.path.join(image_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # Open the image
            image = Image.open(image_path)
            if frame_id in text_dict:
                draw = ImageDraw.Draw(image)

                # If text position is not provided, place text at the bottom center
                if text_position is None:
                    text = text_dict[frame_id]
                    text_width, text_height = draw.textsize(text, font=font)
                    x = 0#(image.width - text_width) / 2
                    y = image.height - text_height - 10  # 10 pixels from the bottom
                    text_position = (x, y)

                # Add text to image
                draw.text(text_position, text_dict[frame_id], font=font, fill="white")

            # Save or overwrite the image in the output directory
            image.save(output_path)

# Example usage
image_directory = 'output/images/dir/40cc5749c7d59c06_5c97/video'
output_directory = 'output/new_images'
texts_to_add = {
    0: "what can I help you with?",
    1: "what can I help you with?",
    2: "I'd like my plant watered",
    3: "I'd like my plant watered",
    4: "The plant needs to be watered. ",
    5: "The plant needs to be watered. ",
    6: "Bring some water in a container from the sink and pour into the plant.",
    7: "Bring some water in a container from the sink and pour into the plant.",
}

add_text_to_images(image_directory, texts_to_add, output_directory, font_path="/usr/share/fonts/truetype/msttcorefonts/arial.ttf", font_size=50)
