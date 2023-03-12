## List dags
```commandline
airflow dags list
```
- Sample output
```commandline
dag_id                          | filepath                           | owner | paused
================================+====================================+=======+=======
file_processing_with_python_dag | file_processing_with_python_dag.py | train | True  
ingest_data_dag                 | ingest_data_dag.py                 | train | True  
my_dag                          | my_dag.py                          | train | True  
postgresql_op_dag               | postgresql_op_dag.py               | train | True  
python_branch_dag               | python_branch_dag.py               | train | True  
simple_dag                      | simple_dag.py                      | train | True
```
## Pause dag


## Test dag 
```commandline
airflow dags test file_processing_with_python_dag 2023-03-08
```
## Delete dag

