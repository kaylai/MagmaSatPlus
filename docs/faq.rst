#####
FAQ's
#####
.. contents::

These are still a work in progress. Have a Q? Get in touch by email: kayla.iacovino@nasa.gov. Or submit an issue on the `github repository <https://github.com/kaylai/VESIcal>`_.

I'm running a BatchFile with MagmaSat, and the calculation hangs or crashes
===========================================================================
Sometimes MagmaSat can fail to converge on an answer for a specific sample. In this case, your batch calculation will either hang on this sample, never spitting out a result, or a segmentation fault will occur within the ENKI thermoengine module (which MagmaSat runs on top of). We cannot catch these errors in VESIcal, since they are occuring within thermoengine. First, run `.get_data()` on your BatchFile object and visually inspect your data, ensuring values are present for all species as you expect them to be. Next, determine which sample is causing an issue (use the status bar as a guide). Try removing that sample from your BatchFile and running the calculate command again.
