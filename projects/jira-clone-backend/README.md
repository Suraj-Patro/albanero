dataclass
dataclass_wizard
marshmallow



dataclass_wizard
    camel to snake conversion


marshmallow
    data preload after validation (if successful)
    else through the validation failure message
    ( no need to call extra function )


mongoDB actions into
    seperate classes
    merge with the data models itself
        not possible in case of some DB queries accross differnt collection
        otherwise implement the function in the class with the  list attribate
            pass the single variable accross


no Dunder methods


case conversion
auto data loading
data validation

skiping some fields from being serialised due to
    sensitive
    or too huge
    done using exclude parameter in pydantic field
    can be done by first doing to_dict()
    then removing ( del ) the desired fields
    and then doing json dumps

    or iterate over the list of desired fields
    and assign empty strings or shorter string to them
    then json dumps


preventing some extra data fields from being deserialised
    not hindering validation

avoid providing attributes metadata also in validation



https://docs.pydantic.dev/latest/usage/dataclasses/

allows use of dataclasses with data validation

Keep in mind

pydantic.dataclasses.dataclass
    drop-in replacement for dataclasses.dataclass
        with validation
    not a replacement for pydantic.BaseModel



flask error handler

https://flask.palletsprojects.com/en/2.3.x/errorhandling/


https://dataclass-wizard.readthedocs.io/en/latest/common_use_cases/serialization_options.html#exclude-fields

