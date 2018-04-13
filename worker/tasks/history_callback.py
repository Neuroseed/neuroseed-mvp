import time
from keras import callbacks

SAVE_METRICS_ON_BATCH = False
UPDATE_ON_BATCH_N = 10


class HistoryCallback(callbacks.Callback):

    def __init__(self, task, epochs, batches_in_epoch, examples,
                 save_metrics_on_batch=SAVE_METRICS_ON_BATCH, update_on_batch_n=UPDATE_ON_BATCH_N):
        super().__init__()

        self._task = task
        self.batches_in_epoch = batches_in_epoch

        #task.history['batch'] = {}
        task.history['epoch'] = {}

        task.history['epochs'] = epochs
        task.history['current_epoch'] = 0

        self.batches = int(batches_in_epoch * epochs)
        task.history['batches'] = self.batches
        task.history['current_batch'] = 0

        task.history['batches_in_epoch'] = batches_in_epoch
        task.history['current_batch_in_epoch'] = 0

        self.examples = examples
        task.history['examples'] = examples
        task.history['current_example'] = 0

        self.save_metrics_on_batch = save_metrics_on_batch
        self.update_on_batch_n = update_on_batch_n

        task.save()

    @property
    def task(self):
        return self._task

    def on_batch_end(self, batch, logs=None):
        if self.save_metrics_on_batch:
            del logs['batch']  # delete batch number
            del logs['size']  # delete batch size
            logs['time'] = round(time.time(), 3)  # add current time

            batch_history = self.task.history['batch']

            for key in logs:
                history = batch_history.setdefault(key, [])
                value = float(logs[key])
                history.append(value)

        if batch % self.update_on_batch_n == 0:
            with self.task.save_context():
                self.task.history['current_batch_in_epoch'] = batch
                self.task.history['current_example'] = int(batch / self.batches_in_epoch * self.examples)

                current_epoch = self.task.history['current_epoch']
                batch = (current_epoch - 1) * self.batches_in_epoch + batch

                self.task.history['current_batch'] = batch

    def on_epoch_begin(self, epoch, logs=None):
        self.task.history['current_epoch'] = epoch + 1
        self.task.history['current_batch'] = 0
        self.task.history['current_batch_in_epoch'] = 0
        self.task.history['current_example'] = 0

        self.task.save()

    def on_epoch_end(self, epoch, logs=None):
        logs['time'] = round(time.time(), 3)  # add current time

        epoch_history = self.task.history['epoch']

        for key in logs:
            history = epoch_history.setdefault(key, [])
            value = float(logs[key])
            history.append(value)

        self.task.history['current_epoch'] = epoch + 1
        self.task.history['current_batch'] = self.batches_in_epoch * (epoch + 1)
        self.task.history['current_batch_in_epoch'] = self.batches_in_epoch
        self.task.history['current_example'] = self.task.history['examples']

        self.task.save()

    def on_train_end(self, logs=None):
        pass
