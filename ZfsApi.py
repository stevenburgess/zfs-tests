import subprocess
import os
# A collection of zfs calls that can be stubed out

def fs_exists(zfs_receive_path):
    """Check if a zfs Filesytem already exists"""
    devnull = open(os.devnull, 'w')
    try:
        subprocess.check_call(['zfs', 'get', 'name', zfs_receive_path],
                stdout=devnull, stderr=devnull)
    except subprocess.CalledProcessError:
        return False
    return True

def zfs_recv(file_to_receive, desitnation_fs):
    """Receive the specified zfs send file to the destination fs"""
    subprocess.check_call('cat ' + file_to_receive + ' | zfs recv ' + desitnation_fs, shell=True)

def get_filesystem_properties(filesystem_name, property_set):
    """Given the name of a filesystem and a list of properties returns a
    dictionary of name value pairs"""
    # Not all properties are valid filesystem properties, some of them are
    # snapshot exclusive or the user could mistype. This section checks that
    # the requested properties exist, and are filesystem properties.
    file_system_proprties = frozenset(
            ['available','compressratio','creation','name',
            'mounted','origin','refcompressratio','referenced','type','used',
            'usedbychildren','usedbydataset','usedbyrefreservation',
            'usedbysnapshots','userrefs','written','aclinherit','atime',
            'canmount','casesensitivity','checksum','compression','copies',
            'dedup','devices','exec','logbias','mountpoint','normalization',
            'primarycache','quota','readonly','recordsize','refquota',
            'refreservation','reservation','secondarycache','setuid',
            'sharenfs','sharesmb','snapdir','sync','utf8only','version'])

    illegal_properties = frozenset(property_set) - file_system_proprties
    if illegal_properties:
        raise ValueError(illegal_properties)
    # -H strips the header, you do not need it since you know the order
    # -p gives you the exact values, so time in UNIX timestamps, size in bytes
    get_response = subprocess.check_output(
            ['zfs', 'get', '-Hp', ','.join(property_set), filesystem_name]).decode("utf-8")
    propery_dictionary = {}
    for line in get_response.splitlines():
        split_line = line.split()
        propery_dictionary[split_line[1]] = split_line[2]
    return propery_dictionary

def get_filesystem_size(filesystem_name):
    """Return the size of the named filesystem in bytes as an int"""
    propery_dictionary = get_filesystem_properties(filesystem_name, ['used'])
    return int(propery_dictionary['used'])

def snapshot_filesystem(filesystem_name, snapshot_name):
    """Snapshot a filesystem with a given name"""
    if not fs_exists(filesystem_name):
        raise ValueError(filesystem_name + " Does not exist")
    full_snapshot_name = filesystem_name + '@' + snapshot_name
    subprocess.check_call(['zfs', 'snapshot', full_snapshot_name])

def create_filesystem(file_system_path):
    """Creates a zfs filesystem. This function requires that its direct parent
    exists"""
    # Figure out if the parent file system exists
    final_slash = str.rfind(file_system_path, '/')
    parent_fs_name = file_system_path[:final_slash]
    if not fs_exists(parent_fs_name):
        raise ValueError("Parent filesystem does not exist for " 
                + file_system_path)
    subprocess.check_call(['zfs', 'create', file_system_path])

def get_current_txg(pool_name):
    """Get the current transaction group number for a given pool. Note that
    this call actually takes some time, since it actually reads from the
    disk"""
    get_response = subprocess.check_output(['zdb', '-u', pool_name]).decode("utf-8")
    for line in get_response.splitlines():
        if "txg" in line:
            # The line looks something like
            # |        txg = 7101599|
            # so there is a tab at the beginning, but thats not the part we are
            # looking at.
            return int(line.split(' ')[2])

def linux_get_current_txg(pool_name):
    """Gets the most recent transaction group number. Since the txg file is
    only 62 lines long, reading through the whole thing seems
    acceptable."""
    txg_file = '/proc/spl/kstat/zfs/txgs-' + pool_name
    txg_file_handle = open(txg_file, 'r')
    for line in txg_file_handle:
        last_line = line
    txg_file_handle.close()
    split_line = last_line.split(' ')
    current_txg = split_line[0]
    return int(current_txg)

def get_pool_name_for_fs(filesystem):
    """Filesystem names are / delimited lists of filesystems, where the text
    before the first / is the name of the zpool this FS belongs to."""
    if not '/' in filesystem:
        # This means the FS is the base FS made for the pool, and you do not
        # have to change anything to get its pool name
        return filesystem
    else:
        # If there is a / then it is a child filesystem, and we only want the
        # part prior to the first /
        return filesystem[:filesystem.find('/')]

def zpool_exists(pool_name):
    """Returns true of a pool by the input name is found on this system, false
    otherwise"""
    devnull = open(os.devnull, 'w')
    try:
        subprocess.check_call(['zpool', 'get', 'name', pool_name],
                stdout=devnull, stderr=devnull)
        return True
    except subprocess.CalledProcessError:
        return False

