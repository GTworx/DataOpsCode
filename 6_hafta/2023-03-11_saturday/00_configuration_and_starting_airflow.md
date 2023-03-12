## Activate venv for airflow
```
source ~/venvairflow/bin/activate

airflow version

2.2.0
```

### Some important configurations
#### Before change configuration you must back up airflow.cfg
- dags_folder
- default_timezone
- executor
- sql_alchemy_conn

## Change dags list interval, Disable examples 
```
sed -i "s+dag_dir_list_interval = 300+dag_dir_list_interval = 5+g" venvairflow/airflow.cfg

sed -i "s+load_examples = True+load_examples = False+g" venvairflow/airflow.cfg
```

## Start Airflow
```
sudo systemctl start airflow
sudo systemctl start airflow-scheduler
```

- Wait 30 secs for the Airflow web server spin up.   
- Open browser http://127.0.0.1:1502 and see airflow web ui.   
- username: admin, password: admin  



