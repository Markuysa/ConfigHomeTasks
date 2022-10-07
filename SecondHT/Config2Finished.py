import zipfile
import requests
import io
import graphviz as gv

def getMetadata():
    pypiURL = requests.get(f"https://pypi.org/pypi/{packageName}/json").json()
    currentVersion = pypiURL["info"]["version"]  # getting the current version of the package
    allreleases = pypiURL["releases"]
    currentVersionRelease = allreleases[currentVersion][0]  # from all releases gets the newest
    currentVersionReleaseURL = currentVersionRelease["url"]  # gets the url ro metadata file
    File = requests.get(currentVersionReleaseURL)
    return zipfile.ZipFile(io.BytesIO(File.content)) # returns the zipfile archive, that consists of data from our metafile

def formDependencies():
    global metadata
    archive = getMetadata() #getting the zipfile object with metadata file
    for name in archive.namelist():
        if name.endswith("METADATA"): # looks for the file with ../METADATA at the end of its name
            metadata = (str(archive.read(name), 'utf-8')) # reads the metadata object
    if metadata==None: return -1
    dependencies = list()
    splittedMEta = metadata.split("\n")
    for meta in splittedMEta:
        if "Requires-Dist" in str(meta):
            dependency = meta.split(" ") #gets the dependency from meta file
            if (dependency[2]!=";"): dependency[1]+=dependency[2]  #if there is a version in dependency
            dependencies.append(dependency[1])
    return dependencies
def buildGraph(Depends):
    dGraph = gv.Digraph(comment='Dependencies of {}'.format(packageName))
    dGraph.node(packageName, packageName)
    for dep in Depends:
        dGraph.node(dep, dep)                     # sets the connections btwn nodes
        dGraph.edge(packageName, dep)

    dGraph.render('test-output/round-table.gv', view=True) # renders the graph (outputs in pdf)



def main():
    global packageName
    global metadata
    packageName = input()
    packageName=packageName.lower()
    dependencies = formDependencies()
    buildGraph(dependencies)
if __name__ == '__main__':
    main()
