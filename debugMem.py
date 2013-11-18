#!/usr/bin/env python


import gc
import inspect

exclude = [
    "function",
    "type",
    "list",
    "dict",
    "tuple",
    "wrapper_descriptor",
    "module",
    "method_descriptor",
    "member_descriptor",
    "instancemethod",
    "builtin_function_or_method",
    "frame",
    "classmethod",
    "classmethod_descriptor",
    "_Environ",
    "MemoryError",
    "_Printer",
    "_Helper",
    "getset_descriptor",
    "weakref", "property", "cell", "staticmethod",
    "Quitter", "CodecInfo", "_TemplateMetaclass",
    "staticmethod",
    ]

def dumpObjects(outfile):
    global exclude
    gc.collect()
    oo = gc.get_objects()
    for o in oo:
        if getattr(o, "__class__", None):
            name = o.__class__.__name__
            if name not in exclude:
                try: filename = inspect.getabsfile(o.__class__)
                except TypeError:
                    exclude.append(name)
                    continue
                print >> outfile, "Object :", repr(o), "..."
                print >> outfile, "Class  :", repr(name), "..."
                print >> outfile, "defined:", filename, "\n"

if __name__=="__main__":

    class TestClass:
        pass

    testObject1 = TestClass()
    testObject2 = TestClass()

    dumpObjects(sys.stdout)
