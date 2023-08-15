try:
    raise Exception("Hello world")
except Exception as ex:
    print(str(ex))