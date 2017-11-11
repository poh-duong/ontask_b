
## 1.1.0 

### Removed

- Support for SQLite3. Now using only postgresql

- Token authentication

- Major overhaul of code to polish bugs in all packages.

## 1.0.2 2017-10-22

### Added

- Shared workflows now have restricted operations. Delete, flush, rename are
  only allowed to owners.
  
- Columns can now also be added from the matrix screen.

- Send email now checks for correctness of email addresses (basic check)
  
### Changed

- Fixed a bug in a redirect when finishing the attributes screen with a Save
  and close.

- Workflow model now stores all the information about columns in a single 
  JSON object rather than three of them individually. This is to include in 
  the future things like "category names" for the values in the column (and 
  simplify data entry for rows). This is a transparent change in the 
  underlying model.
  
- Major revamp of the column representation. It now has its own data model 
  (instead of being folded as JSON fields in the Workflow model). Major 
  rewrite of the column-handling functions/views to account for this change.
  
- Fixed several bugs in the merge procedure (column reordering, column 
  renaming in the data_frame, and combining renaming and selection of key 
  columns).
  
- Fixed the import/export in the presence of the new column model + tested 
  cases of full/partial export with full/partial import. Serializers are now 
  properly invoked in a recursive way.
  
- Code reorg to curb down on large files.

- Wrote the templates and views for the pages for 404, 403, 400 and 500.
   
## 1.0.1 2017-10-18

### Added

- The possibility to turn the URL for serving an action on/off
- The possibility to share workflows. The functionality relies on the sessions
   being stored in the database. It assigns a session key to each workflow that
   is remove once the user goes back to the main page or the session expires.
   Any access to a workflow is checked against the owner, the users that can
   access it (ManyToMany relation in workflow) and if the workflow has the 
   sesison_key of an active session.
    
- Filter name does not need to be restricted to have a "variable" name style.

## 1.0.0 2017-10-17

### Added

- This CHANGELOG file will include the developments included in OnTask
- Deployed the production instance with the basic functionality:
    - Workflow, action, condition and filter creation
    - HTML preview based on condition
    - Bulk email with notification email, tracking, and message preview
    - Import/export of workflows with/without data.
    - Update/Merge of CSV with automatic detection of data types and unique
      keys. Merge procedure allows user to select key, rename columns and
      choose the modality of merging.
    - API offering functionality to list, create, update and delete workflows,
      as well as updating and merging data frames.
    - Workflow operations to manage attributes, column names, key columns
    - Search and Data entry for individual rows
    - Column deletion
    - Fully operational admin subsite with permission control of all the
      objects, user and group manipulation, handling Token authentiation for 
      the API, and user profile.