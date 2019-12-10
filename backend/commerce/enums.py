class CheckEnum:
    TYPE_KITCHEN = 'kitchen'
    TYPE_CLIENT = 'client'
    CHECK_TYPE = (
        (TYPE_KITCHEN, 'kitchen'),
        (TYPE_CLIENT, 'client'),
    )

    STATUS_NEW = 'new'
    STATUS_RENDERED = 'rendered'
    STATUS_PRINTED = 'printed'
    CHECK_STATUS = (
        (STATUS_NEW, 'new'),
        (STATUS_RENDERED, 'rendered'),
        (STATUS_PRINTED, 'printed'),
    )
