class ObjectHoldingTheValue:
    def __init__(self, initial_value=0):
        self._value = initial_value
        self._callbacks = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        old_value = self._value
        self._value = new_value
        self._notify_observers(old_value, new_value)

    def _notify_observers(self, old_value, new_value):
        for callback in self._callbacks:
            callback(old_value, new_value)

    def register_callback(self, callback):
        self._callbacks.append(callback)

def check_artists(old_value, new_value):
    if old_value != new_value:
        print("new artist")
    else:
        print ("same artist")

holder = ObjectHoldingTheValue()
holder.register_callback(check_artists)
holder.value = "Barac"  # nothing is printed
holder.value = "Barac"  # nothing is printed
holder.value = 700  # a message is printed

