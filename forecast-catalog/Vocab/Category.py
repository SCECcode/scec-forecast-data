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

table_name = 'Category'

schema_name = 'Vocab'

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
    'id': {
        chaise_tags.generated: None
    },
    'uri': {
        chaise_tags.generated: None
    },
    'name': {
        chaise_tags.display: {
            'name': 'Name'
        }
    },
    'description': {
        chaise_tags.display: {
            'name': 'Description'
        }
    },
    'synonyms': {
        chaise_tags.display: {
            'name': 'Synonyms'
        }
    },
    'Owner': {}
}

column_comment = {
    'id': 'The preferred Compact URI (CURIE) for this term.',
    'uri': 'The preferred URI for this term.',
    'name': 'The preferred human-readable name for this term.',
    'description': 'A longer human-readable description of this term.',
    'synonyms': 'Alternate human-readable names for this term.',
    'Owner': 'Group that can update the record.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'id',
        em.builtin_types['ermrest_curie'],
        nullok=False,
        default='CORE:{RID}',
        annotations=column_annotations['id'],
        comment=column_comment['id'],
    ),
    em.Column.define(
        'uri',
        em.builtin_types['ermrest_uri'],
        nullok=False,
        default='/id/{RID}',
        annotations=column_annotations['uri'],
        comment=column_comment['uri'],
    ),
    em.Column.define(
        'name',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['name'],
        comment=column_comment['name'],
    ),
    em.Column.define(
        'description',
        em.builtin_types['markdown'],
        nullok=False,
        annotations=column_annotations['description'],
        comment=column_comment['description'],
    ),
    em.Column.define(
        'synonyms',
        em.builtin_types['text[]'],
        annotations=column_annotations['synonyms'],
        comment=column_comment['synonyms'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        {
            'source': 'RID'
        }, {
            'source': 'name'
        }, {
            'source': 'description'
        }, {
            'source': 'synonyms'
        }, {
            'source': 'RCT'
        }, {
            'source': 'RMT'
        }, {
            'source': [{
                'outbound': ['Vocab', 'Category_RCB_fkey']
            }, 'ID']
        }, {
            'source': [{
                'outbound': ['Vocab', 'Category_RMB_fkey']
            }, 'ID']
        }, {
            'source': [{
                'outbound': ['Vocab', 'Category_Catalog_Group_fkey']
            }, 'ID']
        }
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'category'

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
    em.Key.define(['id'], constraint_names=[['Vocab', 'Category_idkey1']],
                  ),
    em.Key.define(['uri'], constraint_names=[['Vocab', 'Category_urikey1']],
                  ),
    em.Key.define(['RID'], constraint_names=[['Vocab', 'Category_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['Vocab', 'Category_Catalog_Group_fkey']],
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
        constraint_names=[['Vocab', 'Category_RCB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['Vocab', 'Category_RMB_fkey']],
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
