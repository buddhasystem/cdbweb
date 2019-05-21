# ---
PAGECHOICES	= [('25','25'),   ('50','50'),   ('100','100'),
                   ('200','200'), ('400','400'), ('800','800'),]

GTSTATUSCHOICES	= [('All','All'), ('NEW','New'), ('PUBLISHED','Published'), ('INVALID','Invalid'),]

GTTYPECHOICES	= [('All','All'), ('RELEASE','Release'), ('DEV','Dev'),]

# ---
GTCOMPCHOICES	= [
    ('sidebyside',	'Display side by side'),
    ('diff',		'Diff (terse, skip matching payloads)'),
    ('fulldiff',	'Full Diff (verbose, list matching payloads)'),
    ('runexp',		'Limit by exp and run'),
]

GTCOMPTEMPLATES = {
    'sidebyside':'gtcompare.html',
    'diff':'gtdiff.html',
    'fulldiff':'gtdiff.html',
    'runexp':'gtcompare.html',
    }

# ---
EXCLUDE_SELECTORS = {
    'Payload':('ID',),
    }

# ---
EXCLUDE_COLUMNS = {
   'GlobalTagPayload':	{
        'pk':	('global_tag_payload_id',),
    },
    'GlobalTag':	{
        'all':	('dtm_ins', 'numberOfGlobalTagPayloads', 'basf2modules')
    },
    'Payload':		{
        'all':	('payload_id', 'payload_url', 'dtm_ins', 'dtm_mod', 'iov',),
        'pk':	('payload_url',),
    },
}
