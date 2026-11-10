#! /bin/bash

# Print header
echo '-------------------------'
echo '     Kafka Testbed'
echo '  Javascript Consumer'
echo '-------------------------'
echo ''

# Get current directory and script location
CURRENT_DIR="$(pwd)"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
#echo "Script directory: $SCRIPT_DIR"
#echo "Current directory: $CURRENT_DIR"

# Run consumer
node "$SCRIPT_DIR/../javascript/javascript_consumer.js"

# End of script
