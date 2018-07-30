# Flask contact API practice
A quick exercise to try out flask. Auth is required for endpoints that modify data.

Made using python 2.7

Contacts have the following pieces of information:

* `first_name`
* `last_name`
* `email`
* `last_modified`

#### Notes: 

* `last_modified` is updated when a someone modifies data & stores their username.

### Authentication info
  This is hard coded into the main script.
  Username: `fakeuser`
  Password: `web`


# Example usage

* List all contacts

  ```curl http://localhost:5000/contacts```

* Add contact (req: `first_name` & `email`)

  ```curl -u fakeuser:web -H "Content-Type: application/json" -X POST -d '{"first_name":"Rudolph", "last_name":"DeReindeer", "email":"rudolph@brightnose.com"}' http://localhost:5000/contacts```

* Look up a specific contact by contact id

  ```curl http://localhost:5000/contacts/1```

* Delete contact

  ```curl -u fakeuser:web -H "Content-Type: application/json" -X DELETE http://localhost:5000/contacts/2```

* Update contact (req: `first_name`, `last_name` & `email`)

  ```curl -u fakeuser:web -H "Content-Type: application/json" -X PUT -d '{"first_name":"Mister", "last_name":"Grinch", "email":"mister.grinch@istolechristmas.com"}' http://localhost:5000/contacts/3```


# Possible Updates:

* Store epoch time but display user-friendly time when appropriate (currently only showing user-friendly values)
* Find a better solution for logging user modified so I don't need person_modifying = user_modified() in so many places