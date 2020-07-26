
# MORJES TÄSSÄ MUN MUUTOS
#Let's see if this works
# LIT 

""" TODO """

""" _________ || Main || _________ """
""" - File organisation """

""" _________ || Add || _________ """
""" - Lift state updating  """
""" - Add per user signaling and linking """
""" - Recognize nicnames for sites & openings """
""" - Lift folders for data and photos """
""" - Conversation state shortcuts and notes """
""" - Callback keyboards """
""" - User choice feedback """
""" - User creation and setup """

""" _________ || Update || _________ """

""" _________ || Code fix || _________ """
""" - Better var names """
""" - Better state names """

""" _________ || Optimaze || _________ """
""" - Workbook as argument """

""" _________ || Polish || _________ """
""" - User friendly conversation quide """

""" _________ || BUGS || _________ """
""" - nah """


import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter, CallbackContext, CallbackQueryHandler, CallbackContext
from pathlib import Path

from lift import Lift, LiftState, load_lifts, add_lift
from message_handlers import reply_test, reply_text, reply_photo, reply_site, reply_opening, combine
from message_handlers import ConversationState

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import os
print(os.getcwd())

import openpyxl
wb = openpyxl.load_workbook('file.xlsx')


group_chat_id = "-415596535"




def test_print(update : Update, context : CallbackContext):
    print("Test Print:")
    print("message id: ", update.message.message_id)
    print("chat id: ", update.message.chat.id)
    print(context.user_data['conv_state'])

def button(update : Update, context : CallbackContext):
    query = update.callback_query

# CallbackQueries need to be answered, even if no notification to the user is needed
# Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if (query.data == "send_lift"):
        add_lift(Lift(context.user_data['lift'].id,
            context.user_data['lift'].photo, 
            LiftState.NONE, 
            context.user_data['lift'].site, 
            context.user_data['lift'].opening,
            context.user_data['lift']).note)

        context.bot.send_photo(-415596535, context.user_data['lift'].photo, combine(context))

        context.user_data['lift'].clear()
        
        context.user_data['conv_state'] = ConversationState.PHOTO


    elif(query.data == "cancel_lift"):
        context.user_data['lift'].clear()

        context.user_data['conv_state'] = ConversationState.PHOTO

    query.edit_message_text(text="Selected option: {}".format(query.data))


    




def main():
    
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1182411075:AAGsO0gh6609YJTeGa09CBRAZePXm6m5Ivo", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher


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

    #TEMP
    last_id = lift_list[-1].id

    dp.bot_data['last_id'] = last_id

    dp.add_handler(MessageHandler(Filters.text("Test"), reply_test))

    dp.add_handler(MessageHandler(Filters.photo, reply_photo))
    dp.add_handler(MessageHandler(Filters.text(sites), reply_site))
    dp.add_handler(MessageHandler(Filters.text(openings), reply_opening))

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
