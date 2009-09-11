from functools import wraps

def run_until_stopped(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            try:
                self = args[0]
                self.shutdown()
            except (IndexError, AttributeError):
                pass
            pass
    
    return wrapped
