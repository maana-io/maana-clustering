# Maana Q Knowledge Microservice: Maana Clustering


## Features










### Maana Q Client (i.e., peer-to-peer)

It is possible, though not generally preferred, for services to depend directly on other services, passing requests through a secure CKG endpoint.  This template includes the necessary authentication code for your convenience.  Simply supply environment settings and use the `client` from the GraphQL context:

```bash
#
# ---------------APPLICATION VARIABLES-------------------
#

MAANA_ENDPOINT_URL=


#
# ---------------AUTHENTICATION VARIABLES--------------------
#

# keycloak or auth0
AUTH_PROVIDER=

# URL for auth server (without path), i.e. https://keycloakdev.knowledge.maana.io:8443
AUTH_DOMAIN=

# Keycloak or auth0 client name/id.
AUTH_CLIENT_ID=

# Client secret for client credentials grant
AUTH_SECRET=

# Auth audience for JWT
# Set to same value as REACT_APP_PORTAL_AUTH_IDENTIFIER in Maana Q deployment ENVs)
# NOTE: For use of keycloak in this app, this value should match both the realm and audience values. 
AUTH_IDENTIFIER=
```

And, in your resolver:

```python
    # A resolver can access the graphql client via the context.
    client = info.context["client"]

    # Query all maana services.
    result = client.execute('''
    {
        allServices {
            id
            name
        }
    }
    ''')

    print(result)
```

## Deploy

To simplify deployment to your Maana Q Kubernetes cluster, use the [CLI `mdeploy` command](https://github.com/maana-io/q-cli#mdeploy):

```
gql mdeploy
```

and follow the prompts.
