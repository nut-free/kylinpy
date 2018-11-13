# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pprint import pprint

from sqlalchemy import create_engine, inspect


kylin = create_engine('kylin://ADMIN:KYLIN@sandbox/learn_kylin')
pprint(kylin.table_names())

insp = inspect(kylin)
pprint(insp.get_columns('DEFAULT.KYLIN_SALES'))
pprint(insp.get_schema_names())

sql1 = """
SELECT KYLIN_SALES.OPS_USER_ID AS "KYLIN_SALES.OPS_USER_ID",
       COUNT (1) AS "TRANS_CNT"
FROM "DEFAULT"."KYLIN_SALES" AS "KYLIN_SALES"
JOIN "DEFAULT"."KYLIN_CAL_DT" AS "KYLIN_CAL_DT" ON KYLIN_SALES.PART_DT = KYLIN_CAL_DT.CAL_DT
JOIN "DEFAULT"."KYLIN_CATEGORY_GROUPINGS" AS "KYLIN_CATEGORY_GROUPINGS" ON KYLIN_SALES.LEAF_CATEG_ID = KYLIN_CATEGORY_GROUPINGS.LEAF_CATEG_ID
AND KYLIN_SALES.LSTG_SITE_ID = KYLIN_CATEGORY_GROUPINGS.SITE_ID
JOIN "DEFAULT"."KYLIN_ACCOUNT" AS "BUYER_ACCOUNT" ON KYLIN_SALES.BUYER_ID = BUYER_ACCOUNT.ACCOUNT_ID
JOIN "DEFAULT"."KYLIN_ACCOUNT" AS "SELLER_ACCOUNT" ON KYLIN_SALES.SELLER_ID = SELLER_ACCOUNT.ACCOUNT_ID
JOIN "DEFAULT"."KYLIN_COUNTRY" AS "BUYER_COUNTRY" ON BUYER_ACCOUNT.ACCOUNT_COUNTRY = BUYER_COUNTRY.COUNTRY
JOIN "DEFAULT"."KYLIN_COUNTRY" AS "SELLER_COUNTRY" ON SELLER_ACCOUNT.ACCOUNT_COUNTRY = SELLER_COUNTRY.COUNTRY
WHERE KYLIN_CAL_DT.YEAR_BEG_DT >= CAST('2018-11-08' AS DATE)
  AND KYLIN_CAL_DT.YEAR_BEG_DT <= CAST('2018-11-09' AS DATE)
GROUP BY KYLIN_SALES.OPS_USER_ID
ORDER BY "TRANS_CNT" DESC
LIMIT 10000;
"""  # noqa

sql2 = """
SELECT * FROM KYLIN_SALES LIMIT 10
"""

rp = kylin.execute(sql1)
pprint(rp.fetchall())
