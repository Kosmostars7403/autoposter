import os
from dotenv import load_dotenv
import vk_api
import telegram
import requests
import argparse


def post_vk(image_path, text_path):
    vk_session = vk_api.VkApi(login=vk_user_login, token=vk_user_token)
    vk = vk_session.get_api()

    upload = vk_api.VkUpload(vk_session)

    photo_sizes = upload.photo(
        image_path,
        album_id=vk_album_id,
        group_id=vk_group_id
    )

    with open(text_path, 'r') as caption:
        vk.wall.post(owner_id='-{}'.format(vk_group_id), message=caption.read(), from_group=1,
                     attachments='photo-{}_{}'.format(vk_group_id, photo_sizes[0]['id']))


def post_telegram(image_path, text_path):
    bot = telegram.Bot(token=telegram_token)
    with open(text_path, 'r') as caption, open(image_path, 'rb') as image:
        bot.send_message(chat_id=telegram_channel, text=caption.read())
        bot.send_photo(chat_id=telegram_channel, photo=image)


def post_facebook(image_path, text_path):
    url = "https://graph.facebook.com/v7.0/{}/photos".format(facebook_group_id)
    with open(text_path, 'r') as caption, open(image_path, 'rb') as image:
        files = {'file': image}
        payrole = {
            'caption': caption.read(),
            'access_token': facebook_token,
        }
        response = requests.post(url, files=files, data=payrole)
        response.raise_for_status()


def parse_console_arguments():
    parser = argparse.ArgumentParser(description='Постинг в VK, Telegram, Facebook')
    parser.add_argument('image', help='Путь к изображению')
    parser.add_argument('text', help='Путь к тексту')
    parser.add_argument('-pf', '--post_facebook', help='Выложить в Facebook.', action='store_true')
    parser.add_argument('-pt', '--post_telegram', help='Выложить в Telegram.', action='store_true')
    parser.add_argument('-pv', '--post_vk', help='Выложить во Вконтакте.', action='store_true')

    return parser


if __name__ == '__main__':
    load_dotenv()

    vk_user_token = os.getenv('VK_USER_TOKEN')
    vk_user_login = os.getenv('VK_USER_LOGIN')
    vk_group_id = os.getenv('VK_GROUP_ID')
    vk_album_id = os.getenv('VK_ALBUM_ID')

    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_channel = os.getenv('TELEGRAM_CHANEL_ID')

    facebook_token = os.getenv('FACEBOOK_TOKEN')
    facebook_group_id = os.getenv('FACEBOOK_GROUP_ID')

    parser = parse_console_arguments()

    args = parser.parse_args()

    if args.post_facebook:
        post_facebook(args.image, args.text)

    if args.post_vk:
        post_vk(args.image, args.text)

    if args.post_telegram:
        post_telegram(args.image, args.text)
