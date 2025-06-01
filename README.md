Простой API на FastAPI с интеграцией платежной системы Stripe для оплаты товаров.

Проект реализует сервер с тремя основными эндпоинтами:

- GET /item/{item_id} - возвращает HTML-страницу с информацией о товаре и кнопкой "Buy". При нажатии на кнопку запускается процесс оплаты через Stripe.
- GET /buy/{item_id} — создаёт Stripe Checkout Session для оплаты одного товара и возвращает `session_id`.
- POST /order/buy — создаёт Stripe Checkout Session для оплаты заказа, состоящего из нескольких товаров, переданных списком ID.

-- Установка и запуск

1. Клонируйте репозиторий:

git clone https://github.com/yourusername/your-repo.git
cd your-repo


2. Создайте и активируйте виртуальное окружение:

python -m venv .venv
.venv\Scripts\activate # Windows


3. Установите зависимости:

pip install fastapi uvicorn stripe python-dotenv


4. Создайте файл `.env` в корне проекта и добавьте в него ваши ключи Stripe:

SK_STRIPE_API_KEY=sk_test_ваш_секретный_ключ
PK_STRIPE_PUBLIC_KEY=pk_test_ваш_публичный_ключ


5. Запустите приложение:

uvicorn main:app --reload


6. Откройте в браузере страницу товара, например:

http://127.0.0.1:8000/item/1



-- Использование

- На странице товара нажмите кнопку "Buy" для оплаты одного товара.
- Для оплаты нескольких товаров отправьте POST-запрос на `/order/buy` с JSON телом:

{
"item_ids": [1,}

Технологии

- Python 3.13
- FastAPI
- Stripe Python
- Pydantic
- python-dotenv
