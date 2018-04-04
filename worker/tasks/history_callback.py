import time
from keras import callbacks


class HistoryCallback(callbacks.Callback):
    UPDATE_ON_BATCH = 10

    def __init__(self, task, epochs, batches_in_epoch):
        super().__init__()

        self._task = task
        self.batches_in_epoch = batches_in_epoch

        task.history['batch'] = {}
        task.history['epoch'] = {}

        task.history['epochs'] = epochs
        task.history['current_epoch'] = 0

        task.history['batches'] = batches_in_epoch * epochs
        task.history['current_batch'] = 0

        task.history['batches_in_epoch'] = batches_in_epoch
        task.history['current_batch_in_epoch'] = 0

        task.save()

    @property
    def task(self):
        return self._task

    def on_batch_end(self, batch, logs=None):
        del logs['batch']  # delete batch number
        del logs['size']  # delete batch size
        logs['time'] = round(time.time(), 3)  # add current time

        batch_history = self.task.history['batch']

        for key in logs:
            history = batch_history.setdefault(key, [])
            value = float(logs[key])
            history.append(value)

        self.task.history['current_batch_in_epoch'] = batch

        current_epoch = self.task.history['current_epoch']
        batch = (current_epoch - 1) * self.batches_in_epoch + batch
        self.task.history['current_batch'] = batch

        if batch % self.UPDATE_ON_BATCH == 0:
            self.task.save()

    def on_epoch_begin(self, epoch, logs=None):
        self.task.history['current_epoch'] = epoch + 1
        self.task.history['current_batch'] = 0
        self.task.history['current_batch_in_epoch'] = 0

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

        self.task.save()

    def on_train_end(self, logs=None):
        pass
