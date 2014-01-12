import subprocess

class SlurmLib():
    def __init__(self):
        self._squeue = "squeue"
        self._username = "root"

    def start_count(self):
        _command = ("%s --noheader -o '%%i|%%T|%%u|%%U|%%r|%%R'" % self._squeue)
        #log.debug("Running `%s`...", _command)
        #log.debug("Computing updated values for total/available slots ...")
        proc = subprocess.Popen(["squeue", "--noheader", "-o", "'%%i|%%T|%%u|%%U|%%r|%%R'"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        (total_running, self.queued, self.user_run, self.user_queued) = count_jobs(stdout, self._username)

def count_jobs(squeue_output, whoami):
    """
    Parse SLURM's ``squeue`` output and return a quadruple `(R, Q, r,
    q)` where:

    * `R` is the total number of running jobs (from any user);
    * `Q` is the total number of queued jobs (from any user);
    * `r` is the number of running jobs submitted by user `whoami`;
    * `q` is the number of queued jobs submitted by user `whoami`

    The `squeue_output` must contain the results of an invocation of
    ``squeue --noheader --format='%i:%T:%u:%U:%r:%R'``.
    """
    total_running = 0
    total_queued = 0
    own_running = 0
    own_queued = 0
    print squeue_output
    for line in squeue_output.split('\n'):
        if line == '':
            continue
        # the choice of format string makes it easy to parse squeue output
        print(line)
        jobid, state, username, uid, reason, nodelist = line.split('|')
        if state in ['RUNNING', 'COMPLETING']:
            total_running += 1
            if username == whoami:
                own_running += 1
        # XXX: State CONFIGURING is described in the squeue(1) man
        # page as "Job has been allocated resources, but are waiting
        # for them to become ready for use (e.g. booting).".  Should
        # it be classified as "running" instead?
        elif state in ['PENDING', 'CONFIGURING']:
            total_queued += 1
            if username == whoami:
                own_queued += 1
    print("total_running %d, total_queued %d, own_running %d, own_queued %d" % (total_running, total_queued, own_running, own_queued))
    return (total_running, total_queued, own_running, own_queued)

a = SlurmLib()
a.start_count()
