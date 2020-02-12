import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

main_pool = config.get('perf_tests', 'main_pool')
# zfs filesystems start with a pool name and have their paths seperated by
# forward slashes
test_filesystem_path = main_pool + '/' + config.get('perf_tests', 'test_filesystem')

# This will be the full path to the file that will be zfs received during the
# tests.
test_file_full_path = config.get('perf_tests', 'test_file')

# The directory the tests will occur in.
mount_point = config.get('perf_tests', 'mount_point')

# The directory to place logs in.
log_directory = config.get('perf_tests', 'log_directory')

# The directory to put starting and ending results in
results_directory = config.get('perf_tests', 'results_directory')

# The directory for runnings system statistics during a run
stats_directory = config.get('perf_tests', 'stats_directory')

