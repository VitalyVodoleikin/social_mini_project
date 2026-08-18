# ----------
# БЛОК ОБЪЯВЛЕНИЯ ФУНКЦИЙ

import json
import os

from PIL import Image, ImageDraw


def get_many_test_users_accounts_text_file(total_users_qt, superusers_qt):
    """Создает файл с необходимым кол-вом регистрационных
    данных тестовых аккаунтов, чтобы не прописывать их данные
    по-отдельности вручную.
    Будет создан файл с даннуми аккаунтов суперпользователей 
    и простых пользователей.
    Данные суперпользователей нужно внести в БД через интерфейс 
    терминала с помощью команды
    ```
    python manage.py createsuperuser
    ```
    """
    with open(
        "many_test_users_accounts_data.txt",
        "w",
        encoding="utf-8"
    ) as file:
        for i in range(1, total_users_qt + 1):
            file.write("\n")
            if i < (superusers_qt + 1):
                file.write(f"{i})\t\t\t\t\tsuperuser\n")
            else:
                file.write(f"{i})\t\t\t\t\tuser\n")
            file.write(f"username\t\t\tuser{i}\n")
            file.write(f"first_name\t\t\tuser{i}\n")
            file.write(f"last_username\t\tuser{i}\n")
            file.write(f"E-mail\t\t\t\tuser{i}@example-email.com\n")
            file.write(f"password\t\t\tpass_user{i}\n")
    

def get_many_test_simple_users_accounts_dump_file(
        total_users_qt, superusers_qt,
        usage_model, keys, avatar_path
):
    """
    Создает .json-файл "1_dump_many_simple_users.json"
    для загрузки данных о простых пользователях в БД с помощью фикстур.
    Команды в терминале:
    ```
    python manage.py loaddata <dump_file_name>
    ```
    В БД загрузятся данные о простых пользователях.
    Очередность загрузки данного файла в БД: 1.
    Формат времени, используемый в БД:
    2001-01-01 01:01:00.000001
    """
    simple_users_list = []
    for simple_user in range((superusers_qt + 1), (total_users_qt + 1)):
        user_fields_to_adding = {
            "model": usage_model,
            "pk": simple_user,
            "fields": {
                "password": f"{keys[simple_user]}",
                "last_login": f"2026-03-20 00:00:01.00000{len(simple_users_list) + 1}",
                "is_superuser": 0,
                "first_name": f"user{simple_user}",
                "last_name": f"user{simple_user}",
                "is_staff": 0,
                "is_active": 1,
                "email": f"user{simple_user}@example-email.com",
                "username": f"user{simple_user}",
                "avatar": avatar_path + f"-{simple_user}.png",
                "bio": f"User {simple_user}. {'About_me.' * 30}",
                "date_of_birth": "2000-01-15"
            }
        }
        simple_users_list.append(user_fields_to_adding)
    with open("1_dump_many_simple_users.json", "w", encoding="utf-8") as file:
        json.dump(simple_users_list, file, indent=2, ensure_ascii=False)


def get_many_posts_dump_file(
        total_users_qt, posts_qt,
        usage_model, img_path
):
    """
    Создает .json-файл "2_dump_many_posts.json"
    для загрузки данных о постах в БД.
    Очередность загрузки данного файла в БД: 2.
    """
    posts_list = []
    for user in range(1, total_users_qt + 1):
        for post in range(1, posts_qt + 1):
            post_to_adding = {
                "model": usage_model,
                "pk": len(posts_list) + 1,
                "fields": {
                    "content": f"Many_many_post's_text{user}--{post}\n" * 10,
                    "image": img_path + f"{user}--{post}.png",
                    "created_at": f"2026-03-20 00:00:01.000{len(posts_list) + 1}00+03:00",
                    "updated_at": f"2026-03-20 00:00:01.000{len(posts_list) + 1}00+03:00",
                    "author_id": user
                }
            }
            posts_list.append(post_to_adding)

    with open("2_dump_many_posts.json", "w", encoding="utf-8") as file:
        json.dump(posts_list, file, indent=2, ensure_ascii=False)


def get_many_images_and_avatar_at_mediaDir(
        total_users_qt, posts_qt,
        test_img_colors, test_avatar_colors,
        img_dir, avatar_dir, test_img_dementions,
        text_in_img_coords
):
    """
    Создает папку с тестовыми изображениями для каждого поста
    и папку с тестовыми аватарами для каждого пользователя.
    """
    # Создаём папки для сохранения media, если их нет
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(avatar_dir, exist_ok=True)
    # Создаем изображения для постов
    for user in range(1, total_users_qt + 1):
        for post in range(1, posts_qt + 1):
            # Создаём новое изображение
            img = Image.new(
                'RGB',
                test_img_dementions,
                color=test_img_colors[post - 1]
            )
            draw = ImageDraw.Draw(img)
            # Добавляем текст с номером изображения
            draw.text(
                text_in_img_coords,
                f"PostImage User {user} -- Post {post}",
                fill='black'
            )
            # Сохраняем файл
            filename = f"{img_dir}image{user}--{post}.png"
            img.save(filename)
            print(f"Создан файл: {filename}")
    # Создаем аватары для пользователей
    for user in range(1, total_users_qt + 1):
        # Создаём новый аватар
        avatar = Image.new(
            'RGB',
            test_img_dementions,
            color=test_avatar_colors[user - 1]
        )
        draw = ImageDraw.Draw(avatar)
        # Добавляем текст с номером аватара
        draw.text(text_in_img_coords, f"AVATAR User {user}", fill='black')
        # Сохраняем файл
        filename = f"{avatar_dir}avatar-{user}.png"
        avatar.save(filename)
        print(f"Создан аватар: {filename}")



# ----------
# КОНСТАНТЫ

# Как много необходимо создать тестовых аккаунтов суперпользователей
SUPERUSERS_QUANTITY = 2
# Как много необходимо создать тестовых аккаунтов пользователей
TOTAL_USERS_QUANTITY = 10
# Модель для пользователей
MODEL_USERS_USERS = "users.customuser"
# Ключи каждого простого пользователя в модели для пользователей
USER_PASS_KEYS = {
    3: (
        "pbkdf2_sha256$260000$JqfKk63PrNl10rcR0GiFPj$"
        "yx9cPM2RMlsKO9TcB6RjWkGc/Xx124dcOAxl9QP9v7Y="),
    4: (
        "pbkdf2_sha256$260000$hCF8U5S8Y1msHYFmOUVQZt$"
        "9/g1U3zjNzDrcQzzWOwZSs+cVIbAStBa/7jwt8U/qjc="),
    5: (
        "pbkdf2_sha256$260000$m5VIFoFCjfDarqqMBJTnff$"
        "1XQ04odNzjFEJejwF07TpUGb2l76NC5v9G9S5Rn5RPE="),
    6: (
        "pbkdf2_sha256$260000$7dgOoEz2krRd9Xp2v5VFM7$"
        "48mdePcGNSJ7RK1UMta1i+xIdu1Zd5KZI3b9psEZrYE="),
    7: (
        "pbkdf2_sha256$260000$eveWK7dBPIvYqi6Eq5vWz2$"
        "7AewBELE4Upfrt70mMNm9cUXJ96WNmS9AoeP+i3l+KA="),
    8: (
        "pbkdf2_sha256$260000$66NWF9WGMR05zw8yFfby5F$"
        "iP2a0W70hLa4gJPRk8Zjdrx90ZXJhizsHIlaaSar/4U="),
    9: (
        "pbkdf2_sha256$260000$3sTjZnISgfDmmCZhAwUNzV$"
        "L4vt9y0UtQeKvIGcTrpnr4QPaM0sY3nzF6WaSPfVQAE="),
    10: (
        "pbkdf2_sha256$260000$OGy3Sw5AFFb7ieyaLhJp3t$"
        "q8pXmysAJ2ch2I6MJvda/uvIAc+PuC2jv8RF72sgJd0=")
}
# Название папки с аватарами пользователей
AVATAR_DIR = "../media/avatar/"
# Ссылка на аватар в модели для пользователей
AVATAR_IMAGE_PATH = AVATAR_DIR + "avatar"
# Цвета для создания тестовых аватаров
AVATAR_COLORS = (
    "red", "orange", "yellow", "green", "blue",
    "indigo", "violet", "brown", "grey", "white"
)
# Модель для постов
MODEL_POSTS = "posts.post"
# Кол-во тестовых постов у каждого тестового пользователя
POSTS_FOR_EACH_USERS = 7

# Размеры изображения
IMAGE_SIZE = (500, 300)
# Размерф текста на тестовом изображении
TEXT_IN_IMG_COORDS = (160, 130)
# Название папки с изображениями
IMAGE_DIR = "../media/posts/images/"
# Ссылка на изображение в модели для рецептов
POSTS_IMAGE_PATH = IMAGE_DIR + "image"
# Цвета для создания тестовых изображений
IMG_COLORS = (
    "red", "orange", "yellow",
    "green", "blue", "indigo",
    "violet"
)



# ----------
# БЛОК ЗАПУСКА ФУНКЦИЙ
if __name__ == "__main__":
    get_many_test_users_accounts_text_file(TOTAL_USERS_QUANTITY, SUPERUSERS_QUANTITY)
    get_many_test_simple_users_accounts_dump_file(TOTAL_USERS_QUANTITY, SUPERUSERS_QUANTITY, MODEL_USERS_USERS, USER_PASS_KEYS, AVATAR_IMAGE_PATH)
    get_many_posts_dump_file(TOTAL_USERS_QUANTITY, POSTS_FOR_EACH_USERS, MODEL_POSTS, POSTS_IMAGE_PATH)
    get_many_images_and_avatar_at_mediaDir(TOTAL_USERS_QUANTITY, POSTS_FOR_EACH_USERS, IMG_COLORS, AVATAR_COLORS, IMAGE_DIR, AVATAR_DIR, IMAGE_SIZE, TEXT_IN_IMG_COORDS)



# ----------
# Дополнительная информация
# При генерации текстового файла с данными суперпользователей и простых пользователей
# будут сгенерированы текстовые данные 2-ух суперпользователей, которых мы регистрируем 
# через терминал вречную с помощью команды
# ```
# python manage.py createsuperuser
# ```
# Их пароли мы вносим через терминал при их регистрации, 
# но в самой таблице с пользоваетлями в БД будут находиться после регистрации такие 
# ключи их паролей:
# SUPERUSERS_PASS_KEYS = {
#     1: ("pbkdf2_sha256$1000000$y91JNg2rV68UHKIMrYKbgD$"
#         "FQOHP1W7Bpm2GCPSFlN9FOnm9RseeWu9tsa2y35IFko="),
#     2: ("pbkdf2_sha256$1000000$XJ7P1EO2deIRuR4E8CWqKS$"
#         "71+xRMwvcjAVk8V+tKpYhoaaLuBFZJedDX84g48S/vc=")
# }
# 
