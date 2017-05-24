# GRASS-rest

GRASS-rest aims to define and implement a [REST API](https://en.wikipedia.org/wiki/Representational_state_transfer) to [GRASS GIS](https://grass.osgeo.org/).
The `swagger/grass_gis.yaml` file define a [Swagger](http://swagger.io) compliant file documenting the API (work in progress). 
The overall concept of the possible GRASS REST API is described in  `swagger/grass_gis_concept.yaml` where it is possible to find a synthetic and simplified version of the API.

This is just a first attempt to define a REST API for GRASS. Comments and hints are welcome.

## Concept

The API is divided in three main components:
- `modules/` that return a JSON description of the GRASS GIS modules;
- `data/` that provide access to the GRASS data (i.e. gisbase, location, mapset) and the main contents (rasters, vectors, regions);
- `jobs/` to define the modules to be executed in which mapset. The API introduce two foreign words (job and task) respect to the GRASS world. With **task** we mean a GRASS module with all the parameters defined by the user. With **job** we define a series of tasks that can be executed in series or in parallel. Here an example of what could be the python equivalent:
```python
Job([Task("r.import"),
     Task("r.slope.aspect"),
     (Task("r.mapcalc"), Task("r.mapcalc")),
     Task("r.mapcalc"),
     Task("r.out.gdal")])
```
Every job/task is identified by a random [Universally Unique Identifier (UUID)](https://en.wikipedia.org/wiki/Universally_unique_identifier) and all the outputs (raster/vector) of a task will contains in the raster/vector metadata description field a JSON field with the uuid to the job and the task that generated the output.
Every job/task can define specific environmental variables. A shared set of environmental variables can be set a different level, the nested level inherit from the parents and can overwrite the values. The foreseen levels are: gisabase > location > mapset > job > task. Each gisbase can define the set of shared environmental variables (e.g. enable the null compression) then other specific options can be set/overwritten at lower level. The job contains the full record of the environmental variable inherited from the gisbase/location/mapset.
The job are characterized by three different status:
- staging: is a temporary draft of the job
- waiting: the job is in the queue to be executed, the status can be changed from waiting back to the staging area
- running: when the job status is in running it can not be modify any more by the user, and it is read-only. Once the job is executed the status can be nly one of the following status:
    - success: the job terminated without errors
    - failed: a task in the job terminates with errors
    - killed: the user kill the job.


## Open questions

* Should the data (gisbase/location/mapset) have always the same owner and add an extra layer on top of GRASS to manage the user permission/access to and from mapsets?
Or should we stick with unix filesystem permissions? The first solution has the advantage that the service can run without the root permission and can provide much more flexibility to manage users/teams/processes, but has the disadvantage that we need to develop a new layer to manage permission and it is not clear yet how to avoid user to execute `g.copy` copying data from a dataset that is accessible to GRASS but that should be not available to the user.
* Should we create a database (e.g. postgresql) to store history
