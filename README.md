# constructure-single-node

Useful developer command on mac when coding with chinese characters, which has its own ',' ';' etc.

pcregrep --color='auto' -n '[^\x00-\x7F]' whole.sql


DESIGN:

REST API -- look aside cache only for matching scores (cache.sql)
         -- db (whole.sql)
