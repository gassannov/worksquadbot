import os
from PIL import Image
from telegram import Bot, InputSticker
from telegram.constants import StickerFormat
import asyncio

# Configuration
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
YOUR_USER_ID = 123456789  # Your Telegram user ID
EMOJI_PACK_NAME = "myemojis_by_YourBotName"  # Must end with _by_<bot_username>
EMOJI_PACK_TITLE = "My Custom Emojis"
INPUT_FOLDER = "source_images"
OUTPUT_FOLDER = "processed_emojis"

# Step 1: Process images to 100x100 PNG with transparency
def process_images(input_folder, output_folder):
    """Convert all images to 100x100 transparent PNG"""
    os.makedirs(output_folder, exist_ok=True)
    processed_files = []
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp')):
            input_path = os.path.join(input_folder, filename)
            output_filename = f"{os.path.splitext(filename)[0]}.png"
            output_path = os.path.join(output_folder, output_filename)
            
            try:
                # Open image
                img = Image.open(input_path)
                
                # Convert to RGBA for transparency support
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Resize to 100x100 (for emoji) or 512x512 (for stickers)
                # For emojis: use 100x100
                img_resized = img.resize((100, 100), Image.LANCZOS)
                
                # Save as PNG
                img_resized.save(output_path, 'PNG', optimize=True)
                processed_files.append(output_path)
                print(f"✓ Processed: {filename}")
                
            except Exception as e:
                print(f"✗ Error processing {filename}: {e}")
    
    return processed_files

# Step 2: Create emoji pack using Telegram Bot API
async def create_emoji_pack(bot_token, user_id, pack_name, pack_title, image_files):
    """Create a custom emoji pack programmatically"""
    bot = Bot(token=bot_token)
    
    # Prepare stickers list
    stickers = []
    
    for idx, image_path in enumerate(image_files):
        # Each emoji needs an associated emoji character
        # You can customize this - use different emojis for different images
        emoji = "😀"  # Default emoji, change as needed
        
        # Create InputSticker object
        with open(image_path, 'rb') as img_file:
            sticker = InputSticker(
                sticker=img_file,
                emoji_list=[emoji],
                format=StickerFormat.STATIC  # For PNG emojis
            )
            stickers.append(sticker)
    
    try:
        # Create the emoji pack
        result = await bot.create_new_sticker_set(
            user_id=user_id,
            name=pack_name,
            title=pack_title,
            stickers=stickers,
            sticker_type="custom_emoji"  # This makes it an emoji pack, not sticker pack
        )
        
        if result:
            emoji_link = f"https://t.me/addemoji/{pack_name}"
            print(f"\n✓ Emoji pack created successfully!")
            print(f"📦 Pack name: {pack_name}")
            print(f"🔗 Share link: {emoji_link}")
            return emoji_link
        else:
            print("✗ Failed to create emoji pack")
            return None
            
    except Exception as e:
        print(f"✗ Error creating emoji pack: {e}")
        return None

# Main automation function
async def main():
    print("🚀 Starting automated emoji pack creation...\n")
    
    # Step 1: Process images
    print("📸 Processing images...")
    processed_files = process_images(INPUT_FOLDER, OUTPUT_FOLDER)
    print(f"\n✓ Processed {len(processed_files)} images\n")
    
    if not processed_files:
        print("✗ No images to process!")
        return
    
    # Step 2: Create emoji pack
    print("📦 Creating emoji pack on Telegram...")
    await create_emoji_pack(
        bot_token=BOT_TOKEN,
        user_id=YOUR_USER_ID,
        pack_name=EMOJI_PACK_NAME,
        pack_title=EMOJI_PACK_TITLE,
        image_files=processed_files
    )

# Run the automation
if __name__ == "__main__":
    asyncio.run(main())