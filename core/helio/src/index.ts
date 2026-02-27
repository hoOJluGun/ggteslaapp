import Fastify from 'fastify';
import { connect } from 'nats';

const fastify = Fastify({ logger: true });

fastify.get('/health', async (request, reply) => {
    return { status: 'OK' };
});

const start = async () => {
    try {
        try {
            const nc = await connect({ servers: process.env.NATS_URL || 'nats://localhost:4222' });
            fastify.log.info(`Connected to NATS: ${nc.getServer()}`);
        } catch (e) {
            fastify.log.warn("NATS disconnected, starting in standalone mode");
        }

        await fastify.listen({ port: 3000, host: '0.0.0.0' });
    } catch (err) {
        fastify.log.error(err);
        process.exit(1);
    }
};

start();
