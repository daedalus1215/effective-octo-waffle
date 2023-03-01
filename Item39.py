from threading import Thread
import os
import random

# Say we are writing a MapReduce implementation and we want common class to represent the input data.
# Can define a abstract class

class InputData:
    def read(self):
        raise NotImplementedError


class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        with open(self.path) as file:
            return file.read()


class Worker:
    def __init__(self, input_data):
        self.input_data = input_data;
        self.result = None

    def map(self):
        raise NotImplementedError

    def __reduce__(self):
        raise NotImplementedError


class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


# Create a factory to generate inputs and aggregate workers


def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


# Execute these workers by fanning out the map step to multiple threads
# Then we call reduce repeatedly to combine the results into one final value


def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, *rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result

# Finally connect all the pieces togeher in a function to run each step
def mapreduce(data_dir):
    return execute(create_workers(generate_inputs(data_dir)))

# Run the function on a set of test input files

def write_test_files(tmpdir):
    os.makedirs(tmpdir)
    for i in range (1000):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write('\n' * random.randint(0, 100))

tmpdir = 'test_inputs'
write_test_files(tmpdir)

result = mapreduce(tmpdir)
print(f'there are {result} lines')

# This is great, but the mapreduce func is not generic at all. If we wanted to write
# another inputdata or worker subclass, we would also have to rewrite the generate_inputs,
# create_workers, and mapreduce

# We cannot continue to use __init__, because of the issues with diamong inheritance to say the most extreme case
# We need to use the @classmethod, so we can create new InputData instances using a common interface
class GenericInputData2:
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputData2(GenericInputData2):
    def read(self):
        with open(self.path) as file:
            return file.read()

    @classmethod
    def generate_inputs(cls, config):
        print(f'gen_input, what is config: {config}')
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


# similarly, we can make the create_workers helper part of the GenericWorker class


class GenericWorker2:
    def map(self):
        raise NotImplementedError

    def __reduce__(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers

# Now all we need to do is change the dependency


class LineCountWorker2(GenericWorker2):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = 0

    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def mapreduce2(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)

print(f'There are {mapreduce2(worker_class=LineCountWorker2, input_class=PathInputData2, config={"data_dir": "test_inputs"})} lines')
