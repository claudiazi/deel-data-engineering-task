import airbyte as ab
from airbyte.caches import SnowflakeCache
from airbyte.strategies import WriteStrategy
import time

source = ab.get_source(
   "source-postgres",
   install_if_missing=True,
    version="3.6.30",
   config={
       "host": "host.docker.internal",
       "port": 5432,
         "database": "finance_db",
         "username": "cdc_user",
        "password": "cdc_1234",
         "replication_method": {
                "method": "CDC",
                "replication_slot": "cdc_pgoutput",
                "publication": "cdc_publication",
                "initial_waiting_seconds": 120,
            },
        "schemas": ["operations"],
        "ssl_mode": { "mode": "disable"
},}
)

# somehow the destination-snowflake didnt work out as expected, use SnowflakeCache instead as a temporary solution
sf_cache = SnowflakeCache(
      account="BUTEFLJ-DH94720",
      username="AIRBYTE_USER",
      password="1234",
      warehouse="AIRBYTE_WAREHOUSE",
      database="BRONZE_LAYER",
      role="AIRBYTE_ROLE",
      schema_name="FINANCE_DB__OPERATIONS"
)


def run_sync():
    source.check()
    source.select_streams(["customers", "orders", "products", "order_items"])
    source.read(cache=sf_cache, write_strategy=WriteStrategy.APPEND)
    print("Sync completed.")


if __name__ == "__main__":
    while True:
        run_sync()
        print("Waiting 10 minutes until next sync...")
        time.sleep(600)  # 600 seconds = 10 minutes