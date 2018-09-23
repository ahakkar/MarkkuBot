# -*- coding: utf-8 -*-

from core.printlog import printlog
from core.count_and_write import count_and_write
from core.get_ids import get_ids

class CommandRouter():
    def __init__(self, db):
        self.db = db

    def start(self, bot, update):
        printlog(update, "start")

        _, chat_id = get_ids(update) # Ignoraa user_id, tätä käytetään paljon
        count_and_write(self.db, update, "commands")

        bot.send_message(chat_id=chat_id, text="Woof woof")

    def stats(self, bot, update):
        printlog(update, "stats")

        user_id, chat_id = get_ids(update)

        count_and_write(self.db, update, "commands")

        if self.db.in_blacklist(user_id):
            update.message.reply_text("Markku ei seuraa sinua. Käytä komentoa /unblacklist , jos haluat seurannan käyttöön.\n" \
                                    "Markku does not track you. Use the command /unblacklist to enable tracking.")
            return

        count_messages = self.db.get_counter_user(user_id, chat_id, "count.messages")
        count_stickers = self.db.get_counter_user(user_id, chat_id, "count.stickers")
        count_kiitos = self.db.get_counter_user(user_id, chat_id, "count.kiitos")
        count_photos = self.db.get_counter_user(user_id, chat_id, "count.photos")

        sticker_percent = 0
        kiitos_percent = 0

        if count_stickers + count_messages != 0:
            sticker_percent = round((count_stickers / (count_stickers+count_messages) * 100), 2)
        
        if count_messages != 0:
            kiitos_percent = round((count_kiitos / count_messages * 100), 2)

        msg = "@{}:\nMessages: {}".format(update.message.from_user.username, count_messages)
        msg += "\nStickers: {} ({}%)".format(count_stickers, sticker_percent)
        msg += "\nKiitos: {} ({}%)".format(count_kiitos, kiitos_percent)
        msg += "\nPhotos: {}".format(count_photos)        

        bot.send_message(chat_id=chat_id, text=msg)