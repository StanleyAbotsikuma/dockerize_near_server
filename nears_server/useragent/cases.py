class MyArray:
    _instance = None
    _data = []
    _observers = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get(self, index):
        return self._data[index]

    def set(self, index, value):
        self._data[index] = value
        self._notify_observers()

    def append(self, value):
        self._data.append(value)
        self._notify_observers()

    def pop(self, index=None):
        value = self._data.pop(index)
        self._notify_observers()
        return value

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def _notify_observers(self):
        for observer in self._observers:
            observer.notify(self._data)
            
            
            
#             from myapp.array import MyArray

# def my_view(request):
#     my_array = MyArray()
#     my_array.append('some value')
#     my_value = my_array.get(0)
#     return HttpResponse(my_value)