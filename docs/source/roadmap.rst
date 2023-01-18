.. image:: alpaca128.png
    :height: 92px
    :width: 128px
    :align: right

=================
Developer Roadmap
=================


Before starting your development project, it is highly recommended that you take
a few minutes to read through |princ|. Also, t's suggested that you make an
Alpaca driver for a single ASCOM device type and a single instance of that
device. This roadmap is written with that in mind.

Alpaca Driver Request Flow - Responder Classes
----------------------------------------------

Incoming HTTP/REST requests from the client are routed through the server by
Falcon, and result in calls to the *responder* classes for the device API. For
example, an app would send the following HTTP request to see if the rotator is
moving:

``/api/v1/rotator/0/ismoving?ClientID=xxx&ClientTransactionID=yyy``

Here is the code to handle a simple request for the Rotator's
:py:class:`~rotator.IsMoving` property.

.. image:: ismoving.png
    :height: 264px
    :width: 700px
    :align: center

Preprocessor
~~~~~~~~~~~~

``@before`` - This is a decorator :py:class:`~shr.PreProcessRequest()` which is
applied to all responder classes. Its job is to quality check the request. It
rejects illegal values for Alpaca ``ClientID`` and ``ClientTransactionID``. It
also checks that the ``DeviceNumber`` is a valid integer. If any of these tests
fail, it raises an ``HTTPBadRequest`` [#f1]_  with a body containing a specific
error message.

.. note::

    Raising an ``HTTPBadRequest`` [#f1]_ anywhere within a responder, including
    within the low-level device logic or a decorator, immediately abandons
    processing  and and sends an HTTP ``400 Bad Request`` response back to the
    client. It cannot be an Alpaca response (which would have a ``200 OK``
    status) because the request is not even a legal Alpaca request.

GET responder
~~~~~~~~~~~~~

Once the request is deemed Alpaca-legal by the pre-processor, the responder's
``on_get()`` method is called if the API request is for a ``GET`` (get the value
of a property). The first thing you see is a call into the rotator device to see
if it is connected. If not, it's an Alpaca
:py:class:`~exceptions.NotConnectedException`. Then it tries to read the
position from the rotator device. If an exception is raised from within the
device code, it's caught with a generic ``except`` and results in an Alpaca
:py:class:`~exceptions.DriverException`. Otherwise, it uses a
:py:class:`~shr.PropertyResponse` object to construct the JSON for an Alpaca
property response, including the retrieved position value. For example:

.. code-block:: json
    :emphasize-lines: 2
    :caption: Alpaca property response

    {
        "Value": true               // It's moving
        "ClientTransactionID": 321,
        "ServerTransactionID": 1,   // Automatically bumped by PropertyResponse
        "ErrorNumber": 0,           // Success
        "ErrorMessage": "",
    }

It sets the ``Response.text`` to the above Alpaca JSON, and returns to Falcon,
which sends the response to the remote app the JSON as the HTTP body with a
``200 OK`` status. That's it!

PUT Responder
~~~~~~~~~~~~~

Alpaca API *method* calls, those which do something, use the HTTP ``PUT``
method. Here is the responder code for :py:class:`~rotator.MoveAbsolute`:

.. image:: moveabsolute.png
    :height: 375px
    :width: 700px
    :align: center

The main thing to note here is that the parameter for the *method* comes in the
HTTP body of the ``PUT``. Falcon provides the ``req.get_media()`` function to
get the form data, and the fields are in a Python dictionary. So for example the
``Position`` parameter to ``MoveAbsolute()`` is element ``'Position'`` of the
dictionary. It uses the :py:class:`~shr.MethodResponse` class to construct the
JSON response. We'll cover the more detailed exception handling in the next
section.


Alpaca Exceptions
-----------------

Continuing with the above sample, note how the Alpaca
:py:class:`~exceptions.NotConnectedException` is returned to the remote app. The
:py:class:`~shr.PropertyResponse` constructor gets the Falcon ``Request`` object
as its first parameter. The second parameter, the Alpaca exception class
:py:class:`~exceptions.NotConnectedException` is used by
:py:class:`~shr.PropertyResponse` to get the Alpaca error number and an error
message with which it constructs the Alpaca JSON Response:

.. code-block:: json
    :emphasize-lines: 2,3
    :caption: Alpaca **NotConnectedException** response

    {
        "ErrorNumber": 1031,        // 0x407
        "ErrorMessage": "The device is not connected.",
        "Value": ""                 // App ignores this value if present
    }

It sets the ``Response.text`` to the above Alpaca JSON, and returns to Falcon,
which returns the JSON as the HTTP body with a ``200 OK`` status. Note that any
Alpaca request which gets to the responder always returns with an HTTP ``200
OK`` status, even though the response might be an Alpaca exception like this.

.. tip::

    You can supply your own error message as an optional parameter to any of the
    Alpaca exception classes. You should try to help the client app and its user
    by providing specifics about the error, and even perhaps a suggestion on how
    to fix the problem.

.. _driver-exception:

Run-Time Errors - DriverException
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Alpaca :py:class:`~exceptions.DriverException` is specified for use by the
device for any error or failure not covered by the other more specific Alpaca
exceptions. In the example above notice that the call into the device
``rot_dev.ismoving`` is guarded by a ``try/except``. The exception is passed to
the ``DriverException`` class which creates a detailed report. Let's see how
this works...

.. important::

    It's vital that *any* problem encountered by your device be telegraphed back
    to the app via one of the Alpaca exceptions. For most problems, this will be
    the ``DriverException``.

Throughout the template/sample, the invocation of ``DriverException`` uses some
Python magic to The :py:class:`~exceptions.DriverException` has unique
enhancements. Look now. In the example above, note the construction of
``DriverException`` includes an error code, an automaticelly constructed
responder class name, and the Python exception object. This allows
``DriverException`` to construct a detailed error message that includes the API
endpoint name (the name of the responder class), the Python module and line
number, and optionally a Python call stack traceback (the
:py:attr:`~config.Config.verbose_driver_exceptions` config option).

Also, since ``DriverException`` can use any error codes from ``0x500`` through
``0xFFF``, you can supply an error code. These codes are for you to use and have
no specified meaning within Alpaca.

Invocations of DriverException
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throughout the template/sample, the invocation of ``DriverException`` uses some
Python 'dunders' to help get the endpoint name into the error message, and also
hand the caught Python runtime exception (``as ex``) to ``DriverException`` for
error reporting including possible traceback (see next section). You will see
this pattern used throughout the template/sample and it is self-documenting
thanks to the dunders.

.. code-block:: python

    except Exception as ex:
        resp.text = MethodResponse(req, # Put is actually like a method :-(
                        DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
        return


.. attention::

    This may surprise you, but if your device runs into trouble after
    successfully starting an operation, you *must* raise an exception when
    the client app later asks for the status of that operation. See
    :ref:`excep-intro` and |async|.

So if your Rotator accepts a request to move to a new angle, and then gets
jammed up or otherwise fails to successfully complete the move to the new angle,
then :py:class:`~rotator.IsMoving` must raise a ``DriverException``, preferably
with a detailed error message like ``Rotator has failed, possible jam or cable
wrap``. If the *completion property* ``IsMoving`` returns False it means "no
longer moving and it got there *successfully*."

In this case, even deep within your device code, raise any Python exception
(e.g. ``RuntimeError``) with your detailed message. The boiler plate exception
handling shown above and used in all of the responder classes will turn this
into a useful Alpaca ``DriverException``.

.. note::

    The app must always check :py:class:`~rotator.IsMoving`
    to make sure that the move request completed successfully.


Example of DriverException with Verbose and Concise Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the exception handling in action, look at the
:py:meth:`rotatordevice.RotatorDevice.MoveAbsolute` method in the simulated
rotator logic where it checks to see if it's being asked to move while it's
already moving:

.. code-block:: python
    :emphasize-lines: 3

    if self._is_moving:
        self._lock.release()
        raise RuntimeError('Cannot start a move while the rotator is moving')

Now start up the rotator sample and then use a tool like ``curl`` or the
|thunder| to send Alpaca HTTP requests to set ``Connected`` to ``True`` then
``MoveAbsolute(123)`` which will take some time. Now, while it is moving, make
another request to ``MoveAbsolute()``. This will trigger the above logic to
raise an internal Python ``RuntimeError``. The result will be your driver
returning something like the following ``DriverException`` (with a ``200 OK``
HTTP status).

.. code-block:: json

    {
        "ServerTransactionID": 3,
        "ClientTransactionID": 321,
        "ErrorNumber": 1280,
        "ErrorMessage": "DriverException: MoveAbsolute failed
                Traceback (most recent call last):
                File \"device/rotator.py\", line 292, in on_put
                    rot_dev.MoveAbsolute(newpos)    # async
                        File \"device/rotatordevice.py\", line 289, in MoveAbsolute
                            raise RuntimeError('Cannot start a move while the rotator is moving')
                            RuntimeError: Cannot start a move while the rotator is moving"
    }

Since the low-level call and the Alpaca endpoint names are the same and also the
line numbers in the two modules are similar, this may be confusing. What this
traceback says is that the Python exception ``RunTimeError`` is raised at line
289 in the **rotatordevice.py** module (in *its*
:py:meth:`~rotatordevice.RotatorDevice.MoveAbsolute`) method, and that was
called at line 292 in the Alpaca API responder class'
:py:meth:`rotator.MoveAbsolute.on_put` handler. Note the first part of the
``ErrorMessage`` automatically prints the Alpaca exception type
``DriverException`` as well at the name of the Alpaca API EndPoint
``MoveAbsolute``. Also note that the error message passed To the Python
RunTimeError exception appears in the Alpaca DriverException error message.

.. note::

    Observe that the Rotator continues to function normally. The initial
    ``MoveAbsolute`` will complete normally, at which time ``IsMoving`` will
    transition from ``True`` To ``False``. The failed second ``MoveAbsolute()``
    will fail without compromising the device's operation.

With the :py:attr:`~config.Config.verbose_driver_exceptions` config option set
to ``false``, this is what is returned when the app violates the "can't move
while moving" rule.

.. code-block:: json

    {
        "ServerTransactionID": 3,
        "ClientTransactionID": 321,
        "ErrorNumber": 1280,
        "ErrorMessage": "DriverException: MoveAbsolute failed
                RuntimeError: Cannot start a move while the rotator is moving"
    }

This is more suitable for production and end-user operations. However to help
troubleshoot device and driver issues, the verbose/traceback option is provided.

.. note::

    All of this is provided by the "boilerplate" logic in the sample/tempate.
    All you need to do is raise an exception in your Python code that gets
    called from any of the Alpaca API responder classes.

Unhandled Exceptions
--------------------

What happens if there is an unhandled exception somewhere? If it's triggered
during handling of an Alpaca request, it needs to result in an HTTP ``500 Server
Error`` response. This template/sample handes this as well. See
:py:func:`app.falcon_uncaught_exception_handler`, which calls
:py:func:`app.custom_excepthook` to make sure the exception info is logged, then
it sends the ``500 Server Error``. The simplicity of this logic is possibly lost
in all of the docstring info.

Last but not least, if an unhandled exception occure *outside* the context of a
Falcon API responder, it ends up in the "last-chance exception handler"
:py:func:`app.custom_excepthook`. Here, a Control-C is allowed to kill the
application. Otherwise the unhanded exception is logged and dismissed. If there
is any possibility that the Python code can still run, it will. If the exception
leads to a cascade of other exceptions, the Python will eventually die. This
handler is installed during app startup :py:func:`app.main`. Have a look at this
but don't change anything except the list of API endpoint class modules that
:py:func:`app.init_routes` sets up.

.. rubric:: Footnotes

.. [#f1] Exception defined by Falcon

..
    Below are links that will open in a separate browser tab for convenience.

.. |guidgen| raw:: html

    <a href="https://guidgenerator.com/online-guid-generator.aspx" target="_blank">
    Online GUID / UUID Generator</a>

.. |conformu| raw:: html

    <a href="https://github.com/ASCOMInitiative/ConformU#readme" target="_blank">
    Conform Universal</a>

.. |princ| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Principles.htm" target="_blank">
    The General Principles</a>

.. |async| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Async.htm" target="_blank">
    Asynchronous APIs</a>

.. |excep| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Exceptions.htm" target="_blank">
    Exceptions in ASCOM</a>

.. |falcweb| raw:: html

    <a href="https://falcon.readthedocs.io/en/stable/" target="_blank">
    The Falcon Web Framework</a>

.. |apiref| raw:: html

    <a href="https://github.com/ASCOMInitiative/ASCOMRemote/raw/master/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf"
    target="_blank">Alpaca API Reference (PDF)</a>

.. |thunder| raw:: html

    <a href="https://www.thunderclient.com/" target="_blank">
    Thunder Client for VS Code</a>

