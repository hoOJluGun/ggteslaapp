import Fastify from 'fastify';
import { connect, StringCodec } from 'nats';

const app = Fastify({ logger: true });
const sc = StringCodec();

async function start() {
  const nc = await connect({ servers: process.env.NATS_URL ?? 'nats://localhost:4222' });

  app.get('/health', async () => ({ ok: true }));

  app.post('/events/:subject', async (req, reply) => {
    const subject = (req.params as { subject: string }).subject;
    nc.publish(subject, sc.encode(JSON.stringify(req.body ?? {})));
    return reply.send({ published: subject });
  });

  await app.listen({ host: '0.0.0.0', port: 3000 });
}

start().catch((err) => {
  console.error(err);
  process.exit(1);
});
