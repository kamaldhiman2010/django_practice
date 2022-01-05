def print_msg(msg):
    def printer():
        print(msg)
    return printer()
fun=print_msg("hello")
