from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackContext, ConversationHandler
from pathlib import Path

from enums import BCD, UD
from lift import Lift, LiftState, add_lift, modify_lift_state
from message_handlers import ConversationState, combine


def preview_button(update : Update, context : CallbackContext):
    query = update.callback_query

# CallbackQueries need to be answered, even if no notification to the user is needed
# Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if (query.data == BCD.REPLY_SEND_LIFT.name):
        add_lift(Lift(context.user_data[UD.NEW_LIFT].id,
            context.user_data[UD.NEW_LIFT].photo, 
            LiftState.NONE, 
            context.user_data[UD.NEW_LIFT].site, 
            context.user_data[UD.NEW_LIFT].opening,
            context.user_data[UD.NEW_LIFT]).note)

        context.bot.send_photo(-415596535, context.user_data[UD.NEW_LIFT].photo, combine(context))

        context.user_data[UD.NEW_LIFT].clear()

        query.edit_message_text(text="Send to group")


    elif(query.data == BCD.REPLY_CANCEL_LIFT.name):
        context.user_data[UD.NEW_LIFT].clear()

        query.edit_message_text(text="Canceled")


    return ConversationHandler.END
    
 

def state_edit_button(update : Update, context : CallbackContext):
    query = update.callback_query
    query.answer()


    """ State Update """

    if(query.data == BCD.REPLY_LIFT_UPDATE_STATE.name):

        keyboard = [[InlineKeyboardButton("Missing", callback_data = BCD.LIFT_STATE_MISSING.name),
                    InlineKeyboardButton("Other", callback_data = BCD.LIFT_STATE_READY.name)],

                    [InlineKeyboardButton("Warehouse", callback_data = BCD.LIFT_STATE_WAREHOUSE.name)],
                    [InlineKeyboardButton("Shore", callback_data = BCD.LIFT_STATE_SHORE.name)],
                    [InlineKeyboardButton("Opening", callback_data = BCD.LIFT_STATE_OPENING.name)],
                    [InlineKeyboardButton("Site", callback_data = BCD.LIFT_STATE_SITE.name)],
                    [InlineKeyboardButton("Ready", callback_data = BCD.LIFT_STATE_READY.name)]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=reply_markup)

        return ConversationState.EDIT_SHIPMENT

    if(query.data == BCD.LIFT_STATE_WAREHOUSE.name):
        st_id = context.user_data[UD.SHIPMENT_ID]

        modify_lift_state(LiftState.WAREHOUSE, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + str(st_id) + ": State update: " + LiftState.WAREHOUSE.name

        context.bot.send_photo(chat_id = -415596535, photo = photo, caption = caption)
        query.edit_message_text(text="Edited state")

        return ConversationHandler.END

    if(query.data == BCD.LIFT_STATE_SHORE.name):
        st_id = context.user_data[UD.SHIPMENT_ID]

        modify_lift_state(LiftState.SHORE, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + str(st_id) + ": State update: " + LiftState.SHORE.name

        context.bot.send_photo(chat_id = -415596535, photo = photo, caption = caption)
        query.edit_message_text(text="Edited state")

        return ConversationHandler.END

    if(query.data == BCD.LIFT_STATE_OPENING.name):
        st_id = context.user_data[UD.SHIPMENT_ID]

        modify_lift_state(LiftState.OPENING, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + str(st_id) + ": State update: " + LiftState.OPENING.name

        context.bot.send_photo(chat_id = -415596535, photo = photo, caption = caption)
        query.edit_message_text(text="Edited state")

        return ConversationHandler.END

    if(query.data == BCD.LIFT_STATE_SITE.name):
        st_id = context.user_data[UD.SHIPMENT_ID]

        modify_lift_state(LiftState.SITE, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + str(st_id) + ": State update: " + LiftState.SITE.name

        context.bot.send_photo(chat_id = -415596535, photo = photo, caption = caption)

        query.edit_message_text(text="Edited state")

        return ConversationHandler.END

    if(query.data == BCD.LIFT_STATE_READY.name):
        st_id = context.user_data[UD.SHIPMENT_ID]

        modify_lift_state(LiftState.READY, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + str(st_id) + ": State update: " + LiftState.READY.name

        context.bot.send_photo(chat_id = 846031989, photo = photo, caption = caption)

        query.edit_message_text(text="Info send to linked users")

        return ConversationHandler.END

    """ Link """

    if(query.data == BCD.REPLT_LIFT_ADD_LINKS.name):
        query.edit_message_text("Who to link?")

        return ConversationState.EDIT_SHIPMENT_LINK

    return ConversationHandler.END

