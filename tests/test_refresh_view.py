import pytest
import sqlalchemy as sa

import ocdskingfisherprocess.config

from ocdskingfisherviews.cli import run_command


@pytest.fixture(scope='module')
def engine():
    config = ocdskingfisherprocess.config.Config()
    config.load_user_config()
    engine = sa.create_engine(config.database_uri)
    return engine


VIEWS_TABLES = {
    "award_documents_summary",
    "award_items_summary",
    "award_suppliers_summary",
    "awards_summary",
    "buyer_summary",
    "contract_documents_summary",
    "contract_implementation_documents_summary",
    "contract_implementation_milestones_summary",
    "contract_implementation_transactions_summary",
    "contract_items_summary",
    "contract_milestones_summary",
    "contracts_summary",
    "parties_summary",
    "planning_documents_summary",
    "planning_milestones_summary",
    "planning_summary",
    "procuringentity_summary",
    "release_summary",
    "tender_documents_summary",
    "tender_items_summary",
    "tender_milestones_summary",
    "tender_summary",
    "tenderers_summary"
}


def test_refresh_runs(engine):
    run_command(['refresh-views', '--remove'])
    run_command(['refresh-views'])
    get_current_tables_query = "select table_name from information_schema.tables where table_schema = 'views'"

    with engine.connect() as conn:
        results = conn.execute(get_current_tables_query)
        db_tables = {result['table_name'] for result in results}
        assert db_tables.issuperset(VIEWS_TABLES)

    run_command(['refresh-views', '--remove'])
    with engine.connect() as conn:
        results = conn.execute(get_current_tables_query)
        db_tables = {result['table_name'] for result in results}
        assert db_tables.isdisjoint(VIEWS_TABLES)


def test_field_count_runs(engine):
    run_command(['refresh-views', '--remove'])
    run_command(['field-counts', '--remove'])
    run_command(['refresh-views'])
    run_command(['field-counts'])
    get_current_tables_query = "select table_name from information_schema.tables where table_schema = 'views'"

    with engine.connect() as conn:
        results = conn.execute(get_current_tables_query)
        db_tables = {result['table_name'] for result in results}
        assert 'field_counts' in db_tables

    run_command(['refresh-views', '--remove'])
    run_command(['field-counts', '--remove'])

    with engine.connect() as conn:
        results = conn.execute(get_current_tables_query)
        db_tables = {result['table_name'] for result in results}
        assert 'field_counts' not in db_tables
