
class BaseUploader():
    def __init__(self):
        pass

    def __str__(self):
        return repr(self)

    def upload(self, image):
        raise NotImplementedError()

if __name__ == '__main__':
    b = BaseUploader()
    print(b)
