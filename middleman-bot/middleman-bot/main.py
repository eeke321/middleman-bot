
# MORJES TÄSSÄ MUN MUUTOS
# LIT 

""

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter, CallbackContext, CallbackQueryHandler, CallbackContext
from enum import IntEnum

from lift import Lift, LiftState, load_lifts, add_lift

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import os
print(os.getcwd())

import openpyxl
wb = openpyxl.load_workbook('file.xlsx')


group_chat_id = "-415596535"

class ConversationState(IntEnum):
    NONE = 0
    PHOTO = 1
    SITE = 2
    OPENING = 3
    MESSAGE = 4
    PREVIEW = 5


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update : Update, context : CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update : Update, context : CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def test_print(update : Update, context : CallbackContext):
    print("Test Print:")
    print("message id: ", update.message.message_id)
    print("chat id: ", update.message.chat.id)
    print(context.user_data['state'])

def button(update : Update, context : CallbackContext):
    query = update.callback_query

# CallbackQueries need to be answered, even if no notification to the user is needed
# Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    query.edit_message_text(text="Selected option: {}".format(query.data))

def ready(context : CallbackContext):
    if (context.user_data['photo'] != None and
        context.user_data['state'] == ConversationState.PREVIEW):
        return True
    else:
        return False

def combine(context : CallbackContext):
    site = "Site: " + context.user_data['site']
    opening = "Opening: " + context.user_data['opening']
    message = "# " + context.user_data['message']

    combine = "New Lift: \n" + site + "\n" + opening + '\n' + message

    print("COMBINED")

    return combine

def reply_test(update : Update, context : CallbackContext):
    update.message.reply_text("Test!")

    photo = context.bot_data['photo']
    update.message.reply_photo(photo)

def reply_text(update : Update, context : CallbackContext):
    if (context.user_data['state'] == ConversationState.MESSAGE):
        update.message.reply_text("Nice message!")

        context.user_data['message'] = update.message.text
        context.user_data['state'] = ConversationState.PREVIEW
    
    if (ready(context) == True):
        photo = context.user_data['photo']
        update.message.reply_text("Preview:")
        update.message.reply_photo(photo, combine(context))

        keyboard = [[InlineKeyboardButton("Yes", callback_data = "Yes"),
                    InlineKeyboardButton("No", callback_data = "No")]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Create lift?', reply_markup=reply_markup)

        context.bot.send_photo(-415596535, photo, combine(context))

        context.user_data['photo'] = None
        context.user_data['site'] = None
        context.user_data['opening'] = None
        context.user_data['message'] = None

    else:
        update.message.reply_text("?")

    #keyboard = [[InlineKeyboardButton("Add", callback_data="Add"),
    #             InlineKeyboardButton("Skip", callback_data="Skip"),
    #             InlineKeyboardButton("Ready", callback_data="Ready")],

    #            [InlineKeyboardButton("Type", callback_data="Type")]]

    #reply_markup = InlineKeyboardMarkup(keyboard)
    #update.message.reply_text('Please choose:', reply_markup=reply_markup)

def reply_pic(update : Update, context : CallbackContext):
    context.user_data['photo'] = update.message.photo[-1]
    update.message.reply_text("Nice photo!")

    context.user_data['site'] = None
    context.user_data['opening'] = None

    context.user_data['state'] = ConversationState.SITE


def reply_site(update : Update, context : CallbackContext):
    context.user_data['site'] = update.message.text
    context.user_data['site_set'] = True

    update.message.reply_text("Nice site!")

    context.user_data['state'] = ConversationState.OPENING

    #if (ready(context) == True):
    #    update.message.reply_text(combine(context))

def reply_opening(update : Update, context : CallbackContext):
    context.user_data['opening'] = update.message.text
    context.user_data['opening_set'] = True

    update.message.reply_text("Nice opening!")

    context.user_data['state'] = ConversationState.MESSAGE



def main():
    
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1182411075:AAGsO0gh6609YJTeGa09CBRAZePXm6m5Ivo", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))


    lift_list = []
    load_lifts(lift_list)

    test_lift = Lift(0, 'https://telegram.org/img/t_logo.png', LiftState.NONE, "S", "O", "Note")
    #add_lift(test_lift)


    print(wb.sheetnames)

    site_code_sheet = wb['sites']
    opening_code_sheet = wb['openings']

    i = 0
    sites = []
    openings = []

    """Initialize"""

    # Todo: Multiple loops
    while True:
        i += 1
        # Get value from sheet cell
        site_code = site_code_sheet.cell(row = i, column = 1).value
        opening_code = opening_code_sheet.cell(row = i, column = 1).value

        # If all cells empty
        if (site_code == None and opening_code == None):
            break

        # Add value to list
        if (site_code != None):
            sites.append(site_code)
        if (opening_code != None):
            openings.append(opening_code)


    print(sites)
    print(openings)

    
    dp.bot_data['photo'] = test_lift.photo
    dp.bot_data['site'] = "TEST"
    dp.add_handler(MessageHandler(Filters.text("Test"), reply_test))


    dp.add_handler(MessageHandler(Filters.photo, reply_pic))
    dp.add_handler(MessageHandler(Filters.text(sites), reply_site))
    dp.add_handler(MessageHandler(Filters.text(openings), reply_opening))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, reply_text))

    dp.add_handler(CallbackQueryHandler(button))


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



if __name__ == '__main__':
    main()
