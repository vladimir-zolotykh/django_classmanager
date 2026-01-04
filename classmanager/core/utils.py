# core/utils.py
def create_class_instance(class_name, fields):
    """
    Dynamically create a simple class and return an instance.
    fields: dict of attribute_name -> value
    """
    cls = type(class_name, (object,), {})
    instance = cls()
    for k, v in fields.items():
        setattr(instance, k, v)
    return instance
