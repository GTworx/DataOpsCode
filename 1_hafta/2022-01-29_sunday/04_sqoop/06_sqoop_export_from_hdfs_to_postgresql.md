1. truncate target table churn
```
truncate table public.churn;
select * from public.churn  limit 5;
rownumber|customerid|surname|creditscore|geography|gender|age|tenure|balance|numofproducts|hascrcard|isactivemember|estimatedsalary|exited|
---------|----------|-------|-----------|---------|------|---|------|-------|-------------|---------|--------------|---------------|------|
```

2. Export
```
sqoop export --connect jdbc:postgresql://localhost/traindb  \
--driver org.postgresql.Driver \
--username train -password Ankara06 \
--export-dir /user/train/output_data/sqoop_import/churn \
-m 4 --table public.churn
```

3. Check postgresql
```
select  count(1) from public.churn;
count|
-----|
10000|
```