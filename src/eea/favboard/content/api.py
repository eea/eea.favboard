""" api.py """

from collective.bookmarks.api.utils import bookmark_dict_to_json_dict
from collective.bookmarks.api.utils import get_bookmark_from_request
from collective.bookmarks.api.utils import get_owner
from collective.bookmarks.storage import Bookmarks
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.services import Service
from zope.interface import alsoProvides
from repoze.catalog.query import Eq, NotEq
from zExceptions import NotFound


class BookmarksAll(Bookmarks):
    """BookmarksAll"""

    def fetch_all(self, query):
        """fetch all bookmarks

        """
        res = []
        for lazy_record in self._soup.lazy(query):
            res.append(self._dictify(lazy_record()))

        return res


class BookmarksGet(Service):
    """BookmarksGet"""

    def reply(self):
        """get all bookmarks

        """

        bookmark = BookmarksAll()
        try:
            owner = get_owner(request=self.request)
        # not sure if Exception covers all exceptions
        except Exception:
            owner = '__anonym__'

        query_eq = Eq("owner", owner)
        query_noteq = NotEq("owner", owner)
        bookmarks_eq = bookmark.fetch_all(query_eq)
        bookmarks_noteq = bookmark.fetch_all(query_noteq)
        bookmarks = bookmarks_eq + bookmarks_noteq

        if bookmarks:
            return [bookmark_dict_to_json_dict(x) for x in bookmarks]

        raise NotFound("No such bookmark found.")


class BookmarkPut(Service):
    """BookmarkPut"""

    def reply(self):
        """update bookmark by

        uid
        owner
        group
        queryparams (optional): serialized querystring

        Add new bookmark if bookmark not found.
        """
        owner, uid, group, queryparams, payload = get_bookmark_from_request(
            self.request, loadjson=True
        )
        alsoProvides(self.request, IDisableCSRFProtection)
        # payload = self.request.form.get("payload", "{}")
        bookmarks = Bookmarks()
        bookmark = bookmarks.update(owner, uid, group, queryparams, payload)
        if not bookmark:
            # be kind
            bookmark = bookmarks.add(owner, uid, group, queryparams, payload)
        self.request.response.setStatus(201)
        return bookmark_dict_to_json_dict(bookmark)
