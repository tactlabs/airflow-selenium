
'''
Created on 

@author: raja csp.raman

source:
    https://stackoverflow.com/questions/71111635/airflow-2-0-task-getting-skipped-after-branchpython-operator
'''


from airflow.decorators import dag, task
from datetime import timedelta, datetime

from airflow.operators.python import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule

import logging
logger = logging.getLogger("airflow.task")

@dag(
    schedule_interval="0 0 * * *",
    start_date=datetime.today() - timedelta(days=2),
    dagrun_timeout=timedelta(minutes=60),
)
def StackOverflowExample():

    @task
    def task_A():

        logging.info("TASK A")
        

    @task
    def task_B():

        logging.info("TASK B")

    @task
    def task_C():

        logging.info("TASK C")

    @task
    def task_D():
        
        logging.info("TASK D")

        return {"parameter":0.5}

    
    def _choose_task(task_parameters,**kwargs):

        logging.info(task_parameters["parameter"])
        if task_parameters["parameter"]<0.5:
            logging.info("SUCCESSS ")
            return ['branch_1', 'task_final']
        else:
            logging.info("RIP")
            return ['branch_2', 'task_final']

    @task(task_id="branch_1")
    def branch_1():
        logging.info("branch_1...")

    @task(task_id="branch_2")
    def branch_2():
        logging.info("branch_2")

    @task(task_id="task_final")
    def task_final():
        logging.info("task_final")


    parameter = task_A() >> task_B() >> task_C() >> task_D()   

    choose_task = BranchPythonOperator(
                                            task_id='choose_best_model',
                                            op_kwargs={"task_parameters":parameter},
                                            python_callable=_choose_task,
                                            trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
                                            )



    choose_task >> [branch_1(), branch_2()] >> task_final()


dag = StackOverflowExample  ()