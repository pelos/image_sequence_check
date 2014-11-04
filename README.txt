image_check.py

checks the integrity of a image sequence,  will check the frame range match
and will verify that each image doesnt contain errors.



run from the command line as

folder/image_check.py -file "/path/to/check"

ui will march down the folder puting the path into the UI
user can specify start frame and end frame.


Run will loop the UI with check box on,
and will check that the exr file is not corrupt,
(checking right and left eye for stereoscopic renders)

and that the sequence of files is complete
will any errors if there is a missing image or is corrupted.