marshmallow
    ORM/ODM/framework-agnostic library
    for converting complex datatypes
        such as objects
    to and from native Python datatypes



from datetime import date
from pprint import pprint

from marshmallow import Schema, fields


class ArtistSchema(Schema):
    name = fields.Str()


class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
    artist = fields.Nested(ArtistSchema())


bowie = dict(name="David Bowie")
album = dict(artist=bowie, title="Hunky Dory", release_date=date(1971, 12, 17))

schema = AlbumSchema()
result = schema.dump(album)
pprint(result, indent=2)
# { 'artist': {'name': 'David Bowie'},
#   'release_date': '1971-12-17',
#   'title': 'Hunky Dory'}

In short, marshmallow schemas can be used to:

    Validate input data.

    Deserialize input data to app-level objects.

    Serialize app-level objects to primitive Python types
    serialized objects can then be rendered to standard formats such as JSON for use in an HTTP API

