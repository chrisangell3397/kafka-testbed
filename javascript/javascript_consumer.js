/**
 * Simple Kafka consumer that prints messages from a topic to the console.
 *
 * Requires: npm install kafkajs
 */
const { Kafka, logLevel } = require('kafkajs')

const BOOTSTRAP_SERVERS = 'localhost:9092'
const TOPIC = 'numbers-test-v0p1'
const GROUP_ID = 'numbers-consumer-js'

const kafka = new Kafka({
  clientId: 'numbers-consumer-js',
  brokers: [BOOTSTRAP_SERVERS],
  logLevel: logLevel.WARN,
});

const consumer = kafka.consumer({ groupId: GROUP_ID })

async function main() {
  await consumer.connect();
  // fromBeginning: start from the earliest message if the group has no committed offset
  await consumer.subscribe({ topic: TOPIC, fromBeginning: true })
  console.log(`Listening on '${TOPIC}'... (Ctrl+C to stop)`)

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      console.log(
        `${topic}[${partition}] @ offset ${message.offset}: ${message.value.toString('utf-8')}`
      );
    },
  });
}

async function shutdown() {
  console.log('\nStopping...')
  try {
    await consumer.disconnect()
  } finally {
    process.exit(0)
  }
}

process.on('SIGINT', shutdown)
process.on('SIGTERM', shutdown)

main().catch((err) => {
  console.error('Consumer error:', err)
  process.exit(1)
})