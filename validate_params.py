from jsonschema import validate

schema = \
    {
        "type": "object",
        "$schema": "http://json-schema.org/draft-03/schema",
        "required": False,
        "properties": {
            "connection": {
                "type": "object",
                "required": True,
                "properties": {
                    "host": {
                        "type": "string",
                        "required": True
                    },
                    "port": {
                        "type": "number",
                        "required": False,
                    },
                    "sid": {
                        "type": "string",
                        "required": True,
                    },
                    "user": {
                        "type": "string",
                        "required": True,
                    },
                    "password": {
                        "type": "string",
                        "required": True,
                    }

                }
            },
            "db": {
                "type": "object",
                "required": True,
                "properties":
                    {
                        "stored_procedure":
                            {
                                "type": "object",
                                "required": True,
                                "properties":
                                    {
                                        "sql": {
                                            "type": "string",
                                            "required": True
                                        },
                                        "args":
                                            {
                                                "type": "array",
                                                "required": True,
                                                "items":
                                                    {

                                                    }
                                            }
                                    }
                            }
                    }
            }
        }
    }

data = \
    {
        "connection":
            {
                "host": "oracle",
                "port": 1521,
                "sid": "lisa",
                "user": "lisa",
                "password": "lisaasil"
            },
        "db":
            {
                "stored_procedure":
                    {
                        "sql":
                            """
begin
  -- Call the function
  :result := chukov_test_package.test_sp(:ppolicyno);
end;
                            """,
                        "args":
                            [
                                {"name": "ppolicyno",
                                 "value": "30005017"},
                            ]
                    }
            }
    }

print(validate(data, schema))