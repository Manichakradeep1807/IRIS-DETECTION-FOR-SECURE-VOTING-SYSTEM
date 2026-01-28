"""
Processes pending user-to-person link tasks created during registration staging.
Safe to run at startup; retries linking and records outcomes.
"""

from typing import Optional

try:
    from registration_db import regdb
    from database_manager import db
except Exception:
    regdb = None
    db = None


def run_link_repair(max_items: int = 50) -> int:
    if regdb is None or db is None:
        return 0
    processed = 0
    try:
        pending = regdb.list_pending()
        for item in pending[:max_items]:
            try:
                username = item.get('username')
                person_id = int(item.get('id'))  # fixed to use 'id'
                ok = db.link_user_to_person(username, person_id)
                if ok:
                    regdb.mark_linked(int(item.get('id')))
                else:
                    regdb.mark_error(int(item.get('id')), 'update returned 0 rows')
                processed += 1
            except Exception as e:
                try:
                    regdb.mark_error(int(item.get('id')), str(e))
                except Exception:
                    pass
    except Exception:
        return processed
    return processed


if __name__ == '__main__':
    n = run_link_repair()
    print('Link repair processed', n)

















