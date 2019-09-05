import argparse
import synapseclient as sc
import synapsebridgehelpers
import os

TABLE_MAPPING = {
        "syn17013485": "syn20710066", # Engagement-v1
        "syn16995608": "syn20710068", # PassiveDisplacement-v4
        "syn15673384": "syn20710073", # Medication-v3
        "syn15673383": "syn20710076", # StudyBurst-v1
        "syn15673382": "syn20710082", # Triggers-v3
        "syn15673381": "syn20710088", # Tapping-v4
        "syn15673380": "syn20710096", # Symptoms-v3
        "syn15673379": "syn20710101", # Demographics-v1
        "syn15673377": "syn20710110", # StudyBurstReminder-v1
        "syn15664831": "syn20710115", # Motivation-v1
        "syn12977322": "syn20710117", # Tremor-v3
        "syn12514611": "syn20710119", # WalkAndBalance-v1
        "syn12492996": "syn20710121", # Health Data Summary Table
        "syn17022539": "syn20712220"} # PassiveGait-v1
SOURCE_PROJECT = "syn18691015"


def get_env_var_credentials():
    credentials = {}
    credentials['synapseUsername'] = os.getenv('synapseUsername')
    credentials['synapsePassword'] = os.getenv('synapsePassword')
    return credentials


def get_relevant_healthcodes(syn):
    relevant_healthcodes = syn.tableQuery(
            "SELECT distinct healthCode FROM syn12492996 "
            "where substudyMemberships like '%Udall-superusers%'").asDataFrame()
    relevant_healthcodes = list(relevant_healthcodes.healthCode)
    return(relevant_healthcodes)


def verify_no_new_table_versions(syn):
    new_table_names_and_versions = [
            "Engagement-v2", "PassiveDisplacement-v5", "Medication-v4",
            "StudyBurst-v2", "Triggers-v4", "Tapping-v5", "Symptoms-v4",
            "Demographics-v2", "StudyBurstReminder-v2", "Motivation-v2",
            "Tremor-v4", "WalkAndBalance-v2"]
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
    credentials = get_env_var_credentials()
    syn = sc.login(credentials["synapseUsername"],
                   credentials["synapsePassword"])
    verify_no_new_table_versions(syn)
    relevant_healthcodes = get_relevant_healthcodes(syn)
    synapsebridgehelpers.export_tables(
            syn = syn,
            table_mapping = TABLE_MAPPING,
            identifier_col = "healthCode",
            identifier = relevant_healthcodes)


if __name__ == "__main__":
    main()
