set search_path = views, public;

drop view if exists contracts_summary;
drop table if exists contracts_summary_no_data;
drop table if exists contract_implementation_transactions_summary;
drop table if exists contract_implementation_milestones_summary;
drop table if exists contract_implementation_documents_summary;
drop table if exists contract_milestones_summary;
drop table if exists contract_documents_summary;
drop table if exists contract_items_summary;
