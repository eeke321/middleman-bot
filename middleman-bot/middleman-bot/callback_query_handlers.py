from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackContext, ConversationHandler
from pathlib import Path

from enums import BCD, UD, BD
from lift import Lift, LiftState, add_lift, modify_lift_state, modify_lift_users
from message_handlers import ConversationState, combine
import copy

def ping_button(update : Update, context : CallbackContext):
    query = update.callback_query
    query.answer()



    return ConversationHandler.END


def preview_button(update : Update, context : CallbackContext):
    query = update.callback_query


    query.answer()

    new_lift = Lift(
        id = context.user_data[UD.NEW_LIFT].id,
        from_user = context.user_data[UD.NEW_LIFT].from_user,
        photo = context.user_data[UD.NEW_LIFT].photo, 
        state = LiftState.NONE, 
        site = context.user_data[UD.NEW_LIFT].site, 
        opening = context.user_data[UD.NEW_LIFT].opening,
        note = context.user_data[UD.NEW_LIFT].note)

    if (query.data == BCD.REPLY_SEND_LIFT.name):
        add_lift(new_lift)

        context.bot_data[BD.LIFT_LIST].append(new_lift)

        keyboard = [[InlineKeyboardButton("Follow " + u'\U0001F91D', callback_data = BCD.FOLLOW_SITE_YES.name)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_photo(-1001123729341, context.user_data[UD.NEW_LIFT].photo, combine(context), reply_markup = reply_markup)

        context.bot_data[BD.LIFT_LIST].append(new_lift)

        context.user_data[UD.NEW_LIFT].clear()

        query.edit_message_text(text="Send to group " + u'\U0001F91D')


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

                    [InlineKeyboardButton("[ Warehouse ]", callback_data = BCD.LIFT_STATE_WAREHOUSE.name)],
                    [InlineKeyboardButton("[ Shore ]", callback_data = BCD.LIFT_STATE_SHORE.name)],
                    [InlineKeyboardButton("[ Opening ]", callback_data = BCD.LIFT_STATE_OPENING.name)],
                    [InlineKeyboardButton("[ Site ]", callback_data = BCD.LIFT_STATE_SITE.name)],
                    [InlineKeyboardButton("Ping!", callback_data = BCD.LIFT_STATE_READY.name)]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=reply_markup)

        return ConversationState.EDIT_SHIPMENT

    if(query.data == BCD.LIFT_STATE_WAREHOUSE.name):
        st_id = context.user_data[UD.SHIPMENT_ID]

        modify_lift_state(LiftState.WAREHOUSE, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + str(st_id) + ": State update: " + LiftState.WAREHOUSE.name

        context.bot.send_photo(chat_id = -1001454113278, photo = photo, caption = caption)
        query.edit_message_text(text="Edited state")

        return ConversationHandler.END

    if(query.data == BCD.LIFT_STATE_SHORE.name):
        st_id = context.user_data[UD.SHIPMENT_ID]

        modify_lift_state(LiftState.SHORE, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + str(st_id) + ": State update: " + LiftState.SHORE.name


        context.bot.send_photo(chat_id = -1001123729341, photo = photo, caption = caption)
        query.edit_message_text(text="Edited state")

        return ConversationHandler.END

    if(query.data == BCD.LIFT_STATE_OPENING.name):
        st_id = context.user_data[UD.SHIPMENT_ID]

        modify_lift_state(LiftState.OPENING, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + str(st_id) + ": State update: " + LiftState.OPENING.name

        context.bot.send_photo(chat_id = -1001123729341, photo = photo, caption = caption)
        query.edit_message_text(text="Edited state")

        return ConversationHandler.END

    if(query.data == BCD.LIFT_STATE_SITE.name):
        st_id = context.user_data[UD.SHIPMENT_ID]

        modify_lift_state(LiftState.SITE, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + str(st_id) + ": State update: " + LiftState.SITE.name

        context.bot.send_photo(chat_id = -1001123729341, photo = photo, caption = caption)

        query.edit_message_text(text="Edited state")

        return ConversationHandler.END

    if(query.data == BCD.LIFT_STATE_READY.name):
        st_id = context.user_data[UD.SHIPMENT_ID]

        modify_lift_state(LiftState.READY, st_id)

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')


        caption = "Shipment " + str(st_id) + ": State update: " + LiftState.READY.name
        
        for x, y in context.bot_data[BD.USER_DICT].items():
            print("Ping! to: " + x + " : " + str(y))

            context.bot.send_photo(chat_id = y, photo = photo, caption = caption)
            photo.seek(0)

        #context.bot.send_photo(chat_id = 846031989, photo
        # = photo, caption = caption)

        #photo.seek(0)

        #context.bot.send_photo(chat_id = 1156192071, photo = photo, caption = caption)

        query.edit_message_text(text="Info send to linked users")

        return ConversationHandler.END

    """ Link """

    if(query.data == BCD.REPLY_LIFT_ADD_LINKS.name):
        query.edit_message_text("Add users:")

        item_id = context.user_data[UD.SHIPMENT_ID] + 1

        lift = context.bot_data[BD.LIFT_LIST][item_id]
        lift.users.clear()

        return ConversationState.EDIT_SHIPMENT_LINK

    if(query.data == BCD.REPLY_USER_END_LINK.name):
        query.edit_message_text("Linking ended")

        st_id = context.user_data[UD.SHIPMENT_ID]
        
        users = context.bot_data[BD.LIFT_LIST][st_id + 1].users

        modify_lift_users(users, st_id)

        return ConversationHandler.END

    """ Ping """

    if(query.data == BCD.REPLY_LIFT_PING.name):
        print("Ping!")

        st_id = context.user_data[UD.SHIPMENT_ID]

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        caption = "Shipment " + str(st_id) + ": Ping!"

        context.bot.send_photo(chat_id = -1001454113278, photo = photo, caption = caption)

        lift_id = st_id + 1
        site = context.bot_data[BD.LIFT_LIST][lift_id].site

        context.bot_data[BD.PING_SITE] = site

        query.edit_message_text(text="Ping send to site: " + site + " " + u'\U0001F6CE')

    return ConversationHandler.END

def follow_site_button(update : Update, context : CallbackContext):

    query = update.callback_query
    query.answer()

    site = context.user_data[UD.FOLLOW_SITE]

    if(query.data == BCD.FOLLOW_SITE_YES.name):

        user_name = None

        for x, y in context.bot_data[BD.USER_DICT].items():
            if (y == update.effective_chat.id):
                user_name = x

        print("New follow: " + user_name)

        context.bot_data[BD.FOLLOW_DICT][site].append(user_name)

        query.edit_message_text(text = "Following site: " + site + " " + u'\U0001F91D')

    if(query.data == BCD.FOLLOW_SITE_NO.name):
        print("N")

    return ConversationHandler.END
