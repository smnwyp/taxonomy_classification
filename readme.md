#how to run

## step0. config run env
using `requirements.txt` file under root

## step 1. config neo4j connection
in `constants.py` file under root, config the following 
3 constants accordingly.
```commandline
NACE_URL
NACE_USER
NACE_PWD
```

## step 2. run the script from commandline
```commandline
python3 main.py -i bomag-gmbh
python3 main.py -i bomag-gmbh namirial-spa
```
to get a list of all `id` 

# future work
1. `data_model.nace.NACENode` should derive from a generic `Node` class
2. error and edge-case handling
3. command piping of `neo4j`
4. spinning up huggingface locally
5. split steps into services linkable via msg queue or sinks
