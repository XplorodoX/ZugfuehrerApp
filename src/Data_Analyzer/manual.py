# Author: Marc Nebel
# Beschreibung: Modul welches eine JSON Objekt mit der Erklärung der Datenbanken für den
# Flask REST Server enthällt

manual = {
  "table1": {
    "name": "delay",
    "description": "This table stores all delays and base value needed for furhter calculations. This isnt intended to be used outside this service",
    "columns": [
      {"name": "date", "type": "Date", "primary_key": True},
      {"name": "n", "type": "Integer", "primary_key": True},
      {"name": "station", "type": "String", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"},
      {"name": "first_station", "type": "Boolean"},
      {"name": "final_station", "type": "Boolean"},
      {"name": "destination", "type": "String"}
    ]
  },
  "table2": {
    "name": "avg_delay_at_over_time",
    "description": "The average delay of all exisiting delays calculated at different points in time",
    "columns": [
      {"name": "n", "type": "Integer", "primary_key": True},
      {"name": "c_date", "type": "Date", "primary_key": True},
      {"name": "station", "type": "String", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  },
  "table3": {
    "name": "avg_delay_at",
    "description": "The average delay of all exisitng delays",
    "columns": [
      {"name": "n", "type": "Integer", "primary_key": True},
      {"name": "station", "type": "String", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  },
  "table4": {
    "name": "avg_delay_at_final",
    "description": "the average delay of the start and the end of a given line",
    "columns": [
      {"name": "n", "type": "Integer", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  },
  "table5": {
    "name": "avg_delay_st_daily",
    "description": "The average daily delay per line. Note that lines are unique per day, so this table is currently the same as delay",
    "columns": [
      {"name": "n", "type": "Integer", "primary_key": True},
      {"name": "date", "type": "Date", "primary_key": True},
      {"name": "station", "type": "String", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  },
  "table6": {
    "name": "avg_delay_st_daily_final",
    "description": "The average daily delay per line at the start and the end of the journey",
    "columns": [
      {"name": "n", "type": "Integer", "primary_key": True},
      {"name": "date", "type": "Date", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  },
  "table7": {
    "name": "avg_delay_st_weekly",
    "description": "The same as the above but weekly",
    "columns": [
      {"name": "n", "type": "Integer", "primary_key": True},
      {"name": "date", "type": "Date", "primary_key": True},
      {"name": "station", "type": "String", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  },
  "table8": {
    "name": "avg_delay_st_weekly_final",
    "description": "The same as the upper daily final but with weeks instead",
    "columns": [
      {"name": "n", "type": "Integer", "primary_key": True},
      {"name": "date", "type": "Date", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  },
  "table9": {
    "name": "avg_delay_st_monthly",
    "description": "The same as the abive but monthly",
    "columns": [
      {"name": "n", "type": "Integer", "primary_key": True},
      {"name": "date", "type": "Date", "primary_key": True},
      {"name": "station", "type": "String", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  },
  "table10": {
    "name": "avg_delay_st_monthly_final",
    "description": "The same as the upper weekly but with months",
    "columns": [
      {"name": "n", "type": "Integer", "primary_key": True},
      {"name": "date", "type": "Date", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  },
  "table11": {
    "name": "avg_delay_destination_final",
    "description": "The average delays of the start and the end of an entire line (AA -> Ulm f.e.)",
    "columns": [
      {"name": "destination", "type": "String", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  },
  "table12": {
    "name": "avg_delay_destination_final_over_time",
    "description": "The same as the above but calculated over different points in time",
    "columns": [
      {"name": "destination", "type": "String", "primary_key": True},
      {"name": "c_date", "type": "Date", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  },
  "table13": {
    "name": "avg_delay_destination",
    "description": "the delay per station per entire line, kinda redundant but important for stations with multiple destinations",
    "columns": [
      {"name": "destination", "type": "String", "primary_key": True},
      {"name": "station", "type": "String", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  },
  "table14": {
    "name": "avg_delay_destination_over_time",
    "description": "The same as the above but over time",
    "columns": [
      {"name": "destination", "type": "String", "primary_key": True},
      {"name": "station", "type": "String", "primary_key": True},
      {"name": "c_date", "type": "Date", "primary_key": True},
      {"name": "ar_time_diff", "type": "String"},
      {"name": "dp_time_diff", "type": "String"}
    ]
  }
}
