import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args
from deriva.core import tag as chaise_tags
import deriva.core.ermrest_model as em

groups = {
    'SCEC Forecast Admin': 'https://auth.globus.org/50b309c9-4223-11eb-8a64-0ece49b2bd8d',
    'SCEC Forecast Curator': 'https://auth.globus.org/e5e0880b-4222-11eb-8c49-0eb9d45bd5fd',
    'SCEC Forecast Writer': 'https://auth.globus.org/ebfd0f5d-4221-11eb-8826-0aecec13621f',
    'SCEC Forecast Reader': 'https://auth.globus.org/a060fd0b-3f13-11eb-85ca-0aecec13621f'
}

annotations = {
    'tag:isrd.isi.edu,2019:catalog-config': {
        'name': 'core',
        'groups': {
            'admin': 'https://auth.globus.org/50b309c9-4223-11eb-8a64-0ece49b2bd8d',
            'reader': 'https://auth.globus.org/a060fd0b-3f13-11eb-85ca-0aecec13621f',
            'writer': 'https://auth.globus.org/ebfd0f5d-4221-11eb-8826-0aecec13621f',
            'curator': 'https://auth.globus.org/e5e0880b-4222-11eb-8c49-0eb9d45bd5fd'
        }
    },
}

acls = {
    'insert': [groups['SCEC Forecast Curator'], groups['SCEC Forecast Writer']],
    'create': [groups['SCEC Forecast Writer']],
    'enumerate': ['*'],
    'update': [groups['SCEC Forecast Curator']],
    'owner': [
        groups['SCEC Forecast Admin'],
        'https://auth.globus.org/aef862ea-d274-11e5-bb09-7bf5b06f98da'
    ],
    'delete': [groups['SCEC Forecast Curator']],
    'write': [],
    'select': [groups['SCEC Forecast Writer'], groups['SCEC Forecast Reader']]
}


def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_catalog(mode, annotations, acls, replace=replace)


if __name__ == "__main__":
    host = 'forecast.derivacloud.org'
    catalog_id = 2
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_catalog=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
