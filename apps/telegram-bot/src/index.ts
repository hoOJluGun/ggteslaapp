import TelegramBot from 'node-telegram-bot-api';
import { connect, NatsConnection, StringCodec } from 'nats';

const token = process.env.TELEGRAM_BOT_TOKEN || 'YOUR_TELEGRAM_TOKEN_HERE';
const natsUrl = process.env.NATS_URL || 'nats://localhost:4222';
const helioCoreUrl = 'http://helio-core:3000';

const bot = new TelegramBot(token, { polling: true });
const sc = StringCodec();

let natsConn: NatsConnection;
let natsConnected = false;

const roles = new Map<number, string>();

async function connectNats() {
    try {
        natsConn = await connect({ servers: natsUrl });
        natsConnected = true;
        console.log('Connected to NATS from Telegram Bot');
        natsConn.closed().then(() => {
            natsConnected = false;
            console.warn('NATS connection closed');
        });
    } catch (e) {
        console.warn('Failed to connect to NATS, proceeding offline', e);
    }
}
connectNats().catch(console.error);

async function publishEvent(subject: string, payload: any) {
    if (!natsConnected) return;
    try {
        natsConn.publish(subject, sc.encode(JSON.stringify(payload)));
    } catch (e) {
        console.error('Failed to publish event', e);
    }
}

bot.onText(/\/start/, async (msg) => {
    const chatId = msg.chat.id;
    await bot.sendMessage(chatId, 'Добро пожаловать в платформу GG Tesla!', { parse_mode: 'Markdown' });
    await publishEvent('telegram.bot.start', { chatId });
});

bot.onText(/\/help/, async (msg) => {
    const chatId = msg.chat.id;
    const helpText = `
/start - Приветствие
/help - Справка по командам
/status - Статус сервера
/role <role> - Назначить роль
  `.trim();
    await bot.sendMessage(chatId, helpText);
});

bot.onText(/\/status/, async (msg) => {
    const chatId = msg.chat.id;
    try {
        const res = await fetch(`${helioCoreUrl}/health`);
        const data = await res.json();
        await bot.sendMessage(chatId, `Статус: ${data.status}\nNATS подключен: ${data.nats_connected}`);
    } catch {
        await bot.sendMessage(chatId, 'Не удалось получить статус сервера');
    }
});

bot.onText(/\/role (.+)/, async (msg, match) => {
    const chatId = msg.chat.id;
    const role = match?.[1].trim();
    if (!role) {
        await bot.sendMessage(chatId, 'Пожалуйста, укажите роль после команды /role');
        return;
    }
    roles.set(chatId, role);
    await publishEvent('authz.role.assign.v1', { userId: chatId, role });
    await bot.sendMessage(chatId, `Роль "${role}" назначена.`);
});
