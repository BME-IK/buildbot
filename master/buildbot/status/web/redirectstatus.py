from twisted.web import resource, util


class RedirectStatusResource(resource.Resource):

    def __init__(self, status):
        self.status = status

    def get_url(self, request):
        """ hi!
        """
        revision = request.args.get("revision", [None])[0]

        builder = request.args.get("builder", [])[0]

        if revision is not None and builder in self.status.getBuilderNames():
            build = self.status.getBuilder(builder).getBuild(0, revision)
            if build is not None:
                number = build.getNumber()
                url = "/builders/%(builder)s/builds/%(number)d" % {
                    'builder': builder,
                    'number': number,

                }
                return url
        return "/waterfall"

    def render(self, request):
        url = self.get_url(request)
        return util.redirectTo(url, request)

    def getChild(self, name, request):
        return self
