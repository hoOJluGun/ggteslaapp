const Fastify = require('fastify')
const initFastify = Fastify({ logger: true })

initFastify.get('/', async (request, reply) => {
    return { hello: 'helio core' }
})

const start = async () => {
    try {
        await initFastify.listen({ port: 3000, host: '0.0.0.0' })
    } catch (err) {
        initFastify.log.error(err)
        process.exit(1)
    }
}
start()
