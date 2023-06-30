import pytest

from airflow.models import DagBag

from contextlib import contextmanager

@contextmanager
def not_raises(ExpectedException):
    try:
        yield

    except ExpectedException as err:
        raise AssertionError(
            "Did raise exception {0} when it should not!".format(
                repr(ExpectedException)
            )
        )

    except Exception as err:
        raise AssertionError(
            "An unexpected exception {0} raised.".format(repr(err))
        )


def test_dag_loaded():
    with not_raises(AssertionError):
        from dags import my_example
    
    dag_bag = DagBag("./dags", include_examples=False)
    dag = dag_bag.get_dag(dag_id="my_example")
    assert dag is not None
    assert len(dag.tasks) == 3
    assert dag_bag.import_errors == {}
