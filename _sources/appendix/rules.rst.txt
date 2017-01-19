useblocks convention
====================

1. We keep all stuff, which belongs together, inside one repository
2. We can open all stuff, which is developed by us, in our IDE
3. We write and use tests
4. We write and publish user documentation
5. We publish code, tests, documentation as versioned package
6. We use logging libraries inside our tools
7. We provide configuration capabilities for our tools
8. We use exceptions
9. We have and follow coding rules
10. We write tons of documentation inside our code
11. We are using continuous integration with ruthless tests

We keep all stuff, which belongs together, inside one repository
----------------------------------------------------------------

* Everything can get an issue in our bug tracker
* Everything can get a version
* Everything is in sync

We can open all stuff, which is developed by us, in our IDE
-----------------------------------------------------------

* No annoying tool switches
* No additional Know How needed
* No "I do it later, when I have finished here..."
* Creating links between code, tests and documentation is easy

We write and use tests
----------------------

* We can sleep well during nights
* Tests are written once and reused hundreds of time
* You can trust others to make changes to your code
* You find bugs during writing of tests
* You use your code the same way like other developers will do

We write and publish user documentation
---------------------------------------

* A link via eMail or 2 hours telephone support. You have the choice
* Use it for selling your tool

We publish code, tests, documentation as versioned package
----------------------------------------------------------

* Proof the quality of your work to the user
* Let the user get everything, which may be needed, with one download
* Know if something is outdated

We use logging libraries inside our tools
-----------------------------------------

* Let the user decide, how and where logs are stored
* Support all forms of logging: console, file, db, email, service, ...

We provide configuration capabilities for our tools
---------------------------------------------------

* Do not have magic numbers in code
* Allow users to use their preferred way of configuration (cli parameter, config file, environment vars, REST API, ...)

We use exceptions
-----------------

* Do not only use print or log messages for errors
* Let calling function know about errors
* Let calling functions decide how to treat errors

We have and follow coding rules
-------------------------------

* Other developers can easily read your code
* Other developers can extend your code
* Reduces the source of errors


We write tons of documentation inside our code
----------------------------------------------

* Other developers can easily understand and extend your code
* Documentation can be reused outside the code (documentation, application)
* Documentation can be used to automatically generate test cases.

We are using continuous integration with ruthless tests
-------------------------------------------------------

* Be sure that each commit fulfills the above rules
* Get great quality with each commit
* Do not get buggy code from others
