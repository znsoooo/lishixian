__all__ = list(globals())

...

__all__ = [k for k in globals() if k not in __all__]
