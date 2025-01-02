TOKEN = '8164262122:AAG5DlcY1-6pVWkC_-qjXOcQTj22Jd-i7BM'

## Этот адрес нужно вручную менять после перезапуска ngrok https://d4c4-2001-41d0-ab05-00-2-0-26b.ngrok-free.app

# Проверьте информацию о вебхуке
# Выполните команду:
#
# Info

#curl https://api.telegram.org/bot8164262122:AAG5DlcY1-6pVWkC_-qjXOcQTj22Jd-i7BM/getWebhookInfo
#

#6. Очистите очередь обновлений
# Иногда обновления от Telegram "застаиваются" из-за того, что вебхук установлен неправильно. Очистите очередь, удалив текущий вебхук:
#
# Удалите вебхук:
# bash
# Копировать код
# curl -X POST https://api.telegram.org/bot<TOKEN>/deleteWebhook
# Установите вебхук заново:
# bash
# Копировать код
# curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://f6ab-141-227-138-58.ngrok-free.app/webhook"
# # deleteWebhook ЭТО НЕВЕРНЫЙ СИНТАКСИС
#curl -X POST https://api.telegram.org/bot8164262122:AAG5DlcY1-6pVWkC_-qjXOcQTj22Jd-i7BM/deleteWebhook

# СЕЙАС НАДО ПИСАТЬ ТАК...
# Invoke-WebRequest -Uri "https://api.telegram.org/bot8164262122:AAG5DlcY1-6pVWkC_-qjXOcQTj22Jd-i7BM/deleteWebhook" -Method POST
#Invoke-WebRequest -Uri "https://api.telegram.org/bot8164262122:AAG5DlcY1-6pVWkC_-qjXOcQTj22Jd-i7BM/getWebhookInfo"
