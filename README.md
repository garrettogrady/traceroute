# traceroute
Traceroute implemented in Python
Programming assignment for Computer Networking

Requirements
============

* Python 2.7.x

Installation
============

Clone the Git repository and install:

.. code-block:: bash

   $ git clone https://github.com/garrettogrady/traceroute.git

Usage
=====

pytraceroute requires root permissions due to the use
of raw (`socket.SOCK_RAW`) sockets so sudo is required when running.

Example usage:

   $ sudo py-traceroute google.com
