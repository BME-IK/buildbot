import os
import sys
import cPickle as pickle

from buildbot.status.results import Results

# path to the buildbot master directory
MASTER = "/home/cloud/master-cloud"
# path to the public_html directory with the PNG files
PNG = "/home/cloud/public_html/pngstatus"
SIZES = ["small", "normal", "large"]


def migrate(builder):
    directory = "%s/%s" % (MASTER, builder)
    files = os.listdir(directory)
    builds = []
    for f in files:
        if f.isdigit():
            build = pickle.load(open("%s/%s" % (directory, f), "rb"))
            builds.append(build)

    builds = sorted(builds, key=lambda build: build.getNumber())
    create_directories(builder)
    for b in builds:
        create_links(builder, b)


def create_directories(builder):
    try:
        os.mkdir("%s/%s" % (PNG, builder))
        for s in SIZES:
            os.mkdir("%s/%s/%s" % (PNG, builder, s))
    except:
        pass


def create_links(builder, build):
    revision = build.getAllGotRevisions().get("")
    result = build.getResults()
    for s in SIZES:
        source = "%s/%s_%s.png" % (PNG, Results[result], s)
        link_name = "%s/%s/%s/%s.png" % (PNG, builder, s, revision)

        try:
            os.symlink(source, link_name)
        except OSError:
            os.remove(link_name)
            os.symlink(source, link_name)


if __name__ == "__main__":
    """ Usage example
    python migrate.py builder1 builder2
    """
    for a in sys.argv[1:]:
        migrate(a)
