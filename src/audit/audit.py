from sqlalchemy import text
from datetime import datetime
from src.database.connection import get_engine

# Pipeline
def start_pipeline(pipeline_name: str):

    engine = get_engine()

    with engine.begin() as conn:

        run_id = conn.execute(
            text("""
                INSERT INTO audit.etl_runs (
                    pipeline_name,
                    start_time,
                    status
                )

                VALUES (
                    :pipeline_name,
                    :start_time,
                    'RUNNING'
                )

                RETURNING run_id
            """),
            {
                "pipeline_name": pipeline_name,
                "start_time": datetime.now()
            }
        ).scalar_one()

    return run_id


def finish_pipeline(run_id):

    engine = get_engine()

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE audit.etl_runs

                SET
                    end_time = :end_time,
                    duration_seconds =
                        EXTRACT(
                            EPOCH FROM (:end_time - start_time)
                        ),
                    status = 'SUCCESS'

                WHERE run_id = :run_id
            """),
            {
                "run_id": run_id,
                "end_time": datetime.now()
            }
        )


def fail_pipeline(run_id, error_message):

    engine = get_engine()

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE audit.etl_runs

                SET
                    end_time = :end_time,
                    duration_seconds =
                        EXTRACT(
                            EPOCH FROM (:end_time - start_time)
                        ),
                    status = 'FAILED',
                    error_message = :error

                WHERE run_id = :run_id
            """),
            {
                "run_id": run_id,
                "end_time": datetime.now(),
                "error": str(error_message)
            }
        )

# Steps
def start_step(run_id, step_name):
    engine = get_engine()

    with engine.begin() as conn:

        step_id = conn.execute(
            text("""
                INSERT INTO audit.etl_steps (
                    run_id,
                    step_name,
                    start_time,
                    status
                )

                VALUES (
                    :run_id,
                    :step_name,
                    :start_time,
                    'RUNNING'
                )

                RETURNING step_id
            """),
            {
                "run_id": run_id,
                "step_name": step_name,
                "start_time": datetime.now()
            }
        ).scalar_one()

    return step_id

def finish_step(step_id, rows_loaded):
    engine = get_engine()

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE audit.etl_steps

                SET
                    end_time = :end_time,
                    duration_seconds =
                        EXTRACT(EPOCH FROM (:end_time - start_time)),
                    rows_loaded = :rows_loaded,
                    status = 'SUCCESS'

                WHERE step_id = :step_id
            """),
            {
                "step_id": step_id,
                "rows_loaded": rows_loaded,
                "end_time": datetime.now()
            }
        )

def fail_step(step_id, error):
    engine = get_engine()

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE audit.etl_steps

                SET
                    end_time = :end_time,
                    duration_seconds =
                        EXTRACT(EPOCH FROM (:end_time - start_time)),
                    status = 'FAILED',
                    error_message = :error_message

                WHERE step_id = :step_id
            """),
            {
                "step_id": step_id,
                "end_time": datetime.now(),
                "error_message": str(error)
            }
        )