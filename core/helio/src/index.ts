import Fastify from 'fastify';
import swagger from '@fastify/swagger';
import swaggerUi from '@fastify/swagger-ui';
import { connect, NatsConnection, StringCodec, JetStreamManager, JetStreamClient } from 'nats';

const fastify = Fastify({ logger: true });
const sc = StringCodec();

let natsConn: NatsConnection | null = null;
let jsm: JetStreamManager | null = null;
let js: JetStreamClient | null = null;
let natsConnected = false;

async function connectNats() {
    try {
        natsConn = await connect({ servers: process.env.NATS_URL || 'nats://localhost:4222' });
        jsm = await natsConn.jetstreamManager();
        js = natsConn.jetstream();
        natsConnected = true;
        fastify.log.info('Connected to NATS JetStream');
        natsConn.closed().then(() => {
            natsConnected = false;
            fastify.log.warn('NATS connection closed');
        });
    } catch (err) {
        natsConnected = false;
        fastify.log.warn('Failed to connect to NATS JetStream, continuing without it');
    }
}

fastify.post<{
    Params: { subject: string };
    Body: any;
}>('/events/:subject', {
    schema: {
        body: { type: 'object' },
        params: {
            type: 'object',
            properties: {
                subject: { type: 'string', minLength: 1 },
            },
            required: ['subject'],
        },
    },
}, async (request, reply) => {
    if (!natsConnected || !js) {
        reply.status(503).send({ error: 'NATS not connected' });
        return;
    }
    const subject = request.params.subject;
    const payload = request.body;
    try {
        const data = JSON.stringify(payload);
        await js.publish(subject, sc.encode(data));
        reply.send({ status: 'published', subject });
    } catch (err) {
        reply.status(500).send({ error: 'Failed to publish event' });
    }
});

fastify.get('/health', async () => {
    return {
        status: 'OK',
        nats_connected: natsConnected,
    };
});

const start = async () => {
    await fastify.register(swagger, {
        openapi: {
            info: {
                title: 'Helio Core API',
                version: '1.0.0',
            },
        },
    });

    await fastify.register(swaggerUi, {
        routePrefix: '/docs',
        uiConfig: {
            docExpansion: 'full',
            deepLinking: false,
        },
        staticCSP: true,
        transformStaticCSP: (header) => header,
    });

    try {
        await fastify.listen({ port: 3000, host: '0.0.0.0' });
        fastify.log.info('Server listening on 0.0.0.0:3000');
        connectNats(); // async execution without blocking start
    } catch (err) {
        fastify.log.error(err);
        process.exit(1);
    }
};
start();
