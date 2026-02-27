import { Telegraf } from 'telegraf';
import { connect, StringCodec } from 'nats';

const token = process.env.TELEGRAM_BOT_TOKEN ?? '';
const bot = new Telegraf(token);
const sc = StringCodec();

async function bootstrap() {
  const nc = await connect({ servers: process.env.NATS_URL ?? 'nats://localhost:4222' });

  bot.command('report', async (ctx) => {
    nc.publish('report.generate', sc.encode(JSON.stringify({ chatId: ctx.chat.id })));
    await ctx.reply('Report generation requested');
  });

  bot.command('role', async (ctx) => {
    nc.publish('authz.role.assign', sc.encode(JSON.stringify({ userId: ctx.from?.id, role: 'viewer' })));
    await ctx.reply('Role assignment event published');
  });

  await bot.launch();
}

bootstrap().catch(console.error);
