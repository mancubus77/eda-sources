# mancubus77.events - Event Driven Ansible Collection

This collection provides Event Driven Ansible (EDA) source plugins for consuming events from AMQP and Kafka message brokers.

## Collection Contents

### Event Source Plugins

#### 1. AMQP Event Source (`amq.py`)

An event source plugin for receiving events via AMQP (Advanced Message Queuing Protocol) using the `aio-pika` library.

**Parameters:**
- `host` (required): The hostname where the AMQP broker is running
- `port` (required): The port where the AMQP server is listening  
- `channel` (required): The AMQP queue/channel name to consume from
- `username` (required): Username for AMQP broker authentication
- `password` (required): Password for AMQP broker authentication
- `encoding` (optional): Message encoding scheme (default: utf-8)

**Example Usage:**
```yaml
sources:
  - mancubus77.events.amq:
      host: "rabbitmq.example.com"
      port: 5672
      channel: "events-queue"
      username: "user"
      password: "password"
      encoding: "utf-8"
```

#### 2. Kafka Enhanced Event Source (`kafka_enhanced.py`)

An enhanced event source plugin for receiving events via Kafka topics using the `aiokafka` library with comprehensive SSL/SASL support.

**Parameters:**
- `host` (required): The hostname where the Kafka broker is running
- `port` (required): The port where the Kafka server is listening
- `topic` (required): The Kafka topic to consume from
- `group_id` (optional): Kafka consumer group ID
- `offset` (optional): Offset reset policy [latest, earliest] (default: latest)
- `encoding` (optional): Message encoding scheme (default: utf-8)

**SSL Configuration:**
- `cafile`: Certificate authority file path
- `certfile`: Client certificate file path  
- `keyfile`: Client private key file path
- `password`: Password for certificate chain
- `check_hostname`: Enable SSL hostname verification (default: true)
- `verify_mode`: Certificate verification mode [CERT_NONE, CERT_OPTIONAL, CERT_REQUIRED] (default: CERT_REQUIRED)

**SASL Configuration:**
- `security_protocol`: Protocol for broker communication [PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL] (default: PLAINTEXT)
- `sasl_mechanism`: Authentication mechanism [PLAIN, GSSAPI, SCRAM-SHA-256, SCRAM-SHA-512, OAUTHBEARER] (default: PLAIN)
- `sasl_plain_username`: Username for SASL PLAIN authentication
- `sasl_plain_password`: Password for SASL PLAIN authentication

**Example Usage:**
```yaml
sources:
  - mancubus77.events.kafka_enhanced:
      host: "kafka.example.com"
      port: 9092
      topic: "events-topic"
      group_id: "eda-consumer-group"
      offset: "latest"
      security_protocol: "SSL"
      check_hostname: true
```

## Rulebook Examples

### AMQP Rulebook Example

```yaml
- name: AMQP Event Listener
  hosts: localhost
  execution_strategy: parallel
  sources:
    - mancubus77.events.amq:
        host: "rabbitmq.example.com"
        port: 5672
        channel: "notifications"
        username: "eda-user"
        password: "eda-password"

  rules:
    - name: Process AMQP Events
      condition:
        all:
          - event.body is defined
      action:
        print_event:
          pretty: true
    
    - name: Alert on Critical Messages
      condition:
        all:
          - event.body.level == "critical"
      action:
        debug:
          msg: "Critical alert received: {{ event.body.message }}"
```

### Kafka Rulebook Example

```yaml
- name: Kafka Event Listener
  hosts: localhost
  execution_strategy: parallel
  sources:
    - mancubus77.events.kafka_enhanced:
        host: "kafka.example.com"
        port: 9092
        topic: "application-events"
        group_id: "eda-processors"
        offset: "latest"
        security_protocol: "SASL_SSL"
        sasl_mechanism: "SCRAM-SHA-256"
        sasl_plain_username: "eda-consumer"
        sasl_plain_password: "secure-password"

  rules:
    - name: Process Kafka Events
      condition:
        all:
          - event.value is defined
      action:
        print_event:
          pretty: true
          
    - name: Handle Error Events
      condition:
        all:
          - event.value.type == "error"
      action:
        debug:
          msg: "Error event received from {{ event.value.service }}"
```

## Installation

### From Source
```bash
# Clone the repository
git clone https://github.com/mancubus77/eda-sources.git
cd eda-sources

# Build the collection
ansible-galaxy collection build

# Install the collection
ansible-galaxy collection install mancubus77-events-1.0.0.tar.gz
```

### From Ansible Galaxy (when published)
```bash
ansible-galaxy collection install mancubus77.events
```

## Dependencies

### Python Dependencies
- `aio-pika`: For AMQP event source
- `aiokafka`: For Kafka event source

### System Requirements
- Python 3.8+
- Event Driven Ansible (EDA) Server
- Access to AMQP/Kafka message brokers

## Running Rulebooks

### Using ansible-rulebook
```bash
# Run AMQP rulebook
ansible-rulebook --rulebook extensions/eda/rulebooks/rb.amqp.yaml -i inventory.yml

# Run Kafka rulebook  
ansible-rulebook --rulebook extensions/eda/rulebooks/rb.kafka.yaml -i inventory.yml
```

### Using ansible-navigator
```bash
# With the provided configuration
ansible-navigator run extensions/eda/rulebooks/rb.kafka.yaml
```

## Development

### Setting up Development Environment
1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install aio-pika aiokafka
   ```
3. Use the provided `ansible-navigator.yaml` for containerized development

### Testing
Test your event sources by running the rulebooks against real AMQP/Kafka brokers or using containerized versions:

```bash
# Example with Docker Compose for local testing
docker-compose up -d rabbitmq kafka
ansible-rulebook --rulebook extensions/eda/rulebooks/rb.amqp.yaml -i inventory.yml
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with real message brokers
5. Submit a pull request

## License

GPL-2.0-or-later

## Support

For issues and questions, please use the [GitHub Issues](https://github.com/mancubus77/eda-sources/issues) tracker.
