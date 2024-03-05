import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
from polybot.img_proc import Img


class Bot:

    def __init__(self, token, telegram_chat_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        # set the webhook URL
        self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/', timeout=60)

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

    def is_current_msg_photo(self, msg):
        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :return:
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        # print(file_info)
        data = self.telegram_bot_client.download_file(file_info.file_path)
        # print(data)
        folder_name = file_info.file_path.split('/')[0]
        # print(folder_name)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def send_photo(self, chat_id, img_path, timeout=30):
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")

        self.telegram_bot_client.send_photo(chat_id, InputFile(img_path))

    def handle_message(self, msg):

        """Bot Main message handler"""
        logger.info(f'Incoming message: {msg}')
        self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')


class QuoteBot(Bot):
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')

        if msg["text"] != 'Please don\'t quote me':
            self.send_text_with_quote(msg['chat']['id'], msg["text"], quoted_msg_id=msg["message_id"])


# class ImageProcessingBot(Bot):

# def __init__(self, msg, telegram_bot_client):
#     self.msg = msg
#     self.telegram_bot_client = telegram_bot_client
#
# def blur(self):
#     img_path = self.download_user_photo(self.msg)
#     if 'caption' in self.msg and self.msg['caption'] == "blur":
#
#         new_image = Img(img_path)
#         new_image.blur()
#         new_path = new_image.save_img()
#         self.send_photo(self.msg['chat']['id'], new_path)
#
# def rotate(self):
#     img_path = self.download_user_photo(self.msg)
#     if 'caption' in self.msg and self.msg['caption'] == "rotate":
#         new_image = Img(img_path)
#         new_image.rotate()
#         new_path = new_image.save_img()
#         self.send_photo(self.msg['chat']['id'], new_path)
class ImageProcessingBot(Bot):

    def handle_message(self, msg):

        if not self.is_current_msg_photo(msg):

            """Bot Main message handler"""
            if msg["text"] == "Hi" or msg["text"] == "hi":
                # new_comm = "hi %s how i can help you" % msg["from"]["first_name"]
                new_comm = f'hi {msg["from"]["first_name"]} how can I help you?'
                logger.info(f'Incoming message: {msg["text"]}')
                self.send_text(msg['chat']['id'], new_comm)

            elif not msg["text"] == "Hi" or not msg["text"] == "hi":
                logger.info(f'incoming message {msg["text"]}')
                self.send_text(msg['chat']['id'], msg["text"])

        else:
            try:
                if 'caption' in msg:
                    caption = msg['caption']
                    if caption == 'blur':
                        self.blur(msg)
                    elif caption == 'contour':
                        self.contour(msg)
                    elif caption == 'rotate':
                        self.rotate(msg)
                    elif caption == 'segment':
                        pass
                    elif caption == 'salt and pepper':
                        pass
                    elif caption == 'concat':
                        pass
                    else:
                        self.send_text(msg['chat']['id'],"Invalid caption. Please try again with one of the following: ['Blur', 'Contour', 'Rotate', 'Segment', 'Salt and pepper', 'Concat']")
                else:
                    self.send_text(msg['chat']['id'], "No caption found. Please include a caption.")
            except Exception as e:

                logger.info(f"Error occurred: {e}")
                self.send_text(msg['chat']['id'], "Something went wrong... Please try again later.")

    def blur(self, msg):
        try:
            img_path = self.download_user_photo(msg)
            new_image = Img(img_path)
            new_image.blur()
            new_path = new_image.save_img()
            self.send_photo_with_timeout(msg['chat']['id'], new_path)
        except Exception as e:
            logger.info(f"Error occurred during blur processing: {e}")
            self.send_text(msg['chat']['id'], "Error processing image... Please try again later.")

    def rotate(self, msg):

        try:
            img_path = self.download_user_photo(msg)
            if 'caption' in msg and msg['caption'] == "rotate":
                new_image = Img(img_path)
                new_image.rotate()
                new_path = new_image.save_img()
                # self.send_photo(msg['chat']['id'], new_path)
                self.send_photo_with_timeout(msg['chat']['id'], new_path)
        except Exception as e:
            logger.info(f"Error occurred during blur processing: {e}")
            self.send_text(msg['chat']['id'], "Error processing image... Please try again later.")


    def contour(self, msg):
        try:
            img_path = self.download_user_photo(msg)
            new_image = Img(img_path)
            new_image.contour()
            new_path = new_image.save_img()
            self.send_photo_with_timeout(msg['chat']['id'], new_path)
        except Exception as e:
            logger.info(f"Error occurred during blur processing: {e}")
            self.send_text(msg['chat']['id'], "Error processing image... Please try again later.")




    # Implement other image processing methods (contour, rotate, segment, salt_and_pepper, concat) similarly

    def send_photo_with_timeout(self, chat_id, photo_path, timeout=30):
        try:
            self.send_photo(chat_id, photo_path)
        except Exception as e:

            logger.info(f"Error sending photo to chat {chat_id}: {e}")
            self.send_text(chat_id, "Error sending photo... Please try again later.")
