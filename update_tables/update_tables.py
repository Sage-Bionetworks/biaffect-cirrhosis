import argparse
import synapseclient as sc
import synapsebridgehelpers

TABLE_MAPPING = {
        "syn12279831": "syn18632066",
        "syn17015193": "syn18632065",
        "syn8261527": "syn18632064",
        "syn7841519": "syn18632063",
        "syn7860696": "syn18632062",
        "syn7841520": "syn18632061"}
SOURCE_PROJECT = "syn7838471"


def get_relevant_healthcodes(syn):
    relevant_healthcodes = syn.tableQuery(
            "SELECT distinct healthCode FROM syn7841519 "
            "where substudyMemberships like '%Cirrhosis_pilot%'").asDataFrame()
    relevant_healthcodes = list(relevant_healthcodes.healthCode)
    return(relevant_healthcodes)


def verify_no_new_table_versions(syn):
    new_table_names_and_versions = [
            "birth-gender-v5", "Diagnosis-v4", "biaffect-keyboard-v2",
            "biaffect-appVersion-v2", "biaffect-MDQ-v2", "biaffect-KeyboardSession-v3"]
    source_tables = syn.getChildren(SOURCE_PROJECT, includeTypes=['table'])
    source_table_names = [t['name'] for t in source_tables]
    prohibited_tables = [table_name in source_table_names
            for table_name in new_table_names_and_versions]
    if any(prohibited_tables):
        prohibited_table_names = [
                n[0] for n in zip(new_table_names_and_versions, prohibited_tables)
                if n[1]]
        error_message = "Found an unexpected table(s): {}".format(
                    ", ".join(prohibited_table_names))
        syn.sendMessage([syn.getUserProfile()['ownerId']],
                        "New BiAffect Table Detected",
                        error_message)
        raise sc.exceptions.SynapseHTTPError(error_message)

def main():
    syn = sc.login()
    verify_no_new_table_versions(syn)
    relevant_healthcodes = get_relevant_healthcodes(syn)
    synapsebridgehelpers.export_tables(
            syn = syn,
            table_mapping = TABLE_MAPPING,
            identifier_col = "healthCode",
            identifier = relevant_healthcodes)


if __name__ == "__main__":
    main()
