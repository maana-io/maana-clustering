from ariadne import ObjectType, QueryType, MutationType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from asgi_lifespan import Lifespan, LifespanMiddleware
from graphqlclient import GraphQLClient

# HTTP request library for access token call
import requests
# .env
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


#import the schema
from app.types.types import clustering_types

import numpy as np
import pandas as pd
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans

def getAuthToken():
    authProvider = os.getenv('AUTH_PROVIDER')
    authDomain = os.getenv('AUTH_DOMAIN')
    authClientId = os.getenv('AUTH_CLIENT_ID')
    authSecret = os.getenv('AUTH_SECRET')
    authIdentifier = os.getenv('AUTH_IDENTIFIER')

    # Short-circuit for 'no-auth' scenario.
    if(authProvider == ''):
        print('Auth provider not set. Aborting token request...')
        return None

    url = ''
    if authProvider == 'keycloak':
        url = f'{authDomain}/auth/realms/{authIdentifier}/protocol/openid-connect/token'
    else:
        url = f'https://{authDomain}/oauth/token'

    payload = {
        'grant_type': 'client_credentials',
        'client_id': authClientId,
        'client_secret': authSecret,
        'audience': authIdentifier
    }

    headers = {'content-type': 'application/x-www-form-urlencoded'}

    r = requests.post(url, data=payload, headers=headers)
    response_data = r.json()
    print("Finished auth token request...")
    return response_data['access_token']


def getClient():

    graphqlClient = None

    # Build as closure to keep scope clean.

    def buildClient(client=graphqlClient):
        # Cached in regular use cases.
        if (client is None):
            print('Building graphql client...')
            token = getAuthToken()
            if (token is None):
                # Short-circuit for 'no-auth' scenario.
                print('Failed to get access token. Abandoning client setup...')
                return None
            url = os.getenv('MAANA_ENDPOINT_URL')
            client = GraphQLClient(url)
            client.inject_token('Bearer '+token)
        return client
    return buildClient()


# Define types using Schema Definition Language (https://graphql.org/learn/schema/)
# Wrapping string in gql function provides validation and better error traceback
type_defs = gql(clustering_types)

# Map resolver functions to Query fields using QueryType
query = QueryType()

# Resolvers are simple python functions

#cluster(dataToCluster: DataToClusterAsInput, algorithm: ClusteringAlgorithmAsInput): [ClusterMember]
@query.field("cluster")
def resolve_cluster(*_, dataToCluster, algorithm):

    # # A resolver can access the graphql client via the context.
    # client = info.context["client"]

    # # Query all maana services.
    # result = client.execute('''
    # {
    #     allServices {
    #         id
    #         name
    #     }
    # }
    # ''')

    # print(result)

    #transform dataToCluster
    data = []

    for r in dataToCluster["rows"]:
        data.append(r["values"])

    if(algorithm["algorithm"] == "KMeans"):
        #creates the algorithm
        kmeans = KMeans(init=algorithm["initializationMethod"], n_clusters=algorithm["numberOfClusters"], random_state=algorithm["randomSeed"], max_iter=algorithm["maxNumberOfIterations"] ,n_init=10)
        #cluster segements 
        y_kmeans = kmeans.fit_predict(data)
        print(y_kmeans)

        clusterMembers = []
        for s in range(len(y_kmeans)):
            member = {
                "id": dataToCluster["rows"][s]["id"],
                "segment": y_kmeans[s]
            }
            print(s)
            clusterMembers.append(member)
        return clusterMembers

@query.field("calculateWCSS")
def resolve_wcss(*_, dataToCluster, algorithm):
    data = []
    wcss = []
    for r in dataToCluster["rows"]:
        data.append(r["values"])

    if(algorithm["algorithm"] == "KMeans"):
        for i in range(1, 11):
            #creates the algorithm
            kmeans = KMeans(init=algorithm["initializationMethod"], n_clusters=i, random_state=algorithm["randomSeed"], max_iter=algorithm["maxNumberOfIterations"] ,n_init=10)
            kmeans.fit_predict(data)
            wcss.append(
                {
                    "id": "WCSS Cluster " + str(i),
                    "clusterNumber": i,
                    "value": kmeans.inertia_
                }
            )

        return wcss
        





@query.field("makeBlobsForTesting")
def resolve_make_blobs_for_testing(*_, samples, clusters, randomState, numberOfFeatures, clusterStandardDeviation):
    X, y = make_blobs(n_samples=samples, centers=clusters, cluster_std=clusterStandardDeviation, random_state=randomState, n_features=numberOfFeatures)
    #map to kind
    rows = []
    for r in range(len(X)):
        row =  {
            "id": "row " + str(r),
            "values": X[r]
        }
        rows.append(row)
    
    return {
        "id": "blob",
        "rows": rows
    }

# Create executable GraphQL schema
schema = make_executable_schema(type_defs, [query])

# --- ASGI app

# Create an ASGI app using the schema, running in debug mode
# Set context with authenticated graphql client.
#ontext_value={'client': getClient()}
app = GraphQL(
    schema, debug=True)

# 'Lifespan' is a standalone ASGI app.
# It implements the lifespan protocol,
# and allows registering lifespan event handlers.
lifespan = Lifespan()


@lifespan.on_event("startup")
async def startup():
    print("Starting up...")
    print("... done!")


@lifespan.on_event("shutdown")
async def shutdown():
    print("Shutting down...")
    print("... done!")

# 'LifespanMiddleware' returns an ASGI app.
# It forwards lifespan requests to 'lifespan',
# and anything else goes to 'app'.
app = LifespanMiddleware(app, lifespan=lifespan)
