from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler, CallbackContext, ConversationHandler
from enums import BCD
from lift import Lift, LiftState, add_lift
from message_handlers import ConversationState, combine


def button(update : Update, context : CallbackContext):
    query = update.callback_query

# CallbackQueries need to be answered, even if no notification to the user is needed
# Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if (query.data == BCD.REPLY_SEND_LIFT.name):
        add_lift(Lift(context.user_data['lift'].id,
            context.user_data['lift'].photo, 
            LiftState.NONE, 
            context.user_data['lift'].site, 
            context.user_data['lift'].opening,
            context.user_data['lift']).note)

        context.bot.send_photo(-415596535, context.user_data['lift'].photo, combine(context))

        context.user_data['lift'].clear()
        
        context.user_data['conv_state'] = ConversationState.PHOTO

        query.edit_message_text(text="Send to group")


    elif(query.data == BCD.REPLY_CANCEL_LIFT.name):
        context.user_data['lift'].clear()

        context.user_data['conv_state'] = ConversationState.PHOTO

        query.edit_message_text(text="Cancelled")
    
    elif(query.data == BCD.REPLY_LIFT_UPDATE_STATE.name):

        keyboard = [[InlineKeyboardButton("Shore", callback_data = BCD.LIFT_STATE_SHORE.name),
                    InlineKeyboardButton("Opening", callback_data = BCD.LIFT_STATE_OPENING.name),
                    InlineKeyboardButton("Site", callback_data = BCD.LIFT_STATE_SITE.name),
                    InlineKeyboardButton("Missing", callback_data = BCD.LIFT_STATE_MISSING.name),
                    InlineKeyboardButton("Other", callback_data = BCD.LIFT_STATE_READY.name)]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=reply_markup)
    
    #query.edit_message_text(text="Selected option: {}".format(query.data))
