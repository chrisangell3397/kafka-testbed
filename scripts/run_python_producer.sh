#! /bin/bash

# Print header
echo '-------------------------'
echo '    Kafka Testbed'
echo '   Python Producer'
echo '-------------------------'
echo ''

# Get current directory and script location
CURRENT_DIR="$(pwd)"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
#echo "Script directory: $SCRIPT_DIR"
#echo "Current directory: $CURRENT_DIR"

# Run producer
python3 "$SCRIPT_DIR/../python/kafka_producer.py"

# End of script
