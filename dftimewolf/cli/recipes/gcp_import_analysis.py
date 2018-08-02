"""A dftimewolf recipe for responding to GCP incidents.

This recipe will copy disks from remote projects into our forensics project and
create an analysis VM to analyze it with the disk attached.

Disks of interest can either be specified in multiple ways:

  --disk_names will copy specific disks in project, regardless of the instance
        they're attached to.
  --instance will copy the instance's boot disk.
  --instance combined with --all_disks will copy all disks attached to a
        specific instance

Sample usage

To copy the boot disk of "owned-instance" in "owned project":

  $ dftimewolf gcp_import_analysis owned-project --instance owned-instance

To copy "disk1" and "disk2" in "owned-project":

  $ dftimewolf gcp_import_analysis owned-project --disks=disk1,disk2

To copy all disks attached to "myinstance" in "myproject":

  $ dftimewolf gcp_import_analysis myproject --instance myinstance \
      --all_disks=True
"""

from __future__ import unicode_literals
from datetime import datetime

contents = {
    'name':
        'gcp_import_analysis',
    'short_description': 'Copies disk from a GCP project to an analysis VM.',
    'modules': [{
        'name': 'GoogleCloudCollector',
        'args': {
            'analysis_project_name': '@analysis_project_name',
            'remote_project_name': '@remote_project_name',
            'remote_instance_name': '@instance',
            'incident_id': '@incident_id',
            'zone': '@zone',
            'disk_names': '@disks',
            'all_disks': '@all_disks',
            'boot_disk_size': '@boot_disk_size',
        },
    }]
}

args = [
    ('remote_project_name',
     'Name of the project containing the instance / disks to copy ', None),
    ('--incident_id', 'The Incident ID on which the name of the analysis VM '
     'will be based', datetime.now().strftime("%Y%m%d%H%M%S")),
    ('--instance', 'Name of the instance to analyze.', None),
    ('--disks', 'Comma-separated list of disks to copy.', None),
    ('--all_disks', 'Copy all disks in the designated instance. '
                    'Overrides disk_names if specified', False),
    ('--analysis_project_name', 'Name of the project where the analysis VM will'
                                ' be created', None),
    ('--boot_disk_size', 'The size of the analysis VM boot disk (in GB)', 50.0),
    ('--zone', 'The GCP zone the forensics project is in', None),
]
