import mesos

class SlurmExecutor(mesos.Executor):
    def __init__(self):
        print("Began init for Executor.")

    def registered(self, driver, executorInfo, frameworkInfo, slaveInfo):
        print ("Registered with Mesos slave.")
