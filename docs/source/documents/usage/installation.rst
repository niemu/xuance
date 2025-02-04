Installation
===========================

The library can be run at Linux, Windows, MacOS, and EulerOS, etc. It is easy to be installed.

Before installing **XuanCe**, you should install Anaconda_ to prepare a python environment.

After that, open a terminal and install **XuanCe** by the following steps.
You can choose two ways to install XuanCe.

.. raw:: html

   <br><hr>

Install via PyPI
---------------------------------------------

**Step 1**: Create a new conda environment (python>=3.7 is suggested).

.. code-block:: bash

    conda create -n xuance_env python=3.7

**Step 2**: Activate conda environment.

.. code-block:: bash
    
    conda activate xuance_env

**Step 3**: Install the library.

.. code-block:: bash
    
    pip install xuance

This command does not include the dependencies of deep learning toolboxes. 

You can also install the **XuanCe** with PyTorch_, TensorFlow2_, MindSpore_, or all of them.

.. code-block:: bash
    
    pip install xuance[torch]

or

.. code-block:: bash
    
    pip install xuance[tensorflow]

or

.. code-block:: bash
    
    pip install xuance[mindspore]

or

.. code-block:: bash

    pip install xuance[all]

Install from GitHub repository
---------------------------------------------

Alternatively, you can install XuanCe from its GitHub repository.

.. note::

    Note: The steps 1-2 are the same as above.

**Step 1**: Create a new conda environment (python>=3.7 is suggested).

.. code-block:: bash

    conda create -n xuance_env python=3.7

**Step 2**: Activate conda environment.

.. code-block:: bash

    conda activate xuance_env

**Step 3**: Download the source code of XuanCe from GitHub.

.. code-block:: bash

    git clone https://github.com/agi-brain/xuance.git

**Step 4**: Change directory to the xuance.

.. code-block:: bash

    cd xuance

**Step 5**: Install xuance.

.. code-block:: bash

    pip install -e .

.. note::

    Note: Some extra packages should be installed manually for further usage.

.. _Anaconda: https://www.anaconda.com/download
.. _PyTorch: https://pytorch.org/get-started/locally/
.. _TensorFlow2: https://www.tensorflow.org/install
.. _MindSpore: https://www.mindspore.cn/install/en

.. raw:: html

   <br><hr>

Testing whether the installation was successful
--------------------------------------------------------------------

After installing XuanCe, you can enter the Python runtime environment by typing "python" in the terminal.
Then, test the installation of xuance by typing:

.. code-block:: python

    import xuance

If no error or warning messages are displayed, it indicates that XuanCe has been successfully installed.
You can proceed to the next step and start using it.

