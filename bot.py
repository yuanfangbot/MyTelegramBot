# /// script
# dependencies = ['python-telegram-bot']
# ///
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- 机器人命令处理函数 ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    处理 /start 命令。
    当用户发送 /start 命令时，机器人会回复欢迎消息。
    """
    user = update.effective_user
    await update.message.reply_html(
        f"你好 {user.mention_html()}! 我是一个稳定的Telegram机器人。",
        # reply_markup=ForceReply(selective=True),
    )
    logger.info(f"用户 {user.full_name} ({user.id}) 发送了 /start 命令。")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    处理 /help 命令。
    当用户发送 /help 命令时，机器人会回复帮助信息。
    """
    await update.message.reply_text("我能做什么？\n\n"
                                    "你可以尝试以下命令：\n"
                                    "/start - 开始与机器人对话\n"
                                    "/help - 获取帮助信息\n"
                                    "或者直接给我发送消息，我会复述你的话。")
    logger.info(f"用户 {update.effective_user.full_name} ({update.effective_user.id}) 发送了 /help 命令。")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    处理普通文本消息。
    机器人会复述用户发送的任何文本消息。
    """
    await update.message.reply_text(f"你说了: {update.message.text}")
    logger.info(f"用户 {update.effective_user.full_name} ({update.effective_user.id}) 发送了消息: {update.message.text}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    处理所有未捕获的错误。
    记录错误信息，并在必要时通知用户。
    """
    logger.warning(f"更新 {update} 导致错误 {context.error}")
    # 可以选择性地向用户发送错误消息
    if update.effective_message:
        await update.effective_message.reply_text("抱歉，我遇到了一个错误。请稍后再试。")

# --- 主函数 ---

def main() -> None:
    """
    启动机器人。
    """
    # 在这里替换为你的机器人TOKEN
    # 你需要从 BotFather 获取你的TOKEN
    # 例如: TOKEN = "YOUR_BOT_TOKEN_HERE"
    TOKEN = "YOUR_BOT_TOKEN_HERE" # <--- 请替换为你的机器人TOKEN

    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("请在 bot.py 文件中替换 'YOUR_BOT_TOKEN_HERE' 为你的实际机器人TOKEN！")
        return

    # 构建应用程序
    application = Application.builder().token(TOKEN).build()

    # 注册命令处理程序
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # 注册消息处理程序 (非命令，处理所有文本消息)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # 注册错误处理程序
    application.add_error_handler(error_handler)

    # 启动机器人
    logger.info("机器人开始轮询更新...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("机器人已停止。")

if __name__ == "__main__":
    main()
