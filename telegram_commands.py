import csv
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes, \
    CallbackQueryHandler

with open("tokens.gitignore") as f:
    text = f.readlines()
    # Configuration for Telegram
    TOKEN = text[0].strip()  # BOT API TOKEN

# States for conversation handler
ID, LOCATION, URL, CONFIRMATION = range(4)

# To store user inputs temporarily
user_data = {}


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Please type /add_device to add a new device.")


# /add_device command handler
async def add_device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter the device ID (e.g., AB291):")
    return ID


# Handle the device ID
async def handle_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['id'] = update.message.text
    await update.message.reply_text("Now enter the location (e.g., Troia):")
    return LOCATION


# Handle the location
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['location'] = update.message.text
    await update.message.reply_text("Now enter the URL (e.g., https://console.geodnet.com/map?mount=AB291):")
    return URL


# Handle the URL
async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['url'] = update.message.text

    # Show collected information and ask for confirmation with inline keyboard
    confirmation_keyboard = [
        [InlineKeyboardButton("✅ Confirm", callback_data='confirm')],
        [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(confirmation_keyboard)

    await update.message.reply_text(
        f"Please confirm the details:\n\n"
        f"ID: {user_data['id']}\n"
        f"Location: {user_data['location']}\n"
        f"URL: {user_data['url']}\n\n",
        reply_markup=reply_markup
    )
    return CONFIRMATION


# Handle the confirmation callback
async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    if query.data == 'confirm':
        # Save to CSV if confirmed
        save_to_csv(user_data['id'], user_data['location'], user_data['url'])
        await query.edit_message_text("Device added successfully and stored in DEVICES.csv.")
    elif query.data == 'cancel':
        await query.edit_message_text("Operation cancelled.")

    return ConversationHandler.END


# Save data to CSV
def save_to_csv(device_id, location, url):
    with open('DEVICES.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([device_id, location, url])


# Handle the cancellation of the conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END


# Start the bot
def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Define the conversation handler with states and callbacks
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_device', add_device)],
        states={
            ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_id)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_location)],
            URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url)],
            CONFIRMATION: [CallbackQueryHandler(handle_confirmation)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == '__main__':
    main()
