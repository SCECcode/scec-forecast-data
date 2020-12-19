import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'SCEC Forecast Admin': 'https://auth.globus.org/50b309c9-4223-11eb-8a64-0ece49b2bd8d',
    'SCEC Forecast Curator': 'https://auth.globus.org/e5e0880b-4222-11eb-8c49-0eb9d45bd5fd',
    'SCEC Forecast Writer': 'https://auth.globus.org/ebfd0f5d-4221-11eb-8826-0aecec13621f',
    'SCEC Forecast Reader': 'https://auth.globus.org/a060fd0b-3f13-11eb-85ca-0aecec13621f'
}

table_name = 'ERMrest_Group'

schema_name = 'public'

column_annotations = {'Owner': {}}

column_comment = {'Owner': 'Group that can update the record.'}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('ID', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('URL', em.builtin_types['text'],
                     ),
    em.Column.define('Display_Name', em.builtin_types['text'],
                     ),
    em.Column.define('Description', em.builtin_types['text'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

table_annotations = {}

table_comment = None

table_acls = {'delete': [], 'insert': [], 'select': [], 'update': [], 'enumerate': []}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'], constraint_names=[['public', 'ERMrest_Group_pkey']],
                  ),
    em.Key.define(['ID'], constraint_names=[['public', 'ERMrest_Group_ID_key']],
                  ),
    em.Key.define(
        ['Display_Name', 'Description', 'URL', 'ID'],
        constraint_names=[['public', 'Group_Compound_key']],
        comment='Compound key to ensure that columns sync up into Visible_Groups on update.',
    ),
]

fkey_defs = []

table_def = em.Table.define(
    table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system=True
)


def main(catalog, mode, replace=False, really=False):
    updater = CatalogUpdater(catalog)
    table_def['column_annotations'] = column_annotations
    table_def['column_comment'] = column_comment
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'forecast.derivacloud.org'
    catalog_id = 2
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
