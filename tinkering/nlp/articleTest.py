#!/usr/bin/env python
from ifc.db import ArticleFeature, db

import logging
import peewee

db_data = ({'article': '1', 'negative': '0.2', 'neutral': '0.4', 'positive': '0.4', 'compound': '1'})
print db_data
try:
	with db.atomic():
		ArticleFeature.insert(db_data).execute()
except peewee.IntegrityError:
		logging.info('Skipping Duplicate')