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

table_name = 'Page_Asset'

schema_name = 'WWW'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'name': 'Created By'
        }
    },
    'RMB': {
        chaise_tags.display: {
            'name': 'Modified By'
        }
    },
    'Page_RID': {},
    'URL': {
        chaise_tags.asset: {
            'md5': 'MD5',
            'url_pattern': '/hatrac/WWW/Page_Asset/{{{Page_RID}}}/{{{_URL.filename}}}',
            'filename_column': 'Filename',
            'byte_count_column': 'Length'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'
            }
        }
    },
    'Filename': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'
            }
        }
    },
    'Content_Type': {},
    'Length': {},
    'Owner': {}
}

column_comment = {
    'Page_RID': 'The Page entry to which this asset is attached',
    'Content_Type': 'Content type of the asset',
    'Length': 'Asset length (bytes)',
    'Owner': 'Group that can update the record.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'Page_RID', em.builtin_types['text'], nullok=False, comment=column_comment['Page_RID'],
    ),
    em.Column.define(
        'URL', em.builtin_types['text'], nullok=False, annotations=column_annotations['URL'],
    ),
    em.Column.define(
        'Filename', em.builtin_types['text'], annotations=column_annotations['Filename'],
    ),
    em.Column.define(
        'Content_Type', em.builtin_types['text'], comment=column_comment['Content_Type'],
    ),
    em.Column.define('Description', em.builtin_types['markdown'],
                     ),
    em.Column.define(
        'Length', em.builtin_types['int8'], nullok=False, comment=column_comment['Length'],
    ),
    em.Column.define('MD5', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

table_display = {'row_name': {'row_markdown_pattern': '{{{Filename}}}'}}

table_annotations = {chaise_tags.table_display: table_display, }

table_comment = 'Asset table for Page'

table_acls = {}

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
    em.Key.define(['RID'], constraint_names=[['WWW', 'Page_Asset_RIDkey1']],
                  ),
    em.Key.define(
        ['Filename'],
        constraint_names=[['WWW', 'Page_Asset_Filename_key']],
        comment='Key constraint to ensure file names in the table are unique',
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Page_RID'],
        'WWW',
        'Page', ['RID'],
        constraint_names=[['WWW', 'Page_Asset_Page_fkey']],
        acls={
            'insert': [groups['SCEC Forecast Curator']],
            'update': [groups['SCEC Forecast Curator']]
        },
        acl_bindings={
            'self_linkage_owner': {
                'types': ['insert', 'update'],
                'scope_acl': ['*'],
                'projection': ['Owner'],
                'projection_type': 'acl'
            },
            'self_linkage_creator': {
                'types': ['insert', 'update'],
                'scope_acl': ['*'],
                'projection': ['RCB'],
                'projection_type': 'acl'
            }
        },
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['WWW', 'Page_Asset_Catalog_Group_fkey']],
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
        constraint_names=[['WWW', 'Page_Asset_RCB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['WWW', 'Page_Asset_RMB_fkey']],
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
