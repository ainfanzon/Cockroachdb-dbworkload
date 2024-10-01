import datetime as dt
import psycopg
import random
import time
import uuid


class Northwind:
    def __init__(self, args: dict):
        # args is a dict of string passed with the --args flag
        # user passed a yaml/json, in python that's a dict object

        self.read_pct: float = float(args.get("read_pct", 50) / 100)

        self.lane: str = (
            random.choice(["ACH", "DEPO", "WIRE"])
            if not args.get("lane", "")
            else args["lane"]
        )

        # you can arbitrarely add any variables you want
        self.uuid: uuid.UUID = uuid.uuid4()
        self.ts: dt.datetime = ""
        self.event: str = ""

    # the setup() function is executed only once
    # when a new executing thread is started.
    # Also, the function is a vector to receive the excuting threads's unique id and the total thread count
    def setup(self, conn: psycopg.Connection, id: int, total_thread_count: int):
        with conn.cursor() as cur:
            print(
                f"My thread ID is {id}. The total count of threads is {total_thread_count}"
            )
            print(cur.execute(f"select version()").fetchone()[0])

    # the run() function returns a list of functions
    # that dbworkload will execute, sequentially.
    # Once every func has been executed, run() is re-evaluated.
    # This process continues until dbworkload exits.
    def loop(self):
        if random.random() < self.read_pct:
            return [self.read]
        # return [self.txn_01, self.txn_02, self.txn_03]
        return [self.txn_01, self.txn_02]

    # conn is an instance of a psycopg connection object
    # conn is set by default with autocommit=True, so no need to send a commit message
    def read(self, conn: psycopg.Connection):
        with conn.cursor() as cur:
            cur.execute(
                "SELECT contact_name, company_name, contact_title, phone From customers WHERE customer_id = 'HUNGC'"
            )
            cur.fetchone()

    def txn_01(self, conn: psycopg.Connection):
        # simulate microservice doing something
        self.uuid = uuid.uuid4()
        self.ts = dt.datetime.now()
        self.event = 0
        self.contact_nm = "%MANAGER%"

        # make sure you pass the arguments in this fashion
        # so the statement can be PREPAREd (extended protocol).

        # Simple SQL strings will use the Simple Protocol.
        # error_type=TypeError, msg=query parameters should be a sequence or a mapping, got str
        with conn.cursor() as cur:
            stmt = """
                "SELECT contact_name FROM customers WHERE UPPER(contact_title) LIKE '%MANAGER%' ORDER BY contact_name LIMIT 10
                """
            #cur.execute(stmt, (self.contact_nm))

    # example on how to create a transaction with multiple queries
    def txn_02(self, conn: psycopg.Connection):
        # all queries sent within 'tx' will commit only when tx is exited
        with conn.transaction() as tx:
            with conn.cursor() as cur:
                # as we're inside 'tx', the below will not autocommit
                cur.execute(
                    "SELECT contact_name, company_name, contact_title, phone From customers WHERE customer_id = 'HUNGC'",
                )
                cur.fetchone()

                # simulate microservice doing something
                time.sleep(0.01)
                self.ts = dt.datetime.now()
                self.event = 1

                stmt = """
                    insert into transactions values (%s, %s, %s, %s);
                    """
                # as we're inside 'tx', the below will not autocommit
                cur.execute(stmt, (self.lane, self.uuid, self.event, self.ts))

    def txn_03(self, conn: psycopg.Connection):
        with conn.transaction() as tx:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT p.product_name, SUM(od.unit_price * CAST(od.quantity AS FLOAT) * (1.0 - od.discount)) AS Sales FROM products AS p INNER JOIN order_details AS od ON od.product_id = p.product_id GROUP BY p.product_name ORDER BY Sales DESC LIMIT 5",
                )
                cur.fetchone()

                # simulate microservice doing something
                self.ts = dt.datetime.now()
                self.event = 2
                time.sleep(0.01)

                stmt = """
                    insert into transactions values (%s, %s, %s, %s);
                    """
                cur.execute(stmt, (self.lane, self.uuid, self.event, self.ts))
