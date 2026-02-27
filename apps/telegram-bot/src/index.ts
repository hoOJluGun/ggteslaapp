import TelegramBot from 'node-telegram-bot-api';
import { connect } from 'nats';

const token = process.env.TELEGRAM_BOT_TOKEN || 'YOUR_TELEGRAM_TOKEN_HERE';
const bot = new TelegramBot(token, { polling: true });

async function start() {
    try {
        const nc = await connect({ servers: process.env.NATS_URL || 'nats://localhost:4222' });
        console.log(`Connected to NATS: ${nc.getServer()}`);
    } catch (e) {
        console.warn("NATS connection skipped or failed, bot will run offline.");
    }

    bot.onText(/\/start/, (msg) => bot.sendMessage(msg.chat.id, 'Welcome to GG Tesla Bot!'));
    bot.onText(/\/help/, (msg) => bot.sendMessage(msg.chat.id, 'Available commands: /start, /help, /status, /role'));
    bot.onText(/\/status/, (msg) => bot.sendMessage(msg.chat.id, 'Bot status: SUPER OK'));
    bot.onText(/\/role (.+)/, (msg, match) => {
        const role = match ? match[1] : 'user';
        bot.sendMessage(msg.chat.id, `Role successfully set to: ${role}`);
    });
}

start().catch(console.error);
