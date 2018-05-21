rm -rf test.db
cat ../src/sql/whole.sql | sqlite3 test.db
cat ../src/sql/test/test.sql | sqlite3 test.db
