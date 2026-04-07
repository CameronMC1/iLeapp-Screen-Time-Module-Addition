__artifacts_v2__ = {
    "screentime_usage": {
        "name": "Screen Time - App Usage",
        "description": "Extracts app usage data from CoreDuet knowledgeC database",
        "author": "YourName",
        "version": "1.0",
        "date": "2026-04-02",
        "requirements": "none",
        "category": "Usage",
        "notes": "Parses CoreDuet knowledgeC.db for app usage activity",
        "paths": ('*/CoreDuet/Knowledge/knowledgeC.db',),
        "output_types": "all",
        "artifact_icon": "clock"
    }
}

import sqlite3
from scripts.ilapfuncs import artifact_processor, open_sqlite_db_readonly

@artifact_processor
def screentime_usage(files_found, report_folder, seeker, wrap_text, timezone_offset):
    data_list = []
    source_path = ''

    for file_found in files_found:
        source_path = str(file_found)

        try:
            conn = open_sqlite_db_readonly(file_found)
            cursor = conn.cursor()

            query = """
            SELECT
                ZOBJECT.ZSTARTDATE,
                ZOBJECT.ZENDDATE,
                ZOBJECT.ZVALUESTRING,
                ZOBJECT.ZSECONDSFROMGMT
            FROM ZOBJECT
            WHERE ZOBJECT.ZSTREAMNAME = '/app/usage'
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            for row in rows:
                start = row[0]
                end = row[1]
                app = row[2]
                tz = row[3]

                duration = None
                if start and end:
                    duration = end - start

                data_list.append((
                    app,
                    start,
                    end,
                    duration,
                    tz
                ))

            conn.close()

        except Exception as e:
            print(f"Error processing {file_found}: {e}")

    data_headers = (
        'App Bundle ID',
        'Start Time',
        'End Time',
        'Duration (seconds)',
        'Timezone Offset'
    )

    return data_headers, data_list, source_path