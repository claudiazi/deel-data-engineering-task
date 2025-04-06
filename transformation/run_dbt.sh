#!/bin/bash
# Run all models once
echo "Starting initial run: dbt run --profiles-dir .dbt"
dbt run  --profiles-dir .dbt

echo "Initial run complete. Sleeping for 600 seconds before starting periodic updates."
sleep 600

# Update the silver_layer and marts every 10 minutes
while true; do
    echo "Starting update: dbt run -s models/marts --profiles-dir .dbt"
    dbt run -s models/marts --profiles-dir .dbt
    echo "Update complete. Sleeping for 600 seconds before the next update."
    sleep 600  # Sleep for 600 seconds (10 minutes)
done
