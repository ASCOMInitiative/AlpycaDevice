..
    The rinohtype PDF builder I use chokes on right-justified images
    failing to wrap them with the text. It also chokes on the |xxx|
    format hyperlinks to externals that I use for opening in a separate
    tab. Therefore I have html and rinoh conditionals in these docs (typ)

.. only:: html

    .. image:: alpaca128.png
        :height: 92px
        :width: 128px
        :align: right

Frequently Asked Questions
==========================

.. _async_faq:

How can I tell if my asynchronous request failed after being started?
---------------------------------------------------------------------

All asynchronous (non-blocking) methods in ASCOM are paired with corresponding
properties that allow you to determine if the operation (running in the
background) has finished. There are two places where an async operation can
fail:

1. When you call the method that starts the operation, for example
   :py:meth:`Focuser.Move <alpaca.focuser.Focuser.Move>`. If you get an
   exception here, it means the device couldn't *start* the operation,
   for whatever reason. Common reasons include an out-of-range request
   or an unconnected device.
2. Later you read the property that tells you whether the async operation
   has finished, for example
   :py:attr:`Focuser.IsMoving <alpaca.focuser.Focuser.IsMoving>`. If you see
   the value change to indicate that the operation has finished, you can be
   *100% certain that it completed successfully*. On the other hand, if you
   get an exception here
   (usually :py:class:`~alpaca.exceptions.DriverException`), it means the
   device *failed to finish the operation successfully*. In this case,
   the device is compromsed and requires special attention.

.. tip::

    .. only:: html

        Have a look at this article |excpdang|. While the article uses the
        C# language and acync/await to illustrate the so-called "dangers"
        (failing to await), the exact same principles apply here.
        In the example above, you really must use
        :py:attr:`Focuser.IsMoving <alpaca.focuser.Focuser.IsMoving>`
        to determine completion. It is the 'await'
        in this cross-language/cross-platform environment. If you ignore
        :py:attr:`Focuser.IsMoving <alpaca.focuser.Focuser.IsMoving>` and instead
        “double-check” the results by comparing your request with the results,
        you run several risks, including

    .. only:: rinoh or rst

        Have a look at this article
        `Why exceptions in async methods are “dangerous” in C# <https://medium.com/@alexandre.malavasi/why-exceptions-in-async-methods-are-dangerous-in-c-fda7d382b0ff>`_.
        While the article uses the C# language and acync/await
        to illustrate the so-called "dangers" (failing to await), the
        exact same principles apply here. In the example above, you really
        must use
        :py:attr:`Focuser.IsMoving <alpaca.focuser.Focuser.IsMoving>`
        to determine completion. It is the 'await'
        in this cross-language/cross-platform environment. If you ignore
        :py:attr:`Focuser.IsMoving <alpaca.focuser.Focuser.IsMoving>` and
        instead “double-check” the results by comparing your request
        with the results, you run several risks, including

1. A lost exception (an integrity bust),
2. a false completion indication if the device passes through the requested
   position on its way to settling to its final place, and
3. needing to decide what “close enough” means.

Plus it needlessly complicates your code. We have to design for, and require,
trustworthy devices/drivers.

.. |excpdang| raw:: html

    <a href="https://medium.com/@alexandre.malavasi/why-exceptions-in-async-methods-are-dangerous-in-c-fda7d382b0ff"
    target="_blank">
    Why exceptions in async methods are “dangerous” in C#</a> (external)

