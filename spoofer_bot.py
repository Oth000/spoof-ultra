import os
import subprocess
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# 👉 Mets ton vrai token ici :
TOKEN = "8086821854:AAGEV04klpCJMSrQZP_O54V_STOgg7PMxVc"

def handle_video(update: Update, context: CallbackContext):
    doc = update.message.document
    if not doc or not doc.file_name.lower().endswith(".mp4"):
        update.message.reply_text("❌ Envoie-moi une vidéo .mp4 en tant que fichier 📎")
        return

    # Téléchargement
    video_path = "input.mp4"
    spoofed_name = ""
    update.message.reply_text("📥 Téléchargement...")
    file = context.bot.get_file(doc.file_id)
    file.download(video_path)

    # Renommage pour le script
    if os.path.exists("input.mp4"):
        os.rename("input.mp4", "original.mp4")

    update.message.reply_text("🌀 Spoofing en cours...")
    result = subprocess.run(["bash", "spoofer_one.sh"], capture_output=True, text=True)
    print(result.stdout)

    # Cherche la vidéo générée
    for file in os.listdir():
        if file.startswith("IMG_") and file.endswith(".MP4"):
            spoofed_name = file
            break

    if spoofed_name:
        update.message.reply_text("✅ Spoof terminé. Envoi en cours...")
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(spoofed_name, "rb"))
        os.remove(spoofed_name)
    else:
        update.message.reply_text("❌ Échec : aucun fichier spoofé trouvé.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.document, handle_video))
    updater.start_polling()
    print("🤖 Bot en ligne.")
    updater.idle()

if __name__ == '__main__':
    main()

