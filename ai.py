import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

# Clé API Telegram
TELEGRAM_API_KEY = '7044574411:AAFxdsxuq3kfwneKewngfbzqVx3OrhCtLcM'

# URL de l'API externe
API_URL = "https://kaiz-apis.gleeze.com/api/gpt-4o"

# Configurer le logging pour suivre les erreurs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Fonction pour démarrer la conversation
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Salut ! 😊 Tu as une question ? Je suis là pour t'aider.")

# Fonction pour traiter les messages et obtenir des réponses de l'API GPT
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text  # Message de l'utilisateur

    if user_message.startswith('/'):
        return  # Ignorer les commandes

    try:
        # Préparer la requête pour l'API GPT de manière rapide
        params = {
            'q': user_message,
            'uid': update.message.from_user.id  # ID de l'utilisateur pour personnaliser l'appel
        }

        # Effectuer la requête à l'API en utilisant un appel rapide
        response = await asyncio.to_thread(requests.get, API_URL, params=params)

        # Vérifier si la réponse est correcte
        if response.status_code == 200:
            data = response.json()  # Extraire les données JSON de la réponse
            bot_reply = data.get('response', 'Désolé, je n\'ai pas pu répondre à ta question.')

            # Styliser et ajouter des emojis pour rendre la réponse plus naturelle
            styled_reply = bot_reply + " 😊✨"

            # Envoi de la réponse générée par l'API, sans délai perçu
            await update.message.reply_text(styled_reply)
        else:
            await update.message.reply_text("Désolé, il semble y avoir un problème avec la réponse. Je vais vérifier ça ! 😕")
            logger.error(f"Erreur de l'API GPT : {response.status_code}")
    
    except Exception as e:
        await update.message.reply_text("Oups, un problème est survenu... Essaie un peu plus tard ! 😔")
        logger.error(f"Erreur : {e}")

# Fonction pour gérer les erreurs
def error(update: Update, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Fonction principale pour démarrer la conversation
def main():
    # Crée une instance de l'Application avec le token de ton bot Telegram
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Ajoute un gestionnaire pour la commande /start
    application.add_handler(CommandHandler("start", start))

    # Ajoute un gestionnaire pour les messages texte
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Ajoute un gestionnaire pour les erreurs
    application.add_error_handler(error)

    # Démarre la conversation
    application.run_polling()

if __name__ == '__main__':
    main()
