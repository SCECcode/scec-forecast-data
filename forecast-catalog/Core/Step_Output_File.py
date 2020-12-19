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

table_name = 'Step_Output_File'

schema_name = 'Core'

column_annotations = {
    'RCT': {
        chaise_tags.display: {
            'name': 'Creation Time'
        },
        chaise_tags.generated: None,
        chaise_tags.immutable: None
    },
    'RMT': {
        chaise_tags.display: {
            'name': 'Last Modified Time'
        },
        chaise_tags.generated: None,
        chaise_tags.immutable: None
    },
    'RCB': {
        chaise_tags.display: {
            'name': 'Created By'
        },
        chaise_tags.generated: None,
        chaise_tags.immutable: None
    },
    'RMB': {
        chaise_tags.display: {
            'name': 'Modified By'
        },
        chaise_tags.generated: None,
        chaise_tags.immutable: None
    },
    'Step_RID': {
        chaise_tags.display: {
            'name': 'Step'
        }
    },
    'File_RID': {
        chaise_tags.display: {
            'name': 'File'
        }
    },
    'Owner': {}
}

column_comment = {'Owner': 'Group that can update the record.'}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'Step_RID', em.builtin_types['text'], annotations=column_annotations['Step_RID'],
    ),
    em.Column.define(
        'File_RID', em.builtin_types['text'], annotations=column_annotations['File_RID'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        {
            'source': 'RID'
        }, {
            'source': [{
                'outbound': ['Core', 'Step_OutputFile_Mapping_Step_RID_fkey']
            }, 'RID']
        }, {
            'source': [{
                'outbound': ['Core', 'Step_OutputFile_Mapping_File_RID_fkey']
            }, 'RID']
        }, {
            'source': 'RCT'
        }, {
            'source': 'RMT'
        }, {
            'source': [{
                'outbound': ['Core', 'Step_Output_File_RCB_fkey']
            }, 'ID']
        }, {
            'source': [{
                'outbound': ['Core', 'Step_Output_File_RMB_fkey']
            }, 'ID']
        }, {
            'source': [{
                'outbound': ['Core', 'Step_Output_File_Catalog_Group_fkey']
            }, 'ID']
        }
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = None

table_acls = {
    'owner': [groups['SCEC Forecast Admin']],
    'write': [],
    'delete': [groups['SCEC Forecast Curator']],
    'insert': [groups['SCEC Forecast Curator'], groups['SCEC Forecast Writer']],
    'select': ['*'],
    'update': [groups['SCEC Forecast Curator']],
    'enumerate': ['*']
}

table_acl_bindings = {
    'self_service': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'projection_type': 'acl'
    },
    'self_service_group': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'projection_type': 'acl'
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(['RID'], constraint_names=[['Core', 'Step_Output_File_RIDkey1']],
                  ),
    em.Key.define(
        ['Step_RID', 'File_RID'],
        constraint_names=[['Core', 'Step_OutputFile_Mapping_RID_key']],
        comment='Step plus file must be distinct.',
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Step_RID'],
        'Core',
        'Step', ['RID'],
        constraint_names=[['Core', 'Step_OutputFile_Mapping_Step_RID_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['File_RID'],
        'Core',
        'File', ['RID'],
        constraint_names=[['Core', 'Step_OutputFile_Mapping_File_RID_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['Core', 'Step_Output_File_Catalog_Group_fkey']],
        acls={
            'insert': [groups['SCEC Forecast Curator']],
            'update': [groups['SCEC Forecast Curator']]
        },
        acl_bindings={
            'set_owner': {
                'types': ['update', 'insert'],
                'scope_acl': ['*'],
                'projection': ['ID'],
                'projection_type': 'acl'
            }
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['Core', 'Step_Output_File_RCB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['Core', 'Step_Output_File_RMB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
]

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
