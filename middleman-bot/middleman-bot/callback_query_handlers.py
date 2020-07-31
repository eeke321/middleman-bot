from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler, CallbackContext, ConversationHandler
from pathlib import Path

from enums import BCD
from lift import Lift, LiftState, add_lift, modify_lift_state
from message_handlers import ConversationState, combine


def preview_button(update : Update, context : CallbackContext):
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

        query.edit_message_text(text="Canceled")


    return ConversationHandler.END
    
 

def state_edit_button(update : Update, context : CallbackContext):
    query = update.callback_query
    query.answer()

    if(query.data == BCD.REPLY_LIFT_UPDATE_STATE.name):

        keyboard = [[InlineKeyboardButton("Missing", callback_data = BCD.LIFT_STATE_MISSING.name),
                    InlineKeyboardButton("Other", callback_data = BCD.LIFT_STATE_READY.name)],

                    [InlineKeyboardButton("Warehouse", callback_data = BCD.LIFT_STATE_WAREHOUSE.name)],
                    [InlineKeyboardButton("Shore", callback_data = BCD.LIFT_STATE_SHORE.name)],
                    [InlineKeyboardButton("Opening", callback_data = BCD.LIFT_STATE_OPENING.name)],
                    [InlineKeyboardButton("Site", callback_data = BCD.LIFT_STATE_SITE.name)]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=reply_markup)

    if(query.data == BCD.LIFT_STATE_WAREHOUSE.name):
        st_id = context.user_data['st']

        modify_lift_state(LiftState.WAREHOUSE, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + st_id + ": State update: " + LiftState.WAREHOUSE.name

        context.bot.send_photo(chat_id = -415596535, photo = photo, caption = caption)
        query.edit_message_text(text="Edited state")

        return ConversationHandler.END

    if(query.data == BCD.LIFT_STATE_SHORE.name):
        st_id = context.user_data['st']

        modify_lift_state(LiftState.SHORE, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + st_id + ": State update: " + LiftState.SHORE.name

        context.bot.send_photo(chat_id = -415596535, photo = photo, caption = caption)
        query.edit_message_text(text="Edited state")

        return ConversationHandler.END

    if(query.data == BCD.LIFT_STATE_OPENING.name):
        st_id = context.user_data['st']

        modify_lift_state(LiftState.OPENING, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + st_id + ": State update: " + LiftState.OPENING.name

        context.bot.send_photo(chat_id = -415596535, photo = photo, caption = caption)
        query.edit_message_text(text="Edited state")

        return ConversationHandler.END

    if(query.data == BCD.LIFT_STATE_SITE.name):
        st_id = context.user_data['st']

        modify_lift_state(LiftState.SITE, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + st_id + ": State update: " + LiftState.SITE.name

        context.bot.send_photo(chat_id = -415596535, photo = photo, caption = caption)
        query.edit_message_text(text="Edited state")

        return ConversationHandler.END

    return ConversationState.EDIT_SHIPMENT

