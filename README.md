p4
==

django 1.6 six step tutorial completed. 

I went a bit beyond the tutorial to work within a virtual environment created using virtualenvwrapper (VEW).  VEW is a virtual environment for working on projects independent of other projects.  This improves workflow and prevents introducing interproject dependencies and dependencies on OS provided tools. 

South was installed to help me with database migrations within django projects.  It is database agnostic.

Fabric was installed to help with project management.  It let me automate unit test execution, git commits and git pushes using ssh.   A dev folder is used for development while a production folder is used for deployment.   This allows one to develop while leaving the production sites working without disruption.

