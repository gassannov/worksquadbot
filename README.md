# САМЫЙ ЛУЧШИЙ БОТ В ИСТОРИИ ТЕЛЕГРАМА
by
- tima
- vanya
- maratik
- qrutomitya
- rassel
- mishanya

## Emoji Image Cropper Bot

Telegram bot that automatically crops images into custom emoji packs.

### Features

- Upload any image
- Automatically suggests grid sizes based on image aspect ratio
- Choose custom grid size (2x2, 3x3, 4x4, etc.)
- Adjustable padding between emoji pieces
- Automatic emoji pack creation
- Get shareable link instantly

### Quick Start

1. Copy environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your bot token from [@BotFather](https://t.me/BotFather):
```
BOT_TOKEN=your_bot_token_here
```

3. Run with Docker Compose:
```bash
docker-compose up -d
```

### Usage

1. Start bot with `/start`
2. Send any image
3. Choose grid size (how many parts to cut)
4. Choose padding (spacing between emoji pieces)
5. Get your emoji pack link!

### Development

Run locally without Docker:
```bash
pip install -r requirements.txt
python main.py
```

### Project Structure

```
src/
├── bot/
│   ├── handlers.py    # Bot command and callback handlers
│   └── keyboards.py   # Inline keyboard builders
├── emoji/
│   ├── processor.py   # Image cropping and processing
│   └── sticker.py     # Sticker pack creation
└── config/
    ├── settings.py    # Application configuration
    └── strings.py     # Bot messages and text
main.py               # Entry point
```